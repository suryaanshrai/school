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

class Penalty(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField()
    due_date = models.DateField()
    date_of_return = models.DateField(default=date.today())

    def __str__(self):
        return f"{self.amount} on {self.user}"