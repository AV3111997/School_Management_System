from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, DetailView, ListView, UpdateView, DeleteView, CreateView
from django.views.generic.edit import FormView
from django.db.models import Count
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import Students, Books, Library, Fees, Grade
from .forms import StudentRegisterForm, BooksForm, LibraryForm, FeesForm, FeesUpdateForm, GradeForm
from accounts.models import User
from django.utils import timezone

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grades'] = Grade.objects.all()
        return context

class StudentRegisterView(CreateView):
    model = Students
    template_name = "office_staff/student-register.html"
    form_class = StudentRegisterForm
    success_url = reverse_lazy("student-register")

    def form_valid(self, form):
        messages.success(self.request, "Student Registered successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return super().form_invalid(form)

class StudentsListByGradeView(ListView):
    model = Students
    template_name = 'office_staff/students-list-by-grade.html'
    context_object_name = 'students'
    paginate_by = 10

    def get_queryset(self):
        grade_id = self.kwargs['grade_id']
        queryset = Students.objects.filter(grade__id=grade_id)
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        grade_id = self.kwargs['grade_id']
        context['grade'] = Grade.objects.get(id=grade_id)
        return context
    
class StudentDetailView(DetailView):
    model = Students
    template_name = 'office_staff/student-detail.html'
    context_object_name ='student'

class StudentUpdateView(UpdateView):
    model = Students
    template_name = 'office_staff/student-update.html'
    form_class = StudentRegisterForm
    context_object_name ='student'

    def get_object(self, queryset=None):
        student_pk = self.kwargs.get('pk')  
        return get_object_or_404(Students, pk=student_pk)
    
    def get_success_url(self):
        return reverse_lazy('student-fee-update', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, "Student's details have been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")

class StudentDeleteView(DeleteView):
    model = Students
    template_name = 'office_staff/student-delete.html'
    context_object_name = 'student'

    def get_success_url(self):
        grade_id = self.kwargs['grade_id']
        return reverse('students-list-by-grade', kwargs={'grade_id': grade_id})

    def delete(self, request, *args, **kwargs):
        student = self.get_object()
        messages.success(self.request, f'Student {student.name} has been deleted.')
        return super().delete(request, *args, **kwargs)
    
class StudentFeeDetailsListView(ListView):
    model = Fees
    template_name = 'office_staff/student-fee-details-list.html'
    context_object_name = 'fees'
    paginate_by = 10

    def get_queryset(self):
        student_id = self.kwargs['pk']
        return Fees.objects.filter(student_id=student_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['pk']
        context['student'] = Students.objects.get(pk=student_id)
        return context

class StudentFeeDetailsView(DetailView):
    model = Fees
    template_name = 'office_staff/student-fee-detail.html'
    context_object_name ='student_fee'

class StudentFeeUpdateView(UpdateView):
    model = Fees
    template_name = 'office_staff/student-fee-update.html'
    form_class = FeesUpdateForm
    context_object_name = 'fee'

    def get_object(self, queryset=None):
        fee_pk = self.kwargs.get('pk')
        return get_object_or_404(Fees, pk=fee_pk)
    
    def get_success_url(self):
        return reverse_lazy('student-fee-update', kwargs={'student_pk': self.object.student.pk, 'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.object.student
        context['fee'] = self.object
        return context

    def form_valid(self, form):
        fee_instance = form.save(commit=False)
        if fee_instance.payment_status == 'paid':
            fee_instance.date_paid = timezone.now().date()
        else:
            fee_instance.date_paid = None 
        fee_instance.save()
        messages.success(self.request, "Fees details have been updated successfully.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Please correct the errors below.")
        return self.render_to_response(self.get_context_data(form=form))

class StudentFeeDeleteView(DeleteView):
    model = Fees
    template_name = 'office_staff/student-fee-delete.html'
    context_object_name = 'student_fee'
    
    def get_object(self):
        student_pk = self.kwargs['student_pk']
        fee_pk = self.kwargs['pk']
        return Fees.objects.get(pk=fee_pk, student__pk=student_pk)

    def get_success_url(self):
        return reverse('fees-list')

    def delete(self, request, *args, **kwargs):
        fee = self.get_object()
        student_name = fee.student.name
        messages.success(self.request, f'Fee record for {student_name} has been deleted.')
        return super().delete(request, *args, **kwargs)
    
class FeesListView(ListView):
    model = Fees
    template_name = 'office_staff/fees-list.html'
    context_object_name = 'fees'
    paginate_by = 10
    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = Fees.objects.all().order_by('-date_paid')
        if search_query:
            queryset = queryset.filter(
                Q(student__name__icontains=search_query)
            )
        return queryset

class FeesCreateView(CreateView):
    model = Fees
    template_name = 'office_staff/fees-create.html'
    form_class = FeesForm
    success_url = reverse_lazy('fees-list')

class AdminStudentSectionView(ListView):
    model = Grade
    template_name = 'admin/students-by-grade-section.html'
    context_object_name = 'grades'

class StaffListView(ListView):
    model = User
    template_name = 'admin/staffs-lists.html'
    context_object_name = 'staffs'
    paginate_by = 10

    def get_queryset(self):
        role = self.kwargs.get('role')
        search_query = self.request.GET.get('search', '')
        queryset = User.objects.filter(role=role)
        if search_query:
            queryset = queryset.filter(
                Q(first_name__icontains=search_query) | 
                Q(last_name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['role'] = self.kwargs.get('role').capitalize()
        context['search_query'] = self.request.GET.get('search', '')
        return context

class LibrarianStudentSectionView(ListView):
    model = Grade
    template_name = 'librarian/students-by-grade-section.html'
    context_object_name = 'grades'
    paginate_by = 10

class LibraryCreateView(CreateView):
    model = Library
    form_class = LibraryForm
    template_name = 'librarian/library-record-create.html'
    success_url = reverse_lazy('library-history-list')

class LibraryHistoryListView(ListView):
    model = Library
    template_name = 'librarian/library-history.html'
    context_object_name = 'library_records'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(student__name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context

class LibraryRecordDetailView(DetailView):
    model = Library
    template_name = 'librarian/library-record-detail.html'
    context_object_name = 'record'

class LibraryRecordDeleteView(DeleteView):
    model = Library
    template_name = 'librarian/library-record-delete.html'
    context_object_name = 'record'
    success_url = reverse_lazy('library-history-list')

class AddBooksView(CreateView):
    model = Books
    form_class = BooksForm
    template_name = 'librarian/add-books.html'
    success_url = reverse_lazy('add-books')

    def form_valid(self, form):
        messages.success(self.request, "Book have been added successfully.")
        return super().form_valid(form)

class ManageBooksView(ListView):
    model = Books
    template_name = 'librarian/manage-books.html'
    context_object_name = 'books'
    paginate_by = 10

class DeleteBooksView(DeleteView):
    model = Books
    template_name = 'librarian/delete-books.html'
    context_object_name = 'book'
    success_url = reverse_lazy('manage-books')

class ManageGradeView(ListView):
    model = Grade
    template_name = 'admin/manage-grades.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return Grade.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = GradeForm()
        return context

    def post(self, request, *args, **kwargs):
        form = GradeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage-grades')
        else:
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class DeleteGradeView(DeleteView):
    model = Grade
    template_name = 'admin/manage-grades.html'
    success_url = reverse_lazy('manage-grades')
    

def update_date_returned(request, pk):
    record = get_object_or_404(Library, pk=pk)
    record.date_returned = timezone.now()
    record.save()
    return redirect('library-record-detail', pk=record.pk)
