from django.contrib import admin
from .models import Issue,Book,Request,Penalty
# Register your models here.

admin.site.register(Issue)
admin.site.register(Book)
admin.site.register(Request)
admin.site.register(Penalty)