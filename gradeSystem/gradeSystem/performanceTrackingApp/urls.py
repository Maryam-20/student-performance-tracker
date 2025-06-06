from django.urls import path
from gradeSystem.performanceTrackingApp.views import StudentPerformanceView, ClassPerformanceView

urlpatterns = [
    path('student/performance/<int:student_id>/', StudentPerformanceView.as_view(), name='student_performance'),
    path('class/performance/', ClassPerformanceView.as_view(), name='class_performance'),
]