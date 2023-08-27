from django.db import models
from datetime import date, timedelta
from student.models import User


class Book(models.Model):
    name = models.CharField(max_length=150)
    quantity = models.IntegerField()
    author = models.CharField(max_length=150)
    def __str__(self):
        return f"{self.quantity} {self.name}"

class Issue(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField(default=date.today()+timedelta(days=30))

    def __str__(self):
        return f"{self.user} issued {self.book} due on {self.due_date}"

class Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bookname = models.CharField(max_length=150)
    reason = models.TextField(max_length=500)

    def __str__(self):
        return f"{self.user} requested {self.bookname}"

class Penalty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.amount} on {self.user}"