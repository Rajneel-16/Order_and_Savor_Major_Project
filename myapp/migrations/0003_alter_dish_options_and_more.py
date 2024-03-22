# Generated by Django 5.0 on 2024-01-20 12:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_category_team_dish_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dish',
            options={'verbose_name_plural': 'Dish Table'},
        ),
        migrations.RenameField(
            model_name='dish',
            old_name='description',
            new_name='ingredients',
        ),
        migrations.AddField(
            model_name='category',
            name='added_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.CharField(default='Your default description', max_length=255),
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='default_category_images/'),
        ),
        migrations.AddField(
            model_name='category',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='added_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='dish',
            name='details',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='discounted_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='dish',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='default_dish_images/'),
        ),
        migrations.AddField(
            model_name='dish',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='dish',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profiles/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='profile',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='team',
            name='added_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='team',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='dish',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='contact_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='team',
            name='designation',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='team',
            name='image',
            field=models.ImageField(upload_to='team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('invoice_id', models.CharField(blank=True, max_length=100)),
                ('payer_id', models.CharField(blank=True, max_length=100)),
                ('ordered_on', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.profile')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.dish')),
            ],
            options={
                'verbose_name_plural': 'Order Table',
            },
        ),
    ]
