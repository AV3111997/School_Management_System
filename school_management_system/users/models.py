from django.db import models

# Create your models here.

class Grade(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Grade",
        blank=False
    )
    
    def __str__(self):
        return self.name

class Students(models.Model):
    GENDER_CHOICES= [
        ("F", "Female"),
        ("M", "Male"),
    ]

    name = models.CharField(
        max_length=100,
        verbose_name="Student's Name",
        blank=False
    )
    father_name = models.CharField(
        max_length=100,
        verbose_name="Father's Name",
        blank=False
    )
    mother_name = models.CharField(
        max_length=100,
        verbose_name="Mother's Name",
        blank=False
    )
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        blank=False
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Gender"
    )
    address = models.TextField(
        verbose_name="Address",
        blank=False
    )
    contact_number = models.CharField(
        max_length=15,
        verbose_name="Contact Number",
        blank=False
    )
    grade = models.ForeignKey(Grade,
        verbose_name="Grade",
        on_delete=models.CASCADE, 
        related_name='grade'
    ) 

    def __str__(self):
        return f"{self.name} (Grade: {self.grade})"

class Books(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name="Title",
        blank=False
    )

    def __str__(self):
        return self.name
    
class Library(models.Model):
    book = models.ForeignKey(
        Books, 
        verbose_name='Book',
        on_delete=models.CASCADE, 
        related_name='book'
    )
    student = models.ForeignKey(
        Students, 
        verbose_name='Borrower', 
        on_delete=models.CASCADE, 
        related_name='student'
    )
    date_borrowed = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Date Borrowed'
    )
    date_returned = models.DateTimeField(
        verbose_name='Date Returned',
        null=True,
        blank=True,
        default="Not yet returned"
    )

    def __str__(self):
        return self.student, self.book

class Fees(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('cash', 'Cash'),
    ]
    student = models.ForeignKey(
        Students,
        verbose_name="Student's Name",
        on_delete=models.CASCADE,
        related_name='fees'
    )
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Amount'
    )
    due_date = models.DateField()  
    payment_status = models.CharField(
        max_length=20,
        choices= PAYMENT_STATUS_CHOICES,
        default='unpaid',
        verbose_name='Status'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True,
        blank=True,
        verbose_name='Payment Method',
    )
    date_paid = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Payment Date',
    )

    def __str__(self):
        return self.student, self.amount, self.due_date, self.payment_status, self.payment_method