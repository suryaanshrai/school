from django.db import models
from student.models import User

class News(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False)
    image = models.ImageField(blank=True,null=True)
    description = models.TextField(max_length=3750) 
    # 3750 characters provide a word limit of nearly 750 words assuming a char length of 5 for each word and ignoring spaces
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)


class Event(models.Model):
    event_name = models.CharField(max_length=150)
    date = models.DateField(blank=True, null=True)


class Gallery(models.Model):
    image = models.ImageField()
    title = models.CharField(max_length=100)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,blank=True,null=True)


class Submission(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, blank=True, null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_by")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="approved_by")


class ActiveSession(models.Model):
    news = models.ForeignKey(News,on_delete=models.CASCADE, blank=True, null=True)
    events = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True)