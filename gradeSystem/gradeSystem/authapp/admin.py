from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(AllUser)
class AllUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('is_staff', 'is_active')
    ordering = ('-date_joined',)
    list_per_page = 20

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'gender', 'grade_level', 'class_name', 'phone_number', 'address', 'date_of_birth', 'is_verified')
    search_fields = ('id', 'full_name', 'class_name')
    list_filter = ('grade_level', 'class_name', 'is_verified')
    ordering = ('-date_updated',)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'gender', 'phone_number', 'position', 'address', 'is_verified', 'is_teacher', 'date_of_birth')
    
    search_fields = ('id', 'full_name', 'position')
    list_filter = ('position', 'is_verified', 'is_teacher')
    ordering = ('-date_updated',)
    list_per_page = 20


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'subject_taught', 'class_teacher', 'staff')
    
    search_fields = ('id', 'full_name', 'subjects_taught', 'class_teacher')
    list_filter = ('subject_taught', 'class_teacher')
    ordering = ('-staff__date_updated',)
    list_per_page = 20