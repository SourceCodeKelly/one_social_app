from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin # Restricts users from accessing others' data
from django.contrib.auth.forms import UserCreationForm # Creates a user automatically 
from django.contrib.auth import login
from django.contrib import messages
from .forms import SignupForm, LoginForm


# Create your views here.

class Home(TemplateView):
    template_name = "home.html"
    
#################################

class Signup(View):
    form_class = SignupForm
    initial = {'key': 'value'}
    template_name = 'signup.html'

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
                                           