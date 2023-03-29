from django.urls import path,include
from .import views

urlpatterns = [
   path('',views.libLogin),
   path('issueBook',views.issueBook),
   path('viewStudents',views.viewStudents),
   path('viewIssues',views.viewIssues),
   path('viewBooks',views.viewBooks),
   path('returnReissueBook',views.returnReissueBook),
   path('reissueBook/<int:myid>/',views.reissueBook),
   path('returnBook/<int:myid>/',views.returnBook),
   path('home',views.home),
   path('logout',views.Logout),
   path('changePass',views.changePass),
   path('profile',views.profile),
#    # path('student/requestBook/',views.studentReqBook),
#    # path('student/dueBooks',views.studentDueBooks),
#    # path('student/history',views.studentHistory),
#    path('student/searchBook',views.studentSearchBook),
#    # path('student/books',views.studentBooks),
#    # path('student/books/view',views.studentBookView),
]
