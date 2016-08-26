#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm


from .models import Employee
from .models import ExpenseItem

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
import csv
from datetime import date

from django.db.models import Count
from django.db.models import F, FloatField, Sum

import calendar

def handle_uploaded_file(f):
    
    csvreader = csv.reader(f)

    # This skips the first row (i.e. header) of the CSV file.
    next(csvreader)

    for row in csvreader:
        # do stuff with each row...
        
        # expense part
        """
>>> import hashlib
>>> m = hashlib.md5()
>>> m.update("Nobody inspects")
>>> m.update(" the spammish repetition")
>>> m.digest()
'\xbbd\x9c\x83\xdd\x1e\xa5\xc9\xd9\xde\xc9\xa1\x8d\xf0\xff\xe9'
>>> m.digest_size
16
>>> m.block_size        
        
        """
        row = [i.strip() for i in row]
        
        # expense part
        expense_date = row[0].split('/')
        year = int(expense_date[2])
        month = int(expense_date[0])
        day = int(expense_date[1])
        
        category = row[1]
        description = row[4]
        pre_tax_amount = int(float(row[5].replace(',', '')) * 100)
        tax_name = row[6]
        tax_amount = int(float(row[7].replace(',', '')) * 100)
        total_amount = int(pre_tax_amount + tax_amount)
        
        print 'pre_tax_amount: ', pre_tax_amount
        print 'tax_amount: ', tax_amount
        print 'total_amount: ', total_amount
        
        # employee part
        employee_name = [i.strip() for i in row[2].split()]
        first_name = employee_name[0]
        last_name = employee_name[1]
        address = row[3]
            
        employee, created = Employee.objects.update_or_create(first_name=first_name, last_name=last_name, address=address)
        
        expense, created = ExpenseItem.objects.get_or_create(date=date(year, month, day), category=category, description=description, 
                                pre_tax_amount=pre_tax_amount, tax_name=tax_name, tax_amount=tax_amount, total_amount=total_amount, employee=employee)
                                
        if created:
            print employee_name
            print expense

        """
        with open('88888.txt', 'wb') as destination:
            for chunk in f.chunks():
                print '===================================='
                print chunk
                print '===================================='

                destination.write(chunk)
        """
class Node:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
            
def upload_file(request):
    data = []
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            
            query_set = ExpenseItem.objects.all()
            #print query_set
            #print 'len qs: ', len(query_set)
            years = query_set.dates('date','year')          
            for year in years:
                year_dict = {}
                print 'year.year: ', year.year
                year_dict['year'] = year.year
                month_data = []
                month_dict = {}
                #month_dict[]
                
                months = query_set.filter(date__year=year.year).dates('date','month')
                #print 'months: ', months
                #print 'qs : ', query_set
                for month in months:
                    a = query_set.filter(date__year=year.year).filter(date__month=month.month).aggregate(total_expenses_amount=Sum(F('total_amount'), output_field=FloatField()))
                    b = "%0.2f" % (a['total_expenses_amount']/100)
                    print 'Month: Total', calendar.month_name[month.month], b
                    

            
 
    else:
        form = UploadFileForm()
        
    l = [{'year':1998, 'data':[{'month':'January', 'sum':3.99}]}, {'year':2005, 'data':[{'month':'January', 'sum':53.99}]}, {'year':2010, 'data':[{'month':'FJanuary', 'sum':3.99}]}]
    
    
    return render(request, 'upload.html', {'form': form, 'll':l})
