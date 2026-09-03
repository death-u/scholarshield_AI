from django.contrib import admin
from .models import Profile,AcademicTask,AcademicNote
# Register your models here.
admin.site.register(Profile)
admin.site.register(AcademicTask)
admin.site.register(AcademicNote)