from re import template
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.Signup.as_view(), name='signup'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/profile-settings/', views.profile_settings, name='profile_settings'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('password-change/', views.ChangePassword.as_view(), name='password_change'),
    path('password-reset/', views.ResetPassword.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('', views.Home.as_view(), name="home"),
    path('upload/', views.PostCreate.as_view(), name='upload'),
    path('like-post/', views.like_post, name='like-post'),
    path('follow', views.follow, name='follow'),
]
