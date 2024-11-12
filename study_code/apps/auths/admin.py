from django.contrib import admin
from .models import (
    Task, CustomUser, Tutor, Student, 
    Result, Chapter, Subject, Group
)


admin.site.register(Task)
admin.site.register(CustomUser)
admin.site.register(Tutor)
admin.site.register(Student)
admin.site.register(Result)
admin.site.register(Chapter)
admin.site.register(Subject)
admin.site.register(Group)