from django.urls import path,include
from .import views

urlpatterns = [
   path('',views.index),
   path('index',views.index),
   path('register',views.studentRegister),
   path('home',views.studentHome),
   path('logout',views.Logout),
   path('changePass',views.changePass),
   # path('student/profile',views.studentProfile),
   path('requestBook',views.studentReqBook),
   path('dueBooks',views.studentDueBooks),
   path('history',views.studentHistory),
   path('searchBook',views.studentSearchBook),
   # path('student/books',views.studentBooks),
   # path('student/books/view',views.studentBookView),
]
