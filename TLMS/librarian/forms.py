from django import forms
from django.contrib.auth.models import User
from main.models import Book,Student

class IssueBookForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="Book Name")
    name2 = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label="[College ID] [ID] [Department] [Semester]", label="Student Details")
    
    book.widget.attrs.update({'class': 'form-control'})
    name2.widget.attrs.update({'class':'form-control'})
