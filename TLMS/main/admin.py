from django.contrib import admin
from .models import Book,Student,Issues,Request,Librarian,OTP
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Issues)
admin.site.register(Librarian)
admin.site.register(Request)
admin.site.register(OTP)
# Register your models here.
