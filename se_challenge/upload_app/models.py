# Ian Carreon, iancrrn@gmail.com

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Employee(models.Model):
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    street = models.CharField(max_length=90)
    zipcode = models.ForeignKey('ZipCode')

    class Meta:
        unique_together = ("first_name", "last_name", "street")
                
class ZipCode(models.Model):
    zipcode = models.CharField(max_length=10, primary_key = True) # Make this the PK since zipcodes are unique
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    
class TaxName(models.Model):
    tax_name = models.CharField(max_length=30)

class Category(models.Model):
    name = models.CharField(max_length=30)
    
class Expense(models.Model):
    date = models.DateField()    
    description = models.CharField(max_length=90)
    
    pre_tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    tax_name = models.ForeignKey(TaxName)
    category = models.ForeignKey(Category)
    employee = models.ForeignKey(Employee) #, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("date", "category", "description", "pre_tax_amount", "employee")
    
class Hobby(models.Model):
    employee = models.ForeignKey(Employee) #, on_delete=models.CASCADE)
