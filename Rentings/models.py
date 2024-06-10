from django.db import models

from Books.models import Book
from Students.models import Student

class Rentings(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_rented = models.DateField()
    date_returned = models.DateField(null=True, blank=True)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return f'{self.book.name} rented by {self.student.first_name} {self.student.last_name}'

