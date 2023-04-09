from django.db import models
from django.contrib.auth.models import User
class Book(models.Model):
    
    bookName = models.CharField(max_length=100)
    bookAuthor = models.CharField(max_length=35)
    bookDiscp = models.TextField(max_length=350)
    bookEdition = models.IntegerField()
    bookLang = models.CharField(max_length=35)
    bookCategory = models.CharField(max_length=35)
    bookQuantity = models.IntegerField()
    # bookUniqueID = models.CharField(max_length=10)
    bookImage = models.ImageField(upload_to="",blank=True)
    isActive = models.BooleanField(default=True)
    
     
    def __str__(self):
        return str(self.id)+ " ["+str(self.bookName)+']'+ " ["+str(self.bookAuthor)+']'+ " ["+str(self.bookDiscp)+']'+ " ["+str(self.bookEdition)+']'+ " ["+str(self.bookLang)+']'+ " ["+str(self.bookCategory)+']'+ " ["+str(self.bookQuantity)+']'+ " ["+str(self.bookImage)+']'
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sem = models.IntegerField()
    dept = models.CharField(max_length=35)
    isActive = models.BooleanField(default=False)
    mobile = models.IntegerField()
    admissionDate = models.DateField(null= False)
    dob = models.DateField(null = False)
    image = models.ImageField(upload_to="", blank=True)
    limit = models.IntegerField(default = 4)
    fine = models.FloatField(default=0)
    
    def __str__(self):
        return "```College ID : ["+str(self.user) +"]``````DEPT : ["+str(self.dept)+']```' + "```SEM : ["+str(self.sem)+']```' +"```Limit : ["+str(self.limit)+"]```"
class Librarian(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    address = models.TextField(max_length=100)
    salary = models.FloatField()
    isActive = models.BooleanField(default=True)
    mobile = models.IntegerField()
    joiningDate = models.DateField(null= False)
    dob = models.DateField(null = False)
    image = models.ImageField(upload_to="", blank=True)
   
    def __str__(self):
        return "["+str(self.id)+']'+" ["+str(self.user)+']'+ " ["+str(self.address)+']'+ " ["+str(self.salary)+']'+ " ["+str(self.mobile)+']'+ " ["+str(self.joiningDate)+']'+ " ["+str(self.dob)+']'+ " ["+str(self.image)+']'
class Issues(models.Model):
    
    book = models.ForeignKey(Book,unique=False, on_delete=models.CASCADE)
    student = models.ForeignKey(Student,unique=False, on_delete=models.CASCADE)
    # librarian_name = models.OneToOneField(Librarian.,on_delete=models.CASCADE)
    issueDate = models.DateField()
    dueDate = models.DateField()
    returnDate = models.DateField(default="")
    status = models.PositiveSmallIntegerField(default = 1)
    def __str__(self):
        return str(self.student_id)

class Request(models.Model):   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bookTitle = models.CharField(max_length=35)
    bookAuthor = models.CharField(max_length=100)
    bookLanguage = models.CharField(max_length=100)
    bookEdition = models.CharField(max_length=100)
    status = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return self.user
     
class OTP(models.Model):
    user= models.OneToOneField(Student, on_delete=models.CASCADE)
    otp = models.IntegerField(default=0)
    email = models.CharField(default="",max_length=255)
    otpType = models.CharField(default="", max_length=50)
    status = models.PositiveIntegerField(default=1)#1 active 2 used
    