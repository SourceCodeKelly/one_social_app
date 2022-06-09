from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # Restricts users from accessing others' data
from django.contrib import messages
from .forms import SignupForm, LoginForm, PostForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Post, Profile, Like
from django.contrib.auth.models import User

# Create your views here.

class Home(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        return context
    
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    
#################################

class Signup(View):
    form_class = SignupForm
    initial = {'key': 'value'}
    template_name = 'signup.html'
    
    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')
        # else process dispatch as it otherwise normally would
        return super(Signup, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')
        return render(request, self.template_name, {'form': form})
    
########################################################

class Login(LoginView):
    template_name = 'login.html'
    form_class = LoginForm
    authentication_form=LoginForm
    redirect_authenticated_user=True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)
            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
            
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(Login, self).form_valid(form)

########################################################
                                           
class ResetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')

########################################################
    
class ChangePassword(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

########################################################
    
@login_required
def profile_settings(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='profile_settings')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile_settings.html', {'user_form': user_form, 'profile_form': profile_form})

########################################################

@login_required(login_url='login')
def settings(request):
    return render(request, 'profile_settings.html')

#######################################################

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ('image', 'caption')
    template_name = 'upload.html'
    success_url = reverse_lazy('home')
    
    def upload(request):
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            user = request.user.username
            if form.is_valid():
                data = form.save(commit=False)
                data.user_name = user
                data.save()
                messages.success(request, f'Posted Successfully')
                return redirect('home')
        else:
            form = PostForm()
        return render(request, 'upload.html', {'form':form})
    
    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(PostCreate, self).form_valid(form)

####################################

@login_required(login_url='login')
def like_post(request):
    user = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id=post_id)
    like_filter = Like.objects.filter(post_id=post_id, user=user).first()
    
    if like_filter == None:
        new_like = Like.objects.create(post_id=post_id, user=user)
        new_like.save()
        post.no_of_likes = post.no_of_likes + 1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes - 1
        post.save()
        return redirect('/')
    
@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length            
    }
    return render(request, 'profile.html', context)