from django.urls import path
from gradeSystem.performanceTrackingApp.views import *

urlpatterns = [
    path('student/performance/<int:student_id>/', StudentPerformanceView.as_view(), name='student_performance'),
    path('class/performance/', ClassPerformanceView.as_view(), name='class_performance'),
    path('analytics/', AnalyticsReportView.as_view(), name='analytics_report'),
    path('alerts/underperforming/', UnderperformingStudentsAlertView.as_view(), name='underperforming_alerts'),
]