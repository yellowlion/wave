# Ian Carreon, iancrrn@gmail.com
# August 27, 2016

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

# from .models import <model_name>
# Employee
# Expense
# ZipCode
# TaxName
# Hobby
# Category

from .models import *

import csv
import StringIO

from datetime import date

from django.db.models import Count
from django.db.models import F, FloatField, Sum

import calendar

def handle_uploaded_file(f):

    # http://stackoverflow.com/questions/3305926/python-csv-string-to-array
    header_read = False
    
    for chunk in f.chunks():
        
        f = StringIO.StringIO(chunk)
        csvreader = csv.reader(f)

        # This skips the first row (i.e. header) of the CSV file.
        if not header_read:
            next(csvreader)
            header_read = True

        for row in csvreader:
            # do stuff with each row...
            
            # remove any whitespace
            #print 'row: ', row
            
            row = [i.strip() for i in row]

            print 'row: ', row
            

            # Extract the expense item part
            expense_date = row[0].split('/') # extract year, month, day
            year = int(expense_date[2])
            month = int(expense_date[0])
            day = int(expense_date[1])
            
            category = row[1]
            print 'category: ', category
            description = row[4]
            
            # work with integers - avoid issues working with floats
            # convert to cents (i.e. multiply by 100)
            pre_tax_amount = int(float(row[5].replace(',', '')) * 100)
            tax_name = row[6]
            tax_amount = int(float(row[7].replace(',', '')) * 100)
            total_amount = int(pre_tax_amount + tax_amount)
                    
            # Extract employee part
            employee_name = [i.strip() for i in row[2].split()]
            first_name = employee_name[0]
            last_name = employee_name[1]
            
            # break up address into street, city, state and zipcode
            # e.g. 1600 Amphitheatre Parkway, Mountain View, CA 94043
            address = row[3].split(',')
            
            street = address[0].strip()
            city = address[1].strip()
            state_and_zipcode = address[2].strip()
            
            temp = state_and_zipcode.split(' ')
            state = temp[0].strip()
            zipcode = temp[1].strip()
        
            zipcode_obj, created = ZipCode.objects.get_or_create(zipcode=zipcode, city=city, state=state)
            employee_obj, created = Employee.objects.get_or_create(first_name=first_name, last_name=last_name, street=street, zipcode=zipcode_obj)
            category_obj, created = Category.objects.get_or_create(name=category)
            taxname_obj, created = TaxName.objects.get_or_create(tax_name=tax_name)
            expense_obj, created = Expense.objects.get_or_create(date=date(year, month, day), category=category_obj, description=description, 
                                    pre_tax_amount=pre_tax_amount, tax_name=taxname_obj, tax_amount=tax_amount, total_amount=total_amount, employee=employee_obj)
            

            
def upload_file(request):
    
    # used for the data to return to the template
    data = []
    
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            
            try:
                handle_uploaded_file(request.FILES['file'])                
            # catch all for now
            # but depending on the error we can bow out gracefully or continue
            # i.e if exception is an IntegrityError then continue...
            # i.e if list index out of range error then stop - possibly invalid CSV file
            except Exception as e: 
                return render(request, 'upload.html', {'form': form, 'data':data, 'error_msg':e})
                
        
            # This section builds the data to return to the template as a list of 'JSON' style/dicts objects
            """
            E.g. something like
            data = [{'year':1998, 'month_list':[{'month':'January', 'total':2.89}]}, 
                    {'year':2005, 'month_list':[{'month':'October', 'total':53.99}]}, 
                    {'year':2010, 'month_list':[{'month':'March', 'total':3.99}]}]
            """
            
            # hit the database once
            query_set = Expense.objects.all()
            
            # get all distinct years
            years = query_set.dates('date','year')
            
            # option to sort years ASC or DESC...
            
            # Group by year
            for year in years:
                year_dict = {}
                
                year_dict['year'] = year.year
                
                month_list = []
                
                # Get the months for this year
                months = query_set.filter(date__year=year.year).dates('date','month')
                for month in months:
                    
                    month_dict = {}
                    
                    # build each month dict
                    month_dict['month'] = calendar.month_name[month.month]
                    result = query_set.filter(date__year=year.year).filter(date__month=month.month).filter(category__name='Travel').aggregate(total_expenses_amount=Sum(F('total_amount'), output_field=FloatField()))
                    
                    month_dict['total'] = '%0.2f' % (result['total_expenses_amount']/100) # divide by 100 -> dollar and cents format
                    
                    # then add month dict to month list
                    month_list.append(month_dict)
                    
                year_dict['month_list'] = month_list
                 
                data.append(year_dict)   
    else:
        form = UploadFileForm()
        
    return render(request, 'upload.html', {'form': form, 'data':data, 'error_msg':None})
