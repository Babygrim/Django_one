from django.db import models
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

# Create your models here.
class search_engine_silpo(models.Model):
    search_request = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    search_date = models.DateTimeField(default = datetime.date.today())
    product_image = models.CharField(max_length=300)
    
    def serialize(self):
        return {
            "id":self.id,
            "search_request": self.search_request,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "search_date": self.search_date,
            "product_image": self.product_image,
        }
        
    class Meta:
        ordering = ['-search_date']
    
    
class search_engine_glove(models.Model):
    search_request = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    search_date = models.DateTimeField(default = datetime.date.today())
    product_image = models.CharField(max_length=300)
    
    def serialize(self):
        return {
            "id":self.id,
            "search_request": self.search_request,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "search_date": self.search_date,
            "product_image": self.product_image,
        }
        
    class Meta:
        ordering = ['-search_date']
    

    
class search_engine_atb(models.Model):
    search_request = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    search_date = models.DateTimeField(default = datetime.date.today())
    product_image = models.CharField(max_length=300)
    
    def serialize(self):
        return {
            "id":self.id,
            "search_request": self.search_request,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "search_date": self.search_date,
            "product_image": self.product_image,
        }
        
    class Meta:
        ordering = ['-search_date']
     
        
        

class wishlist(models.Model):
    user = models.IntegerField()
    product_id = models.IntegerField()
    shop = models.CharField(max_length=255)
    quantity = models.CharField(max_length=255)
    
    
