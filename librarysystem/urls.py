from django.contrib import admin
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.my_login, name="my_login"),
    path('dashboard/', login_required(views.dashboard), name="dashboard"),
    path('students/', login_required(views.students), name="students"),
    path('books/', login_required(views.books), name="books"),
    path('rentings/', login_required(views.rentings), name="rentings"),
    path('logout/', login_required(views.user_logout), name='user-logout'),
    path('books/create/', login_required(views.books_create), name='books-create'),
    path('books/<int:book_id>/', login_required(views.book_detail), name='book_detail'),
    path('students/create/', login_required(views.students_create), name='students-create'),
    path('rentings/create/', login_required(views.add_renting), name='add-renting'),
    path('students/<int:student_id>/', login_required(views.students_detail), name='students_detail'),
    path('rentings/<int:renting_id>/', login_required(views.renting_detail), name='renting_detail'),
    path('rentings/<int:renting_id>/mark_as_read/', login_required(views.mark_as_read), name='mark_as_read'),
    path('students/edit/<int:student_id>/', login_required(views.student_edit), name='student_edit'),
    path('students/delete/<int:student_id>/', login_required(views.student_delete), name='student_delete'),
    path('book/delete/<int:book_id>/', login_required(views.book_delete), name='book_delete'),
    path('rentings/edit/<int:renting_id>/', login_required(views.edit_renting), name='renting_edit'),
    path('book/edit/<int:book_id>/', login_required(views.book_edit), name='book_edit'),
]
