from django.shortcuts import render, get_object_or_404, reverse
from myapp.models import Contact, Dish, Team, Category, Profile, Order
from django.http import HttpResponse,JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from datetime import datetime
from .models import *
import razorpay




def purchase(request,id):
  dish = Dish.objects.get(pk=id)
  differ = dish.price - dish.discounted_price
  user = User.objects.get(username = request.user)
  profile = Profile.objects.get(user = user.pk)
  if request.method == "POST":
    order_detaile = Dish.objects.get(pk = id)
    amount = order_detaile.discounted_price*100
    client = razorpay.Client(auth=('rzp_test_Gj86C8HLpdXP5v','QdbDoue6rGerUbLL48bEdxUD'))

    payment = client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
    print(payment)

    order = Order(customer_id = int(profile.pk),item_id = dish.pk,invoice_id = payment['id'])
    order.save()
    return render(request,'checkoutpage.html',{'payment':payment,'order':order_detaile})
  return render(request,'checkoutpage.html',{'order':dish,'discount':differ}) 

#rzp_test_Gj86C8HLpdXP5v

def success(request):
  return render(request,'success.html')
@csrf_exempt
def index(request):
    if request.method == 'POST':
        # Check if it's a form submission
        name = request.POST.get('Name')
        if name is not None:
            # Handle form submission
            name = request.POST.get('Name')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            booking_date = request.POST.get('date')
            booking_time = request.POST.get('time')
            num_guests = request.POST.get('number_guest')

            date_obj = datetime.strptime(booking_date, "%m/%d/%Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            time_obj = datetime.strptime(booking_time, "%I:%M %p")
            formatted_time = time_obj.strftime("%H:%M")
            # Create a new TableBooking object and save it to the database
            table_booking = TableBooking.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                booking_date=formatted_date,
                booking_time=formatted_time,
                num_guests=num_guests
            ) 
            # Redirect the user to a success page or wherever you want
            return render(request, 'index.html')
        else:
          a = request.POST
          order_id = ""
          for key, val in a.items():
              if key == 'razorpay_order_id':
                  order_id = val
                  break
          order = Order.objects.filter(invoice_id=order_id).first()
          if order is not None:
              order.status = True
              order.save()

    context = {}
    cats = Category.objects.all().order_by('name')
    context['categories'] = cats
    dishes = []
    for cat in cats:
        dishes.append({
            'cat_id': cat.id,
            'cat_name': cat.name,
            'cat_img': cat.image,
            'items': list(cat.dish_set.all().values())
        })
    context['menu'] = dishes
    return render(request, 'index.html', context)





def contact_us(request):
  # make context dictionary, we use this when we want to send something from python to HTML
  context={}
  if request.method=="POST":
    name = request.POST.get("name")
    em = request.POST.get("email")
    sub = request.POST.get("subject")
    msz = request.POST.get("message")
    
    obj = Contact(name=name, email=em, subject=sub, message=msz)
    # no need of any queries, this database connectivity is inbuilt in django
    obj.save()
    context['message']=f"Dear {name}, Thanks for your time!"

  return render(request,'contact.html', context)





def about(request):
  return render(request,'about.html')





def team_members(request):
  context={}
  members = Team.objects.all().order_by('name')
  context['team_members'] = members
  return render(request,'team.html',context)





def all_dishes(request):
  context={}
  dishes = Dish.objects.all()
  if "q" in request.GET:
    id = request.GET("q")
    dishes = Dish.objects.filter(category_id=id)
    context['dish_category'] = Category.objects.get(id=id).name
  
  context['dishes'] = dishes
  return render(request,'all_dishes.html',context)



def register(request):
  context={}
  if request.method=="POST":
    # fetch data from html form
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pass')
    contact = request.POST.get('number')
    check = User.objects.filter(username=email)
    if len(check)==0:
      # Save data to both tables
      # we are sneding email instead of username
      usr = User.objects.create_user(email,email,password)
      usr.first_name = name 
      usr.save()

      profile = Profile(user=usr,contact_number=contact)
      profile.save()
      context['status'] = f"User {name} Registration Successfull!"
      return render(request,'login.html')
    else:
      context['error'] = f"Registration is Not Successfull! A user with this username or email already exists!"
      # in register.html, i have created an API using AJAX to check if any user with the same email already exists

  return render(request,'register.html',context)





def check_user_exists(request):  
  email = request.GET.get('usern')
  check = User.objects.filter(username=email)
  if len(check) == 0:
    return JsonResponse({'status':0,'message':'Does Not Exists'})
  else:
    return JsonResponse({'status':1,'message':'A user with this email alredy exists!'})





def signin(request):
  
  context = {}

  # POST method is more secure than GET method as GET method stores the data in url only but POST method safely takes the data inside backend
  if request.method == "POST":
    email = request.POST.get('email')
    passw = request.POST.get('password')

    check_user = authenticate(username = email, password = passw)

    if check_user:
      login(request,check_user)
      # after login, either send the user to admin page OR dashboard OR show invalid login
      if check_user.is_superuser or check_user.is_staff:
        return HttpResponseRedirect('/admin/')
      return HttpResponseRedirect('/dashboard/')
    else:
      context.update({'message':'Invalid Login Credentials!','class':'alert-danger alert'})

  return render(request,'login.html',context)





def dashboard(request):
    context={}
    login_user = get_object_or_404(User, id = request.user.id) # will return some or the other id
    #fetch login user's details
    profile = Profile.objects.get(user__id=request.user.id)
    context['profile'] = profile

    #update profile
    if "update_profile" in request.POST:
        print("file=",request.FILES)
        name = request.POST.get('name')
        contact = request.POST.get('contact_number')
        add = request.POST.get('address')
       

        profile.user.first_name = name 
        profile.user.save()
        profile.contact_number = contact 
        profile.address = add 

        if "profile_pic" in request.FILES:
            pic = request.FILES['profile_pic']
            profile.profile_pic = pic
        profile.save()
        context['status'] = 'Profile Updated Successfully!'
    
    #Change Password 
    if "change_pass" in request.POST:
        c_password = request.POST.get('current_password')
        n_password = request.POST.get('new_password')

        check = login_user.check_password(c_password)
        if check==True:
            login_user.set_password(n_password)
            login_user.save()
            # automatically login the user again, bcz it will logout bcz of change in password
            login(request, login_user)
            context['status'] = 'Password Updated Successfully!' 
        else:
            context['status'] = 'Current Password Incorrect!'

    #My Orders 
    orders = Order.objects.filter(customer__user__id=request.user.id).order_by('-id')
    context['orders']=orders    
    return render(request, 'dashboard.html', context)





def user_logout(request):
  logout(request)
  return HttpResponseRedirect('/')





def single_dish(request, id):
  context={}
  dish = get_object_or_404(Dish, id=id)

  if request.user.is_authenticated:
    context.update({'dish':dish})
    

  return render(request,'dish.html', context)





def payment_done(request):
  pid = request.GET.get('PayerID')
  order_id = request.session.get('order_id')
  order_obj = Order.objects.get(id=order_id)
  order_obj.status=True 
  order_obj.payer_id = pid
  order_obj.save()
  
  return render(request, 'payment_successfull.html') 





def payment_cancel(request):
  ## remove comment to delete cancelled order
  # order_id = request.session.get('order_id')
  # Order.objects.get(id=order_id).delete()

  return render(request, 'payment_failed.html')



'''
def book_table(request):
    if request.method == 'POST':
        form = TableBookingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('booking_success')  # Redirect to a success page
    else:
        form = TableBookingForm()
    return render(request, 'your_template.html', {'form': form})
'''