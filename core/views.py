from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import re
from django.shortcuts import get_object_or_404


@login_required(login_url='sign_in')
def index(request):
    movies = Movie.objects.all()
    featured_movie = movies[len(movies) - 1]

    context = {
        'movies': movies,
        'featured_movie': featured_movie
    }
    
    return render(request, 'index.html', context)


def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if username and email and password and password2:
            if password == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username already exists')
                    return redirect('sign_up')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email already exists')
                    return redirect('sign_up')
                else:
                    user = User.objects.create_user(
                        username=username, email=email, password=password)
                    user.save()
                    messages.success(request, 'Account created successfully')
                    return redirect('sign_in')
            elif password != password2:
                messages.error(request, 'Passwords do not match')
                return redirect('sign_up')
        else:
            messages.error(request, 'Please fill in all fields')
            return redirect('sign_up')

    return render(request, 'sign_up.html')


def sign_in(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.success(request, 'Logged in successfully')
                return redirect('index')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('sign_in')
        else:
            messages.error(request, 'Please fill in all fields')
            return redirect('sign_in')

    return render(request, 'sign_in.html')


@login_required(login_url='sign_in')
def sign_out(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('sign_in')


@login_required(login_url='sign_in')
def movie(request, pk):
    movie = Movie.objects.get(uu_id=pk)

    context = {
        'movie': movie
    }

    return render(request, 'movie.html', context)


@login_required(login_url='sign_in')
def add_to_list(request):
    if request.method == 'POST':
        movie_url_id = request.POST.get('movie_id')
        uuid_pattern = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        match = re.search(uuid_pattern, movie_url_id)
        movie_id = match.group() if match else None
        
        movie = get_object_or_404(Movie, uu_id=movie_id)
        movie_list,created = MovieList.objects.get_or_create(owner_user=request.user, movie=movie)
        
        if created:
            response_data = {
                'status':'success',
                'message':'Movie added ☺'
            }
        else:
            response_data = {
                'status':'info',
                'message':'Movie already in list'
            }
            
        return JsonResponse(response_data)
    
    else:
        return JsonResponse({
            'status':'error',
            'message':'Invalid request'
        },status=400)



@login_required(login_url='sign_in')
def my_list(request):
    movie_list = MovieList.objects.filter(owner_user=request.user)
    user_movie_list = []
    
    for movie in movie_list:
        user_movie_list.append(movie.movie)
        
    context = {
        'movies': user_movie_list
    }
    
    return render(request, 'me_list.html',context)


@login_required(login_url='sign_in')
def search(request):
    
    if request.method == "POST":
        search_term = request.POST.get('search_term')
        movies = Movie.objects.filter(title__icontains=search_term)
        
        context = {
            'movies': movies,
            'search_term': search_term
        }
        return render(request, 'search.html',context)
    
    else:
        return redirect('/')
        
        
@login_required(login_url='sign_in')        
def genre(request,pk):
    movie_genre = pk
    movies = Movie.objects.filter(genre=movie_genre)
    
    context = {
        'movies': movies,
        'movie_genre': movie_genre
    }
    
    return render(request, 'genre.html',context)
