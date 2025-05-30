from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(AcademicSession)
class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('session_name', 'start_date', 'end_date')
    search_fields = ('session_name',)
    list_filter = ('start_date', 'end_date')
    ordering = ('-start_date',)
    
@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('term_name', 'start_date', 'end_date', 'session')
    search_fields = ('term_name', 'session__session_name')
    list_filter = ('start_date', 'end_date', 'session')
    ordering = ('-start_date',)
    
@admin.register(Classes)
class ClassesAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_teacher', 'no_of_students', 'session', 'term', 'date_created')
    search_fields = ('class_name', 'class_teacher__full_name')
    list_filter = ('session', 'term')
    ordering = ('-date_created',)
    list_per_page = 20
    
@admin.register(JnrClasses)
class JnrClassesAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'no_of_students', 'no_of_subjects_offered', 'session', 'term')
    filter_horizontal = ('subjects_offered',)  # Enable a multi-select widget for subjects
    search_fields = ('class_name', 'class_teacher__full_name')
    list_filter = ('session', 'term')
    ordering = ('-date_created',)
    list_per_page = 20
    
@admin.register(SnrClasses)
class SnrClassesAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'class_teacher', 'no_of_students', 'session', 'term', 'department', 'subjects_offered', 'no_of_subjects_offered', 'date_created')
    search_fields = ('class_name', 'class_teacher__full_name')
    list_filter = ('session', 'term')
    ordering = ('-date_created',)
    list_per_page = 20
    
@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ('subject_name',  'session', 'term', 'date_created')
    search_fields = ('subject_name',)
    list_filter = ('session', 'term', 'teachers')
    list_per_page = 20


@admin.register(SubjectTeacherAssignment)
class SubjectTeacherAssignmentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'teacher', 'class_name', 'session', 'term', 'date_assigned')
    search_fields = ('subject__subject_name', 'teacher__full_name', 'class_name__class_name')
    list_filter = ('session', 'term', 'subject')
    
@admin.register(SubjectScore)
class SubjectScoreAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'first_ca', 'second_ca', 'total_ca', 'exam_score', 'total_score', 'total_score_in_percentage', 'grade', 'term', 'session')
    search_fields = ('student__full_name', 'subject__subject_name', 'term__term_name', 'session__session_name')
    list_filter = ('term', 'session', 'subject')
    ordering = ('-session__start_date',)
    list_per_page = 20
    
@admin.register(StudentResults)
class StudentResultsAdmin(admin.ModelAdmin):
    list_display = ('student', 'term', 'session', 'total_score_obtainable', 'total_score_in_all_subjects', 'average_score', 'average_score_in_percentage', 'class_position')
    search_fields = ('student__full_name', 'term__term_name', 'session__session_name')
    list_filter = ('student', 'term', 'session')
    ordering = ('-session__start_date',)
    list_per_page = 20