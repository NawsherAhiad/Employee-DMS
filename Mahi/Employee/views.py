from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from Employee.models import Employee
import os
from django.db import connection
from django.contrib import messages
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models import Q
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    #return HttpResponse("This is Employees site")
    #return render(request, 'index.html')
    person =[
        {'name':"Ahiad", 'age': "26"},
        {'name':"Mahi", 'age': "27"}
    ]
    return render(request, 'index.html', context= {'person': person})

def search_employees(name='', date_of_birth='', email='', mobile=''):
   
    query = Q()

    if name:
        query &= Q(first_name__icontains=name) | Q(last_name__icontains=name)
    if date_of_birth:
        query &= Q(date_of_birth=date_of_birth)
    if email:
        query &= Q(email__icontains=email)
    if mobile:
        query &= Q(mobile__exact=mobile)
    
    
    employees = Employee.objects.filter(query)
    
    return employees


def read(request):
    obj_e = Employee.objects.all() 
    search = request.GET

    #print(search)
    if search:
        name = request.GET.get('name', '')
        date_of_birth = request.GET.get('date_of_birth', '')
        email = request.GET.get('email', '')
        mobile = request.GET.get('mobile', '')
        obj_e = search_employees(name, date_of_birth, email, mobile)
        
    paginator = Paginator(obj_e, 10)  # Show 10 employees per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
               
    return render(request, 'display.html', context = {'emp': page_obj , 'search': request.GET})





def resize_image(image, max_width=300, max_height=300):
    img = Image.open(image)

    # Maintain aspect ratio
    width_ratio = max_width / img.width
    height_ratio = max_height / img.height
    resize_ratio = min(width_ratio, height_ratio)
    new_width = int(img.width * resize_ratio)
    new_height = int(img.height * resize_ratio)

    # Resize the image using LANCZOS (high-quality resampling filter)
    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    # Determine image format and set default if necessary
    format = image.content_type.split('/')[1].upper()  # Extract format from MIME type
    if format not in ['JPEG', 'PNG', 'GIF', 'BMP']:
        format = 'JPEG'  # Default to JPEG if format is not recognized

    # Save the resized image to a BytesIO object
    img_io = BytesIO()
    img.save(img_io, format=format)

    # Use InMemoryUploadedFile to recreate the image file for Django to handle
    resized_image = InMemoryUploadedFile(
        img_io,       # file
        None,         # field_name
        image.name,   # file name
        image.content_type,  # MIME type
        img_io.tell(),  # size
        None          # content_type_extra
    )

    return resized_image








def add_employee(request):
    if request.method == 'POST':
        data = request.POST
        f_name = data.get('first_name')
        l_name = data.get('last_name')
        email = data.get('email')
        mobile = data.get("mobile")
        dob = data.get('date_of_birth')
        photo = request.FILES.get('profile_picture')
        
        if photo:
            photo = resize_image(photo)
            
        Employee.objects.create(
            first_name = f_name,
            last_name = l_name,
            email = email,
            mobile = mobile,
            date_of_birth = dob,
            profile_picture = photo
      
        )
        messages.success(request, "Record is Updated!")
        # with connection.cursor() as cursor:
        #     cursor.execute("""
        #                 insert into Employee_employee values (%s, %s, %s, %s, %s, %s)
        #                 """, 
        #                 [f_name, l_name, email, mobile, dob, photo]
        #                 )
        #     row = cursor.fetchone()
        #     cursor.close()
        #     #print(row) 
        #return redirect('add_employee/')
    
    messages.success(request, "Record Not Updated!")
    
    return render(request, 'add_employee.html')


def delete_employee(request, id):
    # quereyset = Employee.objects.get(id = id)
    # quereyset.delete()
    delete = connection.cursor()
    delete.execute("delete from Employee_employee where id =%s", [id])
    return redirect("/display/")


def edit_employee(request, id):
    employee = get_object_or_404(Employee, id=id)
    context = {'employee': employee}
    return render(request, "edit_employee.html", context)
    
def update_employee(request, id):
    emp = Employee.objects.get(id=id)
    
    if request.method == "POST":
        data = request.POST
        f_name = data.get('first_name')
        l_name = data.get('last_name')
        email = data.get('email')
        mobile = data.get("mobile")
        dob = data.get('date_of_birth')
        photo = request.FILES.get('profile_picture')

        update = connection.cursor()
        update.execute(
            "UPDATE Employee_employee SET first_name = %s, last_name = %s, email = %s, mobile = %s, date_of_birth = %s WHERE id = %s",
            [f_name, l_name, email, mobile, dob, id]
        )
        
        if photo:
            emp.profile_picture = photo
            emp.save()

        return redirect("/display/")

    messages.success(request, "Record Not Updated!")
    return render(request, 'display.html')
   