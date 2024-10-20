from django import forms
from .models import Students, Books, Library, Fees

class StudentsForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['name', 'father_name', 'mother_name', 'date_of_birth', 'gender', 'address', 'contact_number', 'grade']
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(2000, 2025)),
        }

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['name']

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['book', 'student', 'date_returned']

class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ['student', 'amount', 'due_date', 'payment_status', 'date_paid']
        widgets = {
            'date_paid': forms.DateInput(attrs={'type': 'date'}),
        }
