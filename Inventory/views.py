from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Lost, Review, Badges
from django.db.models import Avg, Count, Sum
from collections import Counter

# Create your views here.

@login_required
def home(request):
    return render(request, 'temporary.html')

@login_required
def uploadview(request):
    return render(request, 'upload.html')

@login_required
def findview(request):
    return render(request, 'find.html')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        username = request.POST['username']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password1, email=email)
        user.save()
        messages.success(request, "You have successfully registered. Please enter the details in the right field to login")
        return redirect('login')
    else:
        return render(request, 'signup.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Login unsuccessful")
            return redirect('login')
    else:
        return render(request, 'registration/login.html')

@login_required
def upload_file(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        image = request.FILES.get('image')
        lostdesc = request.POST.get('lostdesc')
        indexNo = request.POST.get('lostindex')
        name = request.POST.get('name')
        location = request.POST.get('location')

        uploader_name = f"{request.user.first_name} {request.user.last_name}"
        badges = Badges.objects.filter(uploader_name=uploader_name).first()

        if not badges:
            badges = Badges.objects.create(uploader_name=uploader_name, count=0)

        if category != 'ID':
            indexNo = 0
            if not name or not lostdesc:
                messages.error(request, "Please fill all the boxes")
                return redirect(request.META['HTTP_REFERER'])
            else:
                lost = Lost(category=category, image=image, lostdesc=lostdesc, indexNo=indexNo, name=name, location=location, uploader_name=uploader_name)
                lost.save()
                badges.count += 1
                badges.save()
                return redirect('success')
        else:
            name = "studentID"
            lostdesc = "None"
            if not indexNo:
                messages.error(request, "Please fill all the boxes")
                return redirect(request.META['HTTP_REFERER'])
            else:
                lost = Lost(category=category, image=image, lostdesc=lostdesc, indexNo=indexNo, name=name, location=location, uploader_name=uploader_name)
                lost.save()
                badges.count += 1
                badges.save()
                return redirect('success')
    return render(request, 'upload.html')

@login_required
def success(request):
    return render(request, 'success.html', {"name": request.user.first_name})

def logout_view(request):
    logout(request)
    return redirect('login')

def search_file(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        indexNo = request.POST.get('indexNo')
        name = request.POST.get('name')
        desc = request.POST.get('desc')

        temp = Lost.objects.all()
        if category != 'ID':
            if not name or not desc:
                messages.error(request, "Please fill all the boxes")
                return redirect(request.META['HTTP_REFERER'])
        else:
            if not indexNo:
                messages.error(request, "Please enter an index number")
                return redirect(request.META['HTTP_REFERER'])

        if category:
            temp = temp.filter(category=category)
        if indexNo:
            temp = temp.filter(indexNo=indexNo)
        if name:
            temp = temp.filter(name__iexact=name)
        if desc:
            temp = temp.filter(lostdesc__icontains=desc)

        if not temp.exists():
            messages.info(request, "No items found matching the criteria")

        return render(request, 'display.html', {"items": temp})

    return redirect('find')

@login_required
def review(request, lost_item_id):
    lost_item = get_object_or_404(Lost, id=lost_item_id)

    if request.method == 'POST':
        review_text = request.POST.get('review_text')
        rating = request.POST.get('rating')

        if not review_text or not rating:
            messages.error(request, 'Please fill out all fields.')
        else:
            Review.objects.create(
                reviewer_name=request.user,
                lost_item=lost_item,
                rating=rating,
                review_text=review_text,
                uploader_name=lost_item.uploader_name
            )
            messages.success(request, 'Your review has been submitted successfully.')
            return redirect('review', lost_item_id=lost_item_id)

    reviews = Review.objects.filter(uploader_name=lost_item.uploader_name).order_by('-created_at')
    reviewers_badges = {}

    for review in reviews:
        badges = Badges.objects.filter(uploader_name=lost_item.uploader_name).first()
        if badges:
            badge_type = badges.get_badge_type()
            if badge_type:
                reviewers_badges[review.reviewer_name.username] = badge_type
            

    highest_badge_user = Badges.get_highest_count_user()

    context = {
        'lost_item': lost_item,
        'reviews': reviews,
        'reviewers_badges': reviewers_badges,
    }

    return render(request, 'Review.html', context)

def admin_view(request):
    total_lost_items = Lost.objects.count()
    category_counts = Lost.objects.values('category').annotate(count=Count('category')).order_by('-count')
    top_5_categories = category_counts[:5]
    
    # Location analysis
    location_counts = Lost.objects.values('location').annotate(count=Count('location')).order_by('-count')
    top_5_locations = location_counts[:5]
    
    # Review statistics
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(Avg('rating'))['rating__avg']
    rating_distribution = Review.objects.values('rating').annotate(count=Count('rating')).order_by('rating')
    
    # Badges statistics
    total_badges = Badges.objects.count()
    badge_distribution = Counter(Badges.objects.values_list('count', flat=True))
    badge_types = {
        'Trustworthy': Badges.objects.filter(count__gte=50).count(),
        'Reliable': Badges.objects.filter(count__gte=25, count__lt=50).count(),
        'Proven': Badges.objects.filter(count__gte=10, count__lt=25).count(),
        'No Badge': Badges.objects.filter(count__lt=10).count(),
    }
    
    # Top contributors
    top_contributors = Badges.objects.order_by('-count')[:10]
    
    context = {
        'total_lost_items': total_lost_items,
        'top_5_categories': top_5_categories,
        'top_5_locations': top_5_locations,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'rating_distribution': rating_distribution,
        'total_badges': total_badges,
        'badge_distribution': badge_distribution,
        'badge_types': badge_types,
        'top_contributors': top_contributors,
    }
    
    
    return render(request, 'admin.html', context)