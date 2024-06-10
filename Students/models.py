from django.db import models

class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField()
    address = models.CharField(max_length=200)
    grade=models.IntegerField(default=1)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    def __str__(self):
        name=self.first_name+" "+self.last_name
        return name