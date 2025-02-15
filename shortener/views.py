from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import URL
import random
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


def home(request):
    return render(request, 'home.html')
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')

def dashboard(request):
    urls = URL.objects.filter(user=request.user).order_by('-added_time')
    return render(request, 'dashboard.html', {'urls': urls})

def add_url(request):
    if request.method == 'POST':
        if URL.objects.filter(user=request.user).count() >= 5:
            return render(request, 'dashboard.html', {'error': 'You can only add up to 5 URLs'})
        
        title = request.POST.get('title')
        original_url = request.POST.get('original_url')
        short_url = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6))
        URL.objects.create(user=request.user, title=title, original_url=original_url, short_url=short_url)
        return redirect('dashboard')
    return redirect('dashboard')



def dashboard(request):
    urls_list = URL.objects.filter(user=request.user).order_by('-added_time')
    paginator = Paginator(urls_list, 1)  # Show 5 items per page
    page_number = request.GET.get('page')
    urls = paginator.get_page(page_number)
    
    return render(request, 'dashboard.html', {'urls': urls, 'paginator': paginator})



def search(request):
    query = request.GET.get('query', '')
    urls = URL.objects.filter(user=request.user, title__icontains=query).values('title', 'short_url', 'added_time')
    return JsonResponse({'urls': list(urls)})



def delete_url(request, id):
    url = get_object_or_404(URL, id=id, user=request.user)
    url.delete()
    return redirect('dashboard')


def edit_url(request, id):
    url = get_object_or_404(URL, id=id, user=request.user)
    if request.method == "POST":
        url.title = request.POST.get('title')
        url.original_url = request.POST.get('original_url')
        url.save()
        return redirect('dashboard')
    return render(request, 'edit_url.html', {'url': url})

def redirect_to_url(request, short_url):
    # Find the URL object using the short_url field
    url = get_object_or_404(URL, short_url=short_url)
    
    # Redirect to the original URL
    return redirect(url.original_url)
