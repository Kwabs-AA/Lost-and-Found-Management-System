from django.shortcuts import render,redirect
from django.http import HttpResponse,request
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Lost

# Create your views here.

@login_required
def home(request):
    return render(request,'selection.html',{'name':request.user.first_name})

@login_required
def uploadview(request):
    return render(request,'upload.html')

@login_required
def findview(request):
    return render(request,'find.html')

def signup(request):
    if request.method =='POST':
        first_name =request.POST['firstname']
        last_name =request.POST['lastname']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email = request.POST['email']
        indexno = request.POST['indexno']
        username=request.POST['username']

        if password1 != password2:
            messages.error(request,"Passwords Do not match")
            return redirect('signup')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists")
            return redirect('signup')

        user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password1,email=email)
        user.save()
        messages.success(request, "You have successfully registered. Please enter the details in the right field to login")
        return redirect('login')
    else:
        return render(request,'signup.html',{})

def login_user(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Login unsuccessful")
            return redirect('login')
    else:
        return render(request,'registration/login.html')


def upload_file(request):
    if request.method == 'POST':
        category=request.POST.get('category')
        image=request.FILES.get('image')
        lostdesc=request.POST.get('lostdesc')
        indexNo=request.POST.get('lostindex')
        name=request.POST.get('name')
        location=request.POST.get('location')

        if category != 'ID':
            indexNo = 0 
            if name =="" or lostdesc=="":
                messages.error(request,"Please fill the all the boxes")
                return redirect(request.META['HTTP_REFERER'])
            else:
                lost=Lost(category=category,image=image,lostdesc=lostdesc,indexNo=indexNo,name=name,location=location)
                lost.save()
                return redirect('success')
        else:
            name="studentID"
            lostdesc="None"
            if indexNo=="":
                messages.error(request,"Please fill all the boxes")
                return redirect(request.META['HTTP_REFERER'])
            else:
                lost=Lost(category=category,image=image,lostdesc=lostdesc,indexNo=indexNo,name=name,location=location)
                lost.save()
                return redirect('success')            
    return render(request,'upload.html')

@login_required
def success(request):
    return render(request,'success.html',{"name":request.user.first_name})


def logout_view(request):
    logout(request)
    return redirect('login')

def search_file(request):
    if request.method == 'POST':
        category=request.POST.get('category')
        indexNo=request.POST.get('indexNo')
        name=request.POST.get('name')
        desc=request.POST.get('desc')

        temp=Lost.objects.all()
        if category != 'ID':
            if name =="" or desc=="":
                messages.error(request,"Please fill the all the boxes")
                return redirect(request.META['HTTP_REFERER'])
        else:
            if indexNo=="":
                messages.error(request,"Please enter an index number")
                return redirect(request.META['HTTP_REFERER'])
                
            

        if category:
            temp = temp.filter(category=category)
        if indexNo:
            temp = temp.filter(indexNo=indexNo)
        if name:
            temp = temp.filter(name__iexact=name)
        if desc:
            temp = temp.filter(lostdesc__icontains=desc)

        # If all filters are applied and no items found, return no items
        if not temp.exists():
            messages.info(request, "No items found matching the criteria")

        return render(request, 'display.html', {"items": temp})

    return redirect('find')

    
        