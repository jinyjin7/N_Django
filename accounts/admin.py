from django.contrib import admin
from accounts.models import *

admin.site.register(BaseUser)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
admin.site.register(School)
