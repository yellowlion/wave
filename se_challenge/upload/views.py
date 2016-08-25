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

def handle_uploaded_file(f):
    
    csvreader = csv.reader(f)

    # This skips the first row of the CSV file.
    # csvreader.next() also works in Python 2.
    next(csvreader)

    for row in csvreader:
        # do stuff with rows...
        print row
        
        employee_name = [i.strip() for i in row[2].split()]  # employee name
        first_name = employee_name[0]
        last_name = employee_name[1]
        address = row[3]
        
        
        
        obj, created = Employee.objects.update_or_create(first_name=first_name, last_name=last_name, address=address)
        
    """
    with open('88888.txt', 'wb') as destination:
        for chunk in f.chunks():
            print '===================================='
            print chunk
            print '===================================='

            destination.write(chunk)
    """
            
def upload_file(request):
    print 'hellow'
    if request.method == 'POST':
        print 1
        form = UploadFileForm(request.POST, request.FILES)
        print 2
        if form.is_valid():
            print 3
            print request.FILES['file']
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})
