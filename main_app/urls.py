from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.Home.as_view(), name="home"),
]
