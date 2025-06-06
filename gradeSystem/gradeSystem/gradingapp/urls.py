# filepath: c:\performance_tracker\gradeSystem\gradeSystem\gradingapp\urls.py
from django.urls import path
from gradeSystem.gradingapp.views import *

urlpatterns = [
    path('student_dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    # path('check_results/', CheckResultsView.as_view(), name='check_results'),
    # path('check_scores/', CheckSubjectScoresView.as_view(), name='check_scores'),
    path('teacher_dashboard/', TeacherDashboardView.as_view(), name='teacher_dashboard'),
    path('teacher/subjects/', TeacherSubjectsView.as_view(), name='teacher_subjects'),
    path('teacher/enter_scores/<int:subject_id>/<int:class_id>/', EnterScoresView.as_view(), name='enter_scores'),
    path('broadsheet/', BroadsheetView.as_view(), name='broadsheet'),
    path('student_result/<int:result_id>/', StudentResultDetailView.as_view(), name='student_result_detail'),
    path('student/scores-and-result/', StudentScoresAndResultView.as_view(), name='student_scores_and_result'),
   
]