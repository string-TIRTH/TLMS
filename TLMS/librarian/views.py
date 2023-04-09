from django.shortcuts import render
from main.models import Book
from django.shortcuts import redirect, render,HttpResponse
from .models import *
from django.contrib.auth import authenticate, login, logout
from main.models import Student,Issues,User
from . import forms 

from django.core.mail import send_mail
from django.conf import settings
from datetime import date
from datetime import datetime
import datetime as dt
from django.contrib.auth.decorators import login_required
# form django.contri
from django.shortcuts import render

# Create your views here.

def libLogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_staff:
                return redirect('/librarian/viewIssues')
            else:
                alert =1 
                return render(request,"libLogin.html",{'alert':alert})
        else:
            alert = 2
            return render(request, "libLogin.html", {'alert':alert})
    return render(request,'libLogin.html')
@login_required(login_url = '/librarian/')
def home(request):
    
    
    return render(request,'libProfile.html')

@login_required(login_url = '/librarian/')
def issueBook(request):
    form = forms.IssueBookForm()
    if request.method == "POST":
        form = forms.IssueBookForm(request.POST)
        if form.is_valid():
            obj = Issues()
            student_id =  request.POST['name2']
            obj.student_id = student_id
            std = Student.objects.get(id = student_id)
            limit = std.limit
            if(limit>0):
                    obj.issueDate = date.today()
                    bid = request.POST['book']
                    obj.book_id = bid
                    obj.returnDate = date.today()
                    dueDate = date.today() + dt.timedelta(days = 15)
                    obj.dueDate = dueDate
                    print(bid)
                    book = Book.objects.get(id = bid)
                    print(book)
                    book.bookQuantity = book.bookQuantity-1
                    if(book.bookQuantity>=0):    
                        # check = Issues.objects.get(student = student_id,book = bid)
                        # print(check)
                                                        # print(obj.student_id)
                                                        # print(obj.book_id)
                        std.limit= std.limit-1
                        std.save()
                        std.save()
                        book.save()
                        obj.save()
                        alert = 1
                    else: 
                        alert =3
            else:
                    alert = 2
            return render(request, "issueBook.html", {'obj':obj, 'alert':alert})
    return render(request,'issueBook.html',{'form':form})
@login_required(login_url = '/librarian/')
def viewIssues(request):
    issuedBooks = Issues.objects.all().order_by('status')
    details = []
    j =0
    for i in issuedBooks:
        dt1 = str(i.dueDate)
        dt2 = str(date.today())
        d1 = datetime.strptime(dt1,'%Y-%m-%d')
        d2 = datetime.strptime(dt2,'%Y-%m-%d')
        delta = d1 - d2
        delta.days
        fine=0
        if delta.days<0:
            fine=abs(delta.days*10)
        books = list(Book.objects.filter(id=i.book_id,isActive =True))
        students = list(Student.objects.filter(id=i.student_id,isActive =True))
        # print(books)
        # print(students)
        i=0
        print(fine)
        if(fine>0):
            print("Due :"+str(j))
            issuedBooks[j].status = 2
            issuedBooks[j].save()
            
        for l in books:
           
            # print(delta.days) 
            t=(issuedBooks[j].id,students[i].user.get_full_name,students[i].user,books[i].bookName,issuedBooks[j].issueDate,issuedBooks[j].dueDate,abs(delta.days),fine,issuedBooks[j].status)
            students[i].fine = fine
            students[i].save()
            i=i+1
            j=j+1
            
            # print(t)
            details.append(t)
    return render(request, "viewIssues.html", {'issuedBooks':issuedBooks, 'details':details})
    
