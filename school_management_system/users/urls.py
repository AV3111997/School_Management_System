from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='home'),
    path('administrator/students', views.AdminStudentSectionView.as_view(), name='admin-students-lists'),
    path('administrator/<str:role>/', views.StaffListView.as_view(), name='staff-lists'),
    path('manage-grades/', views.ManageGradeView.as_view(), name='manage-grades'),
    path('delete-grades/<int:pk>/', views.DeleteGradeView.as_view(), name='delete-grades'),
    path('librarian/students', views.LibrarianStudentSectionView.as_view(), name='librarian-students-lists'),
    path('librarian/library/record/create/', views.LibraryCreateView.as_view(), name='library-create'),
    path('librarian/library/record/<int:pk>', views.LibraryRecordDetailView.as_view(), name='library-record-detail'),
    path('librarian/library/record/delete/<int:pk>', views.LibraryRecordDeleteView.as_view(), name='library-record-delete'),
    path('librarian/library/history/', views.LibraryHistoryListView.as_view(), name='library-history-list'),
    path('librarian/library/record/update-returned/<int:pk>/', views.update_date_returned, name='update-date-returned'),
    path('librarian/add-books/', views.AddBooksView.as_view(), name='add-books'),
    path('librarian/manage-books/', views.ManageBooksView.as_view(), name='manage-books'),
    path('librarian/delete-books/<int:pk>/', views.DeleteBooksView.as_view(), name='delete-books'),
    path('office-staff/students/grade/<int:grade_id>/', views.StudentsListByGradeView.as_view(), name='students-list-by-grade'),
    path('office-staff/student/register/', views.StudentRegisterView.as_view(), name='student-register'),
    path('office-staff/student/detail/<int:pk>/', views.StudentDetailView.as_view(), name='student-detail'),
    path('office-staff/student/update/<int:pk>/', views.StudentUpdateView.as_view(), name='student-update'),
    path('office-staff/student/delete/<int:grade_id>/<int:pk>/', views.StudentDeleteView.as_view(), name='student-delete'),
    path('office-staff/student/<int:pk>/fees/', views.StudentFeeDetailsListView.as_view(), name='student-fee-details-list'),
    path('office-staff/student/fees/<int:pk>', views.StudentFeeDetailsView.as_view(), name='student-fee-detail'),
    path('office-staff/student/<int:student_pk>/fee/update/<int:pk>/', views.StudentFeeUpdateView.as_view(), name='student-fee-update'),
    path('office-staff/student/<int:student_pk>/fee/delete/<int:pk>/', views.StudentFeeDeleteView.as_view(), name='student-fee-delete'),
    path('office-staff/fees/',views.FeesListView.as_view(), name='fees-list'),
    path('office-staff/fees/make-payment/',views.FeesCreateView.as_view(), name='fees-create')
    
]