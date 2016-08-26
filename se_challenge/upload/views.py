#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm


from .models import Employee
from .models import Expense

# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
import csv
from datetime import date

from django.db.models import Count
from django.db.models import F, FloatField, Sum

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
        
        # expense part
        expense_date = row[0].split('/')
        year = int(expense_date[2])
        month = int(expense_date[0])
        day = int(expense_date[1])
        
        category = row[1]
        description = row[4]
        pre_tax_amount = float(row[5].replace(',', ''))
        tax_name = row[6]
        tax_amount = float(row[7].replace(',', ''))
        
        # employee part
        employee_name = [i.strip() for i in row[2].split()]
        first_name = employee_name[0]
        last_name = employee_name[1]
        address = row[3]
            
        employee, created = Employee.objects.get_or_create(first_name=first_name, last_name=last_name, address=address)
        
        # Add this expense to this employee's expense set, i.e. One-to-Many
        # Assumption: expenses are unique
        employee.expense_set.create(date=date(year, month, day), category=category, description=description, 
                                pre_tax_amount=pre_tax_amount, tax_name=tax_name, tax_amount=tax_amount)

        #print employee.expense_set()                   
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
            
            query_set = Expense.objects.all()
            print query_set
            print 'len qs: ', len(query_set)
            years = query_set.dates('date','year')          
            for year in years:
                year_dict = {}
                #print 'year.year: ', year.year
                year_dict['year'] = year.year
                month_data = []
                month_dict = {}
                #month_dict[]
                
                months = query_set.filter(date__year=year.year).dates('date','month')
                print 'months: ', months
                #print 'qs : ', query_set
                for month in months:
                    a = query_set.filter(date__year=year.year).filter(date__month=month.month)#.aggregate(total_expenses_amount=Sum(F('pre_tax_amount'), output_field=FloatField()))
                    #print '====> a', a
                    

            
            """
            years = Expense.objects.dates('date','year')    
            print years[0].year
            print years[1].year
            
            a = Node(1,2)
            b = Node(3,4)
            
            
            l.append(a)
            l.append(b)
            """
            """
query_set = Post.objects.all()
    years = query_set.dates("pub_date","year")
    date_hierarchy = {}
    for year in years:
        date_hierarchy[year] = {}
        months = query_set.filter(pub_date__year=year.year).dates("pub_date","month")
        for month in months:
            date_hierarchy[year][month] = query_set.filter(pub_date__year=month.year,pub_date__month=month.month).count()            
            
            """
            
            """
            
            Post.objects.raw("SELECT DATE_FORMAT(pub_date, "%Y %M") as pub_date, 
COUNT(*) as count FROM app_posts GROUP BY pub_date ORDER BY count 
DESC")
            from django.db.models.functions import TruncMonth
            
            qs = Expense.objects.annotate(month=TruncMonth('date')).values('month').annotate(c=Sum('pre_tax_amount')).values('month', 'c')    
            
            print qs
            
            summary = (Expense.objects.annotate(m=TruncMonth('date')).values('m')) #.annotate(total=Sum('pre_tax_amount')).order_by())
            print 'summary: ', summary
            
            months = query_set.filter(pub_date__year=year.year).dates("pub_date","month")
            
            
            Bike.objects.filter(date__year = 2014).values('paint_color')
  .annotate(total=Count('paint_color'))
  .order_by('paint_color'))
            #from django.db import connection

            #truncate_month = connection.ops.date_trunc_sql('month','day')
            #qs = Expense.objects.extra({'month': truncate_month}).values('month').annotate(Count('pre_tax_amount'))            #print qs
            #print qs
            expenses = Expense.objects.all().values()
            """
            
            #print expenses
            #return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
        
    l = [{'year':1998, 'data':[{'month':'January', 'sum':3.99}]}, {'year':2005, 'data':[{'month':'January', 'sum':53.99}]}, {'year':2010, 'data':[{'month':'FJanuary', 'sum':3.99}]}]
    return render(request, 'upload.html', {'form': form, 'll':l})
