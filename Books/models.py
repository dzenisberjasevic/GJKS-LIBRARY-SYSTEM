from django.db import models

class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    registered_date = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name

 
