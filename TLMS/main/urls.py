from django.urls import path,include
from .import views

urlpatterns = [
   path('',views.index),
   # path('index',views.index),
   # path('student/register',views.studentRegister),
   # path('student/home',views.studentHome),
   # path('logout/',views.Logout),
   # path('student/changePass',views.changePass),
   # # path('student/profile',views.studentProfile),
   # # path('student/requestBook/',views.studentReqBook),
   # # path('student/dueBooks',views.studentDueBooks),
   # # path('student/history',views.studentHistory),
   # path('student/searchBook',views.studentSearchBook),
   # path('student/books',views.studentBooks),
   # path('student/books/view',views.studentBookView),
]
