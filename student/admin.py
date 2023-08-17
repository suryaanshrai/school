from django.contrib import admin
from student.models import User,Result, Schedule, Classroom, Notice, Member
# Register your models here.
admin.site.register(User)
admin.site.register(Result)
admin.site.register(Schedule)
admin.site.register(Classroom)
admin.site.register(Notice)
admin.site.register(Member)