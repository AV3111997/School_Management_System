from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from accounts.forms import UserDetailUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

class UserListView(ListView):
    model = User
    template_name = "users-list.html"
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        queryset = User.objects.exclude(is_superuser=True)
        queryset = queryset.exclude(role__isnull=True).exclude(role="")
        search_query = self.request.GET.get('search', '')
        role_filter = self.request.GET.get('role', '')

        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query)
            )
        if role_filter:
            queryset = queryset.filter(role=role_filter)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roles'] = User.objects.exclude(role__isnull=True).exclude(role="").values_list('role', flat=True).distinct()
        context['search_query'] = self.request.GET.get('search', '')
        context['role_filter'] = self.request.GET.get('role', '')
        return context

class UserDetailView(DetailView):
    model = User
    template_name = 'user-detail.html'
    context_object_name = 'user_object'
    
class UserUpdateView(UpdateView):
    model = User
    form_class = UserDetailUpdateForm
    template_name = 'user-update.html'
    context_object_name = 'user_object'

    def get_object(self, queryset=None):
        user_pk = self.kwargs.get('pk')  
        return get_object_or_404(User, pk=user_pk)
    
    def get_success_url(self):
        return reverse_lazy('user-update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "User details have been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)
    
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'user-delete.html'
    context_object_name = 'user_object'
    success_url = reverse_lazy('users-list')

    def delete(self, request, *args, **kwargs):
        user_object = self.get_object()
        messages.success(self.request, f'User {user_object.first_name} {user_object.last_name} has been deleted.')
        return super().delete(request, *args, **kwargs)