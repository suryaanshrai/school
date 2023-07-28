from django.db import models
from student.models import User

class News(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField(auto_now=False, auto_now_add=False)
    image = models.ImageField(upload_to="home/static/home/news",blank=True,null=True)
    description = models.TextField(max_length=3750) 
    # 3750 characters provide a word limit of nearly 750 words assuming a char length of 5 for each word and ignoring spaces
    author = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, editable=False,null=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, editable=False, related_name="approver")
    active = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
       if self.image is not None:
        self.image.delete()
       super().delete(*args, **kwargs)



class Event(models.Model):
    event_name = models.CharField(max_length=150)
    date = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=False)


class Gallery(models.Model):
    image = models.ImageField(upload_to="home/static/home/gallery")
    title = models.CharField(max_length=100)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,blank=True,null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,editable=False, related_name="author")
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, editable=False,related_name="approved_by")

    def delete(self, *args, **kwargs):
       self.image.delete()
       super().delete(*args, **kwargs)