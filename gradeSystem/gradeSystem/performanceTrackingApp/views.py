from django.shortcuts import render
import json
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