from django import forms
from gradeSystem.gradingapp.models import *

# class SubjectScoreForm(forms.ModelForm):
#     class Meta:
#         model = SubjectScore
#         fields = ['student', 'class_name', 'subject', 'term', 'session', 'first_ca', 'second_ca', 'exam_score']
#         widgets = {
#             'class_name': forms.HiddenInput(),
#             'subject': forms.HiddenInput(),
#         }
        
# class SubjectTeacherAssignmentForm(forms.ModelForm):
#     class Meta:
#         model = SubjectTeacherAssignment
#         fields = ['subject', 'teacher', 'class_name', 'session', 'term']
#         widgets = {
#             'subject': forms.Select(attrs={'class': 'form-control'}),
#             'teacher': forms.Select(attrs={'class': 'form-control'}),
#             'class_name': forms.Select(attrs={'class': 'form-control'}),
#             'session': forms.Select(attrs={'class': 'form-control'}),
#             'term': forms.Select(attrs={'class': 'form-control'}),
#         }        