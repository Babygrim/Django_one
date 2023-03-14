from django.db import models
import datetime

# Create your models here.
class search_engine_silpo(models.Model):
    search_request = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    product_volume = models.CharField(max_length=200)
    search_date = models.DateTimeField(default = datetime.datetime.now())
    product_image = models.CharField(max_length=300)
    
    class Meta:
        ordering = ['-search_date']
    
    def __str__(self):
        return self.shop_name
    
class search_engine_metro(models.Model):
    search_request = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    product_volume = models.CharField(max_length=200)
    search_date = models.DateTimeField(default = datetime.datetime.now())
    product_image = models.CharField(max_length=300)
    
    class Meta:
        ordering = ['-search_date']
    
    def __str__(self):
        return self.shop_name
    
class search_engine_atb(models.Model):
    search_request = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    product_price = models.CharField(max_length=200)
    search_date = models.DateTimeField(default = datetime.datetime.now())
    product_image = models.CharField(max_length=300)
    
    class Meta:
        ordering = ['-search_date']
    
    def __str__(self):
        return self.shop_name
    
