from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('students/grade/<int:grade_id>/', views.StudentsListByGradeView.as_view(), name='students-list-by-grade'),
    path('student/register/', views.StudentRegisterView.as_view(), name='student-register'),
    path('student/detail/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('student/update/<int:pk>/', views.StudentUpdateView.as_view(), name='student-update'),
    path('student/delete/<int:grade_id>/<int:pk>/', views.StudentDeleteView.as_view(), name='student-delete'),
    path('student/<int:pk>/fees/', views.StudentFeeDetailsListView.as_view(), name='student-fee-details-list'),
    path('student/fees/<int:pk>', views.StudentFeeDetailsView.as_view(), name='student-fee-detail'),
    path('student/<int:student_pk>/fee/update/<int:pk>/', views.StudentFeeUpdateView.as_view(), name='student-fee-update'),
    path('student/<int:student_pk>/fee/delete/<int:pk>/', views.StudentFeeDeleteView.as_view(), name='student-fee-delete'),
    path('fees/',views.FeesListView.as_view(), name='fees-list'),
    path('fees/make-payment/',views.FeesCreateView.as_view(), name='fees-create')
]