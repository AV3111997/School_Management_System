from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-details/', views.UserDetailUpdateView.as_view(), name='user-detail-update'),
    path('change-password/', views.PasswordChangeView.as_view(), name='user-password-change'),
]