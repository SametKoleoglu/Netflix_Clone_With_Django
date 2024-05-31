from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signIn', views.sign_in, name='sign_in'),
    path('signUp', views.sign_up, name='sign_up'),
    path('signOut', views.sign_out, name='sign_out'),
    path('addToList', views.add_to_list, name='add-to-list'),
    path('movie/<str:pk>/', views.movie, name='movie'),
    path('my-list', views.my_list, name='my-list'),
    path('search', views.search, name='search'),
    path('genre/<str:pk>/', views.genre, name='genre'),
]
