from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    is_employee = models.BooleanField(default=False)


class Result(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=150)
    marks = models.IntegerField()
    max_marks = models.IntegerField()
    date = models.DateField()


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
    

class Notice(models.Model):
    issued_for = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    issued_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField(max_length=2000)


class SessionResults(models.Model):
    result = models.ForeignKey(Result, on_delete=models.CASCADE)