from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Lost,Review

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
            return redirect('temp')
        else:
            messages.error(request,"Login unsuccessful")
            return redirect('login')
    else:
        return render(request,'registration/login.html')

@login_required
def upload_file(request):
    if request.method == 'POST':
        category=request.POST.get('category')
        image=request.FILES.get('image')
        lostdesc=request.POST.get('lostdesc')
        indexNo=request.POST.get('lostindex')
        name=request.POST.get('name')
        location=request.POST.get('location')
        
        uploader_name= f"{request.user.first_name} {request.user.last_name}"

        if category != 'ID':
            indexNo = 0 
            if name =="" or lostdesc=="":
                messages.error(request,"Please fill the all the boxes")
                return redirect(request.META['HTTP_REFERER'])
            else:
                lost=Lost(category=category,image=image,lostdesc=lostdesc,indexNo=indexNo,name=name,location=location,uploader_name=uploader_name)
                lost.save()
                return redirect('success')
        else:
            name="studentID"
            lostdesc="None"
            if indexNo=="":
                messages.error(request,"Please fill all the boxes")
                return redirect(request.META['HTTP_REFERER'])
            else:
                lost=Lost(category=category,image=image,lostdesc=lostdesc,indexNo=indexNo,name=name,location=location,uploader_name=uploader_name)
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

@login_required
def review(request,lost_item_id):
    lost_item = get_object_or_404(Lost, id=lost_item_id)

    reviewer_name = request.user
    uploader_name=lost_item.uploader_name

    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        if not review_text or not rating:
            messages.error(request, 'Please fill out all fields.')
        else:
            Review.objects.create(
                reviewer_name=reviewer_name,
                lost_item=lost_item,
                rating=rating,
                review_text=review_text,
                uploader_name=uploader_name
            )
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('review', lost_item_id=lost_item_id)
            

    reviews = Review.objects.filter(uploader_name=uploader_name)

    return render(request, 'review.html', {'lost_item': lost_item,'reviews': reviews,})        

def temporary(request):
    return render(request,'temporary.html')

def alt1(request):
    return render(request,'alt1.html')