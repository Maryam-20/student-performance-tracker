from django.shortcuts import render
import json
from django.db.models import Avg, Count, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from gradeSystem.authapp.models import *
from gradeSystem.gradingapp.models import *

# Create your views here.
class StudentPerformanceView(LoginRequiredMixin, View):
    def get(self, request, student_id):
        student = Student.objects.get(id=student_id)
        results = StudentResults.objects.filter(student=student).order_by('session__start_date', 'term__term_name')
        
        data = [
            {
                "session": result.session.session_name,
                "term": result.term.term_name,
                "score": result.average_score_in_percentage or 0
            }
            for result in results
        ]
        # data = [
            
        #     {'session': '2024/2025', 'term': 'First Term', 'score': 79.6},
        #     {'session': '2024/2025', 'term': 'Second Term', 'score': 85.2},
        #     {'session': '2024/2025', 'term': 'Third Term', 'score': 90.0}
            
        #     # for result in results
        # ]
        
        return render(request, 'performanceTrackingApp/student_performance.html', {
            'student': student,
            'performance_data': json.dumps(data),
        })


class ClassPerformanceView(LoginRequiredMixin, View):
    def get(self, request):
        # Get all classes for the dropdown
        all_classes = Classes.objects.all()
        class_id = request.GET.get('class_id')
        class_obj = None
        avg_per_term = []

        if class_id:
            class_obj = Classes.objects.get(id=class_id)
            results = StudentResults.objects.filter(class_name=class_obj).order_by('session__start_date', 'term__term_name')

            class_summary = {}
            for result in results:
                key = f"{result.session.session_name} {result.term.term_name}"
                class_summary.setdefault(key, []).append(result.average_score_in_percentage or 0)

            avg_per_term = [
                {
                    "period": key,
                    "average": round(sum(scores)/len(scores), 2) if scores else 0
                }
                for key, scores in class_summary.items()
            ]

        return render(request, 'performanceTrackingApp/class_performance.html', {
            'all_classes': all_classes,
            'class_obj': class_obj,
            'avg_per_term': json.dumps(avg_per_term),  # <-- ensure JSON string
            'selected_class_id': int(class_id) if class_id else None,
        })  
   
   
        
class AnalyticsReportView(LoginRequiredMixin, View):
    def get(self, request):
        # Top 5 students by average score
        top_students = StudentResults.objects.values(
            'student__full_name'
        ).annotate(
            avg_score=Avg('average_score_in_percentage')
        ).order_by('-avg_score')[:5]

        # Subjects with highest and lowest average scores
        subject_averages = SubjectScore.objects.values(
            'subject__subject_name'
        ).annotate(
            avg_score=Avg('total_score')
        ).order_by('-avg_score')

        highest_subject = subject_averages.first() if subject_averages else None
        lowest_subject = subject_averages.last() if subject_averages else None

        # Class averages per session/term
        class_averages = StudentResults.objects.values(
            'class_name__class_name', 'session__session_name', 'term__term_name'
        ).annotate(
            avg_score=Avg('average_score_in_percentage')
        ).order_by('class_name__class_name', 'session__session_name', 'term__term_name')

        # Pass/fail rates (assuming pass mark is 40%)
        total_results = StudentResults.objects.count()
        passed = StudentResults.objects.filter(average_score_in_percentage__gte=40).count()
        failed = total_results - passed
        pass_rate = (passed / total_results * 100) if total_results else 0
        fail_rate = (failed / total_results * 100) if total_results else 0

        return render(request, 'performanceTrackingApp/analytics_report.html', {
            'top_students': top_students,
            'highest_subject': highest_subject,
            'lowest_subject': lowest_subject,
            'class_averages': class_averages,
            'pass_rate': round(pass_rate, 2),
            'fail_rate': round(fail_rate, 2),
        })
        
class UnderperformingStudentsAlertView(LoginRequiredMixin, View):
    def get(self, request):
        # You can filter by session/term/class if needed
        threshold = 40  # Pass mark
        underperformers = StudentResults.objects.filter(
            average_score_in_percentage__lt=threshold
        ).select_related('student', 'class_name', 'term', 'session')

        return render(request, 'performanceTrackingApp/underperforming_alerts.html', {
            'underperformers': underperformers,
            'threshold': threshold,
        })