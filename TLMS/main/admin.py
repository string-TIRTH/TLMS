from django.contrib import admin
from .models import Book,Student,Issues,Request,Librarian
admin.site.register(Book)
admin.site.register(Student)
admin.site.register(Issues)
admin.site.register(Librarian)
admin.site.register(Request)
# Register your models here.
