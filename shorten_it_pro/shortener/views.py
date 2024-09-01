
from django.shortcuts import render, HttpResponse, redirect,  get_object_or_404
from shortener import views
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.


from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'index.html')

def user_register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            u = User.objects.create(username=username, first_name=first_name, last_name=last_name, email=email)
            u.set_password(password)
            u.save()
            return redirect('/')
        else:
            context = {}
            context['error'] = "Password and Confirm Password do not match"
            return render(request, 'register.html', context)

def user_login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context = {}
            context['error'] = "Username and Password is incorrect"
            return render(request, 'login.html', context)
@login_required
def user_logout(request):
    logout(request)
    return redirect("/")


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import ShortenedURL, URLAnalytics
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
import string

# Utility function to generate a random shortcode
def generate_shortcode(length=6):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# View to create a new shortened URL
@login_required
def create_shortened_url(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if original_url:
            short_code = generate_shortcode()
            shortened_url = ShortenedURL.objects.create(
                original_url=original_url,
                short_code=short_code,
                created_by=request.user
            )
            return render(request, 'shortened_url.html', {'shortened_url': shortened_url})
    return render(request, 'create_shortened_url.html')

# Redirect view for shortened URL
def redirect_url(request, short_code):
    shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
    
    # Log URL access
    URLAnalytics.objects.create(
        shortened_url=shortened_url,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT')
    )
    
    return HttpResponseRedirect(shortened_url.original_url)

# View to display URL analytics
@login_required
def url_analytics(request):
    user_urls = ShortenedURL.objects.filter(created_by=request.user)
    analytics_data = []
    for url in user_urls:
        analytics = URLAnalytics.objects.filter(shortened_url=url)
        analytics_data.append({
            'url': url,
            'analytics': analytics
        })
    return render(request, 'url_analytics.html', {'analytics_data': analytics_data})

