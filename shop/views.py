from django.shortcuts import render,redirect
from django.http import HttpResponse
from .product import Product
from .category import Category
from .customer import Customer
from django.contrib.auth.hashers import make_password,check_password


# Create your views here.

def home(request):
    category=Category.objects.all()
    categoryID=request.GET.get('category')
    if categoryID:
        products=Product.get_category_id(categoryID)
    else:
        products=Product.objects.all()
    data={'products':products,'categories':category}
    return render(request,'index.html',data)

def signup(request):
    if request.method == 'GET':

        return render(request,"signup.html")
    else:
        fn=request.POST['fn']
        ln=request.POST['ln']
        email=request.POST['email']
        mobile=request.POST['mobile']
        password=request.POST['password']
        userdata=[fn,ln,email,mobile,password]
        print(userdata)
        uservalues={
            'fn':fn,
            'ln':ln,
            'email':email,
            'mobile':mobile
        }
        # storing object
        Customerdata=Customer(first_name=fn,last_name=ln,email=email,mobile=mobile,password=password)
        error_msg=None
        success_msg=None
        if(not fn):
            error_msg="First name should not be empty"
        elif(not ln):
            error_msg="Last name should not be empty"
        elif(not email):
            error_msg="Email should not be empty"
        elif(not mobile):
            error_msg="mobile should not be empty"
        elif(not password):
            error_msg="password should not be empty"
        elif(Customerdata.isexit()):
            error_msg="Email Already Exists"
        if(not error_msg):
            Customerdata.password=make_password(Customerdata.password)
            success_msg="Account Created Successfully"
            Customerdata.save()
            msg={'success':success_msg}
            return render(request,'signup.html',msg)
        else:
            msg={'error':error_msg,'value':uservalues}
            return render(request,'signup.html',msg)
        
#login page
def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        email=request.POST['email']
        password=request.POST['password']
        users=Customer.getemail(email)
        error_msg=None
        if users:
            check=check_password(password,users.password)
            if check:
                return redirect('/')
            else:
                error_msg="Password is incorrect"
                msg={'error':error_msg}
                return render(request,'login.html',msg)
        else:
            error_msg="email is incorrect"
            msg={'error':error_msg}
            return render(request,'login.html',msg)
        