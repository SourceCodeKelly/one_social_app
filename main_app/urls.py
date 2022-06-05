from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('signup/', views.Signup.as_view(), name='signup')
]