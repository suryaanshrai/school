from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=150)
    marks = models.IntegerField()
    max_marks = models.IntegerField()
    date = models.DateField()
    is_active = models.BooleanField(default=True)


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=150)
    due_date = models.DateTimeField()


def validate_section(value):
    if value not in ('A', 'B', 'C'):
        raise ValidationError(
            _("%(value)s is not a valid section"),
            params={"value":value},
        )

class Classroom(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE)
    standard = models.IntegerField(validators=[
        MaxValueValidator(12),
        MinValueValidator(6)
    ])
    section = models.CharField(max_length=1, validators=[validate_section])
    
    def __str__(self):
        return f"{self.member} in {self.standard} {self.section}"

class Notice(models.Model):
    issued_for = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=2000)
    issue_date = models.DateField(default=datetime.now())

    def __str__(self):
        return f"{self.issued_for}:{self.title}"