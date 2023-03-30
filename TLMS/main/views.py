from django.shortcuts import render
from main.models import Book
from django.shortcuts import redirect, render,HttpResponse
from main.models import *
from django.contrib.auth import authenticate, login, logout
from main import models
from datetime import date
from django.contrib.auth.decorators import login_required



def studentRegister(request):
    if request.method == "POST":
        collegeID = request.POST['collegeID']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dept = request.POST['dept']
        dob = request.POST['dob']
        image = request.FILES['image']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            passnotmatch = True
            return render(request, "register.html", {'passnotmatch':passnotmatch})

        user = User.objects.create_user(username = collegeID,email=email, password=password,first_name=fname, last_name=lname)
        print(user)
        student = Student.objects.create(user=user, admissionDate = '2003-12-01', mobile = phone,sem = 1,dob = '2003-12-01',dept =dept,image = image)
        user.save()
        student.save()
        alert = True
        return render(request, "register.html", {'alert':alert})
    return render(request, "register.html")

    
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_superuser:
                return HttpResponse("You are not a student!!")
            else:
                return redirect("/student/home")
        else:
            alert = True
            return render(request, "index.html", {'alert':alert})
    return render(request, "index.html")
@login_required(login_url = '/')
def studentHome(request):
    
    
    return render(request,"stdProfile.html")
@login_required(login_url = '/')
def Logout(request):
    logout(request)
    return redirect ("/")
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
def returnReissueBook(request):
    issuedBooks = Issues.objects.exclude(student = request.user.id,status = 3)
    details = []
    j =0
    for i in issuedBooks:
        days = (date.today()-i.issueDate)
        d=days.days
        fine=0
        if d>14:
            day=d-14
            fine=day*10    
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
    return render(request, "stdHistory.html", {'issuedBooks':issuedBooks, 'details':details})
