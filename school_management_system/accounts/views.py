from django.urls import reverse_lazy
from django.views import generic, View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegistrationForm, UserDetailUpdateForm, PasswordChangeForm
from django.contrib import messages
from .models import User
from django.shortcuts import render, redirect

# Create your views here.

class UserRegistrationView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('register')

    def form_valid(self, form):
        messages.success(self.request, 'Account has been created successfully!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'There was an error with registration. Please try again.')
        return super().form_invalid(form)
    
class UserDetailUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailUpdateForm
    template_name = 'user_detail_update.html'
    success_url = reverse_lazy('user-detail-update')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Your details have been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
    
class UserLoginView(LoginView):
    template_name = 'login.html'

class PasswordChangeView(LoginRequiredMixin, View):
    template_name = 'user_password_change.html'

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Your password has been changed successfully.")
            return redirect(reverse_lazy('user-detail-update'))
        return render(request, self.template_name, {'form': form})