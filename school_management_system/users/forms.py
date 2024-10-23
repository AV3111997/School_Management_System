from django import forms
from .models import Students, Books, Library, Fees, Grade

class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = ['name', 'father_name', 'mother_name', 'date_of_birth', 'gender', 'address', 'contact_number', 'grade']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'address': forms.Textarea(attrs={'class': 'form-control form-control-lg', 'rows':1}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-lg'}),
        }
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control form-control-lg'}),
    )

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = ['book', 'student']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control', 'size': '0'}),
            'student': forms.Select(attrs={'class': 'form-control', 'size': '0'}),
        }

class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ['student', 'amount', 'due_date', 'payment_status', 'payment_method']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control', 'size': '0'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

class FeesUpdateForm(forms.ModelForm):
    class Meta:
        model = Fees
        fields = ['amount', 'payment_status', 'payment_method', 'date_paid']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }
    
    # def save(self, commit=True):
    #     fees_instance = super().save(commit=False)
    #     fees_instance.payment_status = 'paid'
    #     if commit:
    #         fees_instance.save() 
    #     return fees_instance 