@login_required(login_url = '/librarian/')
def returnReissueBook(request):
    issuedBooks = Issues.objects.exclude(status = 3)
    details = []
    j =0
    for i in issuedBooks:
        dt1 = str(i.dueDate)
        dt2 = str(date.today())
        d1 = datetime.strptime(dt1,'%Y-%m-%d')
        d2 = datetime.strptime(dt2,'%Y-%m-%d')
        delta = d1 - d2
        delta.days
        fine=0
        if delta.days<0:
            fine=delta.days*10
        books = list(Book.objects.filter(id=i.book_id,isActive =True))
        students = list(Student.objects.filter(id=i.student_id,isActive =True))
        print(books)
        print(students)
        i=0
        for l in books:
            t=(issuedBooks[j].id,students[i].user.get_full_name,students[i].user,books[i].bookName,issuedBooks[j].issueDate,issuedBooks[j].dueDate,abs(delta.days),fine,issuedBooks[j].status)
            i=i+1
            j=j+1
            details.append(t)
    return render(request, "returnBook.html", {'issuedBooks':issuedBooks, 'details':details})

@login_required(login_url = '/librarian/')    
def viewStudents(request):
    students = Student.objects.all()
    print(students)
    issueCount = []
    # query = "select * from Issues"
    # issues = Issues.objects.raw('select * from Issues')
    for student in students:
        issues = Issues.objects.filter(student_id = student)
        issues = len(issues)
        issueCount.append(issues)
    return render(request, "viewStudents.html", {'students':students,'issueCount':issueCount})

@login_required(login_url = '/librarian/')    
def reissueBook(request,myid):
    issue = Issues.objects.get(id=myid)
    issue.dueDate=datetime.today()+dt.timedelta(days = 15)
    issue.issueDate=datetime.today()
    issue.save()
    alert = 1
    return redirect('/librarian/returnReissueBook',{'alert':alert})

@login_required(login_url = '/librarian/')    
def returnBook(request,myid):
    issue = Issues.objects.get(id=myid)
    issue.status = 3
    stdid = issue.student.id
    # print("id = ")
    # print(stdid)
    std = Student.objects.get(id = stdid)
    # print(std)
    std.limit = std.limit+1
    std.save()
    issue.save()
    alert = 2
    return redirect('/librarian/returnReissueBook',{'alert':alert})
        

# def viewStudents(request):
#     students = Student.objects.all()
#     return render(request, "viewStudents.html", {'students':students})
@login_required(login_url = '/librarian/')
def viewBooks(request):
    books = Book.objects.all()
    print(books)
    return render(request,"libViewBooks.html",{'books':books})
@login_required(login_url = '/librarian/')
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
                return render(request, "libChangePass.html", {'alert':alert})
            else:
                currpasswrong = True
                return render(request, "libChangePass.html", {'currpasswrong':currpasswrong})
        except:
            pass
    return render(request, "libChangePass.html")
@login_required(login_url = '/librarian/')
def profile(request):
    
    
    return render(request,"libProfile.html")
@login_required(login_url = '/librarian/')
def Logout(request):
    logout(request)
    return redirect ("/librarian/")

def notifyEmail(request,myid):
    issue = Issues.objects.get(id=myid)
    user = User.objects.get(id = issue.student.user_id)
    # print(user.email)
    
    print(issue.dueDate)    
    str()
    msg ="Hello "+str(user.first_name)+" "+str(user.last_name)+"\n Please Return Book ["+str(issue.book.bookName)+"] on or before "+str(issue.dueDate)+" to avoid penalties you can reissue it if you need it please visit library \n if you miss the due date then you have to pay 10₹/- as penalty per day... \n Have a nice day"
    subject= "Reminder From Library"
    
    # print(msg)
    sendEmail(user.email,subject,msg)
    alert = 3
    
    return redirect('/librarian/viewIssues',{'alert':alert})
def notifyAll(request):
    issues = Issues.objects.exclude(status = 3)
    
    for i in issues:
        user = User.objects.get(id = i.student.user_id)
        msg ="Hello "+str(user.first_name)+" "+str(user.last_name)+"\n Please Return Book ["+str(i.book.bookName)+"] on or before "+str(i.dueDate)+" to avoid penalties you can reissue it if you need it please visit library \n if you miss the due date then you have to pay 10₹/- as penalty per day... \n Have a nice day"
        subject= "Reminder From Library" 
        sendEmail(user.email,subject,msg)
           
    return redirect('/librarian/viewIssues')
def sendEmail(email,subject,message):
    
    send_mail(subject, message,'librarymanagemnet.one@gmail', [email])
    return 