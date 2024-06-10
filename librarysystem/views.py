from django.shortcuts import render, redirect,get_object_or_404
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from Books.models import Book
from Students.models import Student
from Rentings.models import Rentings
from django.http import HttpResponse
from django.db.models import Count, Q
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404



def my_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard or another page on successful login
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'librarysystem/my_login.html', {'form': form})

# Dashboard
def dashboard(request):
    active_rentings = Rentings.objects.filter(date_returned__isnull=True)
    thebooks = Book.objects.all()
    thestudents = Student.objects.all()
    return render(request, 'librarysystem/dashboard.html', {'active': active_rentings, 'books': thebooks, 'students': thestudents})

# Students
def students(request):
    # Annotate each student with the count of active rentals
    thestudents = Student.objects.annotate(
    active_rent_count=Count('rentings', filter=Q(rentings__date_returned__isnull=True))
    )

    return render(request, 'librarysystem/students.html', {'students': thestudents})



def students_detail(request,student_id):
    student = get_object_or_404(Student, id=student_id)
    active_rentings_count = Rentings.objects.filter(student=student, date_returned__isnull=True).count()
    past_rentings_count=Rentings.objects.filter(student=student,date_returned__isnull=False).count()
    active_rentings=Rentings.objects.filter(student=student,date_returned__isnull=True)
    past_rentings=Rentings.objects.filter(student=student,date_returned__isnull=False)

    return render(request, 'librarysystem/students_detail.html', {'student': student,'activerents':active_rentings_count,'pastrentings':past_rentings_count,'active':active_rentings,'past':past_rentings})


def students_create(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birthday = request.POST.get('birthday')
        adress = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        grade = request.POST.get('grade')

        # Check if any of the fields are empty
        if not all([first_name, last_name, birthday, adress, phone, email, grade]):
            error_message = "All input fields must be populated before confirming."
            return render(request, 'librarysystem/students_create.html', {'error_message': error_message})

        student = Student()
        student.first_name = first_name
        student.last_name = last_name
        student.address = adress
        student.birth_date = birthday
        student.phone = phone
        student.email = email
        student.grade = grade
        student.save()
        return redirect('/students/')
    return render(request, 'librarysystem/students_create.html')



def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.birth_date = request.POST.get('birthday')
        student.address = request.POST.get('address')
        student.phone = request.POST.get('phone')
        student.email = request.POST.get('email')
        student.grade = request.POST.get('grade')
        student.save()
        return redirect('students_detail', student_id=student.id)
    
    return render(request, 'librarysystem/student_edit.html', {'student': student})

def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



# Books
def books(request):
    thebooks = Book.objects.annotate(
    rented=Count('rentings',filter=Q(rentings__date_returned__isnull=True))
    )
    return render(request, 'librarysystem/books.html', {'books': thebooks})



def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    active_rentings_count = Rentings.objects.filter(book=book, date_returned__isnull=True).count()
    past_rentings_count=Rentings.objects.filter(book=book,date_returned__isnull=False).count()
    active_rentings=Rentings.objects.filter(book=book,date_returned__isnull=True)
    past_rentings=Rentings.objects.filter(book=book,date_returned__isnull=False)




    return render(request, 'librarysystem/books_detail.html', {'book': book,'activerents':active_rentings_count,'pastrentings':past_rentings_count,'active':active_rentings,'past':past_rentings})


def book_delete(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.delete()
        return JsonResponse({'message': 'Book deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)


def books_create(request):
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        author = request.POST.get('book_author')
        category = request.POST.get('book_category')
        quantity = request.POST.get('book_quantity')
        location = request.POST.get('book_location')
        registered_date = request.POST.get('book_registered_date')

        # Check if any of the fields are empty
        if not all([book_name, author, category, quantity, location, registered_date]):
            error_message = "All input fields must be populated before confirming."
            return render(request, 'librarysystem/books_create.html', {'error_message': error_message})

        book = Book()
        book.name = book_name
        book.author = author
        book.category = category
        book.quantity = quantity
        book.location = location
        book.registered_date = registered_date
        book.save()
        return redirect('/books')

    return render(request, 'librarysystem/books_create.html')


def book_edit(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        book.name = request.POST.get('name')
        book.author = request.POST.get('author')
        book.category = request.POST.get('category')
        book.location = request.POST.get('location')
        book.quantity = request.POST.get('quantity')
        book.save()
        return redirect('book_detail', book_id=book.id)
    
    return render(request, 'librarysystem/book_edit.html', {'book': book})

def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.delete()
        return JsonResponse({'message': 'Student deleted successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)




# Rentings
def rentings(request):
    active_rentings = Rentings.objects.filter(date_returned__isnull=True)
    return render(request, 'librarysystem/rentings.html', {'active': active_rentings})

def add_renting(request):
    if request.method == 'POST':
        book_id = request.POST.get('book')
        student_id = request.POST.get('student')
        date_rented = request.POST.get('date_rented')
        date_returned = request.POST.get('date_returned')
        quantity=request.POST.get('quantity')

        try:
            book = Book.objects.get(id=book_id)
            student = Student.objects.get(id=student_id)
            renting = Rentings(
                book=book,
                student=student,
                date_rented=date_rented,
                quantity=quantity,
                date_returned=date_returned if date_returned else None
            )
            renting.save()
            return redirect('/rentings')  # Assuming you have a success page
        except (Book.DoesNotExist, Student.DoesNotExist):
            return HttpResponse("Invalid book or student ID", status=400)

    books = Book.objects.all()
    students = Student.objects.all()
    return render(request, 'librarysystem/add_renting.html', {'books': books, 'students': students})





def edit_renting(request, renting_id):
    # Get the renting object to be edited
    renting = get_object_or_404(Rentings, id=renting_id)
    
    if request.method == 'POST':
        # If the form is submitted
        book_id = request.POST.get('book')
        student_id = request.POST.get('student')
        quantity = request.POST.get('quantity')
        date_rented = request.POST.get('date_rented')
        date_returned = request.POST.get('date_returned')
        
        # Update the renting object with the new data
        renting.book = Book.objects.get(pk=book_id)
        renting.student = Student.objects.get(pk=student_id)
        renting.quantity = quantity
        renting.date_rented = date_rented
        date_returned=date_returned if date_returned else None
        renting.save()
        
        return redirect('rentings')  # Redirect to a page displaying all rentings or any other desired page
    
    books = Book.objects.all()
    students = Student.objects.all()
    return render(request, 'librarysystem/renting_edit.html', {'renting':renting,'books': books, 'students': students})
 



def renting_detail(request,renting_id):
    renting = get_object_or_404(Rentings, id=renting_id)
    return render(request, 'librarysystem/rentings_detail.html', {'renting':renting })


def mark_as_read(request, renting_id):
    renting = get_object_or_404(Rentings, id=renting_id)
    renting.date_returned = timezone.now()
    renting.save()
    return redirect('/rentings')

    




# Logout
def user_logout(request):
    logout(request)
    return redirect('my_login')
