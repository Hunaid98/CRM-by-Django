from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank= True, on_delete=models.CASCADE)
    name = models.CharField(null = True, max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    profile_pic = models.ImageField(default = "profile1.pngs", null=True, blank = True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(null = True, max_length=200)
    

    def __str__(self):
        return self.name

class Products(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('out door', 'out door'),
        
    )
    name = models.CharField(null=True, max_length=200)
    price = models.FloatField(null=True)
    category = models.CharField(null=True, max_length=200,choices= CATEGORY)
    description = models.CharField(null=True, max_length=500,blank=True)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    Tags = models.ManyToManyField(Tag)


    def __str__(self):
        return self.name







class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('out of delivery', 'out of delivery'),
        ('Delivered','Delivered'),
    )
    customer = models.ForeignKey(Customer, null= True, on_delete= models.SET_NULL)
    product = models.ForeignKey(Products, null= True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True,null=True)
    status = models.CharField(null = True, max_length=50,choices= STATUS)
    note = models.CharField(null = True, max_length=50)


    def __str__(self):
        return self.product.name
    
    