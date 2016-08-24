from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    address = models.CharField(max_length=255)
    
    def __str__(self):              # __unicode__ on Python 2
        return "%s %s" % (self.first_name, self.last_name)

class Expense(models.Model):
    date = models.DateField()
    category = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    pre_tax_amount = models.DecimalField(max_digits=5, decimal_places=2)
    tax_name = models.CharField(max_length=30) 
    tax_amount = models.DecimalField(max_digits=5, decimal_places=2)
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):              # __unicode__ on Python 2
        #return self.description
        return "%s %s - %s" % (self.date, self.description, self.employee)

