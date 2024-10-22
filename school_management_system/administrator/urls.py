from django.urls import path
from .import views

urlpatterns = [
    path('users-list', views.UserListView.as_view(), name='users-list'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<int:pk>/', views.UserDeleteView.as_view(), name='user-delete'),
]