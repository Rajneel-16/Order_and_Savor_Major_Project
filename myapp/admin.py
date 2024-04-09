'''from django.contrib import admin
from myapp.models import Contact

# Register your models here.
admin.site.site_header = "Rajneel's Spice | Rajneel Wagh"

# this is for showing all the data in tabular form in Django administration
class ContactAdmin(admin.ModelAdmin):
  list_display = ['id','name','email','subject','added_on','is_approved']

admin.site.register(Contact, ContactAdmin) '''

from django.contrib import admin
from myapp.models import Contact, Category, Team, Dish, Profile,Order,TableBooking

admin.site.site_header = "Order & Savor | Project by Rajneel Wagh"
admin.site.register(TableBooking)

class ContactAdmin(admin.ModelAdmin):
    list_display = ['id','name','email','subject','added_on','is_approved']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on','updated_on']

class TeamAdmin(admin.ModelAdmin):
    list_display = ['id','name','added_on','updated_on']

class DishAdmin(admin.ModelAdmin):
    list_display = ['id','name','price','added_on','updated_on']


admin.site.register(Contact, ContactAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Team, TeamAdmin )
admin.site.register(Dish, DishAdmin )
admin.site.register(Profile)
admin.site.register(Order)