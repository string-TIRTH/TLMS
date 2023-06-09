from django.shortcuts import render
from main.models import Book
from django.shortcuts import redirect, render,HttpResponse
from main.models import *
from django.contrib.auth import authenticate, login, logout
from main import models
from main import models
from datetime import date
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import random
def verifyEmail(request):
    if request.method == "POST":
        getotp = request.POST['OTP']
        email = request.POST['email']
        print("values =")
        print(email)
        print(getotp)
        otp = OTP.objects.get(email = email)
        print(otp.otp)
        if(str(getotp)== str(otp.otp)):
            # valid otp
            std = Student.objects.get(id = otp.user.id)
            std.isActive=True
            std.save()
            otp.delete()
            alert = 3
        else:
            alert = 3
            return render(request,'enterOtp.html',{'alert':alert},{'email':email})    
        return redirect('/student/index',{'alert':alert})
    return render(request,'enterOtp.html')

def send_email(request):
    
    subject ="Account Verification For Library Management System :"
    message ="Your OTP is : 343434"
    send_mail(subject, message,'librarymanagemnet.one@gmail', ['tirthprajapati26@gmail.com'])
    return redirect('/student/')
def studentRegister(request):
    if request.method == "POST":
        collegeID = request.POST['collegeID']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        id2 = email[0:10]
        if(collegeID != id2):
            alert = 3
            return render(request, "register.html", {'alert':alert})

        phone = request.POST['phone']
        dept = request.POST['dept']
        dob = request.POST['dob']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            alert = 4
            return render(request, "register.html", {'alert':alert})

        user = User.objects.create_user(username = collegeID,email=email, password=password,first_name=fname, last_name=lname)
        print(user)
        student = Student.objects.create(user=user, admissionDate = date.today(), mobile = phone,sem = 1,dob = dob,dept =dept,image = image)
        user.save()
        student.save()
        otp = random.randrange(100000,999999)
        otpobj = OTP()
        otpobj.user= student
        otpobj.email= email
        otpobj.otpType= 1
        otpobj.otp =otp
        otpobj.status =1
        otpobj.save()
        subject ="Account Verification For Library Management System :"
        message ="Your OTP is : "+str(otp)
        send_mail(subject, message,'librarymanagemnet.one@gmail', [email])
         
        return render(request,'enterOtp.html',{'email':email})
    return render(request, "register.html")


def studentReqBook(request):
    if request.method == "POST":
        bookTitle = request.POST['bookTitle']
        bookAuthor = request.POST['bookAuthor']
        bookEdition = request.POST['bookEdition']
        bookLanguage = request.POST['bookLanguage']
       
        req = Request()
        req.user = request.user
        req.bookTitle = bookTitle
        req.bookAuthor = bookAuthor
        req.bookEdition = bookEdition
        req.bookLanguage = bookLanguage
        
        req.save()
        alert =True
        return render(request, "requestBook.html",{'alert':alert})
    return render(request, "requestBook.html")

    
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser or request.user.is_staff:
                alert = 2
                return render(request, "index.html", {'alert':alert})
            else:
                # std = Student.objects.get(user_id=user.id)
                # if(std.isActive == False):
                #     return HttpResponse("Please Verify your email")
                return redirect("/student/home")
        else:
            alert = 1
            return render(request, "index.html", {'alert':alert})
    return render(request, "index.html")
@login_required(login_url = '/student/')
def studentHome(request):
    
    
    return render(request,"stdProfile.html")
@login_required(login_url = '/')
def Logout(request):
    logout(request)
    return redirect ("/student/")
@login_required(login_url = '/')
def changePass(request):
    if request.method == "POST":
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(current_password):
                u.set_password(new_password)
                u.save()
                alert = True
                return render(request, "changePass.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "changePass.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "changePass.html")

@login_required(login_url = '/')
def studentSearchBook(request):
        if request.method == "POST":
            # titleCheck = request.POST['bookTitleC']
            # authorCheck = request.POST['bookAuthorC']
            # categoryCheck = request.POST['bookCategoryC']
            titleCheck = request.POST.getlist('bookTitleC')
            authorCheck = request.POST.getlist('bookAuthorC')
            categoryCheck = request.POST.getlist('bookCategoryC')
            # print(titleCheck)
            # print(authorCheck)
            # print(categoryCheck)
            # author = keywsOn[0]
            # print(author)
            books = None
            if titleCheck and authorCheck and categoryCheck:
                bookTitle = request.POST['bookTitle']
                bookAuthor = request.POST['bookAuthor']
                bookCategory = request.POST['bookCategory']
                books = Book.objects.filter(bookName__icontains = bookTitle,bookAuthor = bookAuthor,bookCategory= bookCategory)
            elif titleCheck and authorCheck:
                bookTitle = request.POST['bookTitle']
                bookAuthor = request.POST['bookAuthor']
                books = Book.objects.filter(bookAuthor = bookAuthor,bookName__iconstains = bookTitle)
            elif authorCheck and categoryCheck:
                bookAuthor = request.POST['bookAuthor']
                bookCategory = request.POST['bookCategory']
                books = Book.objects.filter(bookAuthor= bookAuthor,bookCategory = bookCategory)
            elif titleCheck and categoryCheck:
                bookTitle = request.POST['bookTitle']
                bookCategory = request.POST['bookCategory']
                books = Book.objects.filter(bookCategory= bookCategory,bookName__icontains = bookTitle)
            elif titleCheck:
                bookTitle = request.POST['bookTitle']
                books = Book.objects.filter(bookName__icontains =  bookTitle)
                # books = Book.objects.raw("select * from main_book where bookName like %"+ bookTitle+"%")
            elif categoryCheck:
                bookCategory = request.POST['bookCategory']
                books = Book.objects.filter(bookCategory= bookCategory)
            elif authorCheck:
                bookAuthor = request.POST['bookAuthor']
                books = Book.objects.filter(bookAuthor= bookAuthor)
            # print(books)    
            # books = list(models.Book.objects.all())
            # print(books)   
            return render(request,"viewBook.html",{'books':books})
        
        return render(request,"searchBook.html")
@login_required(login_url = '/student/')
def studentHistory(request):
    print(request.user.id)
    issuedBooks = Issues.objects.filter(student = request.user.student)
    details = []
    j =0
    for i in issuedBooks:
        days = (date.today()-i.issueDate)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        books = list(Book.objects.filter(id=i.book_id,isActive =True))
        students = list(Student.objects.filter(id=i.student_id,isActive =True))
        print(books)
        print(students)
        i=0
        for l in books:
            t=(issuedBooks[j].id,books[i].bookName,issuedBooks[j].issueDate,issuedBooks[j].dueDate,fine,issuedBooks[j].status)
            i=i+1
            j=j+1
            details.append(t)
        print(details)
    return render(request, "stdHistory.html", {'issuedBooks':issuedBooks, 'details':details})
@login_required(login_url = '/student/')
def studentDueBooks(request):
    issuedBooks = Issues.objects.filter(student = request.user.student).exclude(status = 3)
    details = []
    j =0
    for i in issuedBooks:
        days = (date.today()-i.issueDate)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*5
        books = list(Book.objects.filter(id=i.book_id,isActive =True))
        students = list(Student.objects.filter(id=i.student_id,isActive =True))
        print(books)
        print(students)
        i=0
        for l in books:
            t=(issuedBooks[j].id,books[i].bookName,issuedBooks[j].issueDate,issuedBooks[j].dueDate,fine,issuedBooks[j].status)
            i=i+1
            j=j+1
            details.append(t)
    return render(request, "dueBooks.html", {'issuedBooks':issuedBooks, 'details':details})
