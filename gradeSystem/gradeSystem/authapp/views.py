from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
# from django.views import View
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.views import generic, View
from django.contrib.auth import get_user_model
from .models import AllUser, Staff, Student, Teacher
from django.db import models

# Create your views here.

class SignupView(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = "registration/signup.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)



class myProfileView(LoginRequiredMixin, View):
    def get(self, request, userid):
        student = Student.objects.all().filter(user_id=userid)
        staff = Staff.objects.all().filter(user_id=userid)
        teacher = Teacher.objects.all().filter(staff_id=userid)
        return render(request, 'authapp/my_profile.html', {'student': student, 'staff': staff, 'teacher': teacher})


class AllStudentsView(LoginRequiredMixin, View):
    def get(self, request):
        students = Student.objects.all()
        return render(request, 'authapp/all_students.html', {'students': students})


class AllStudentSearchView(LoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            students = Student.objects.filter(class_name__icontains=search_query)
        else:
            students = Student.objects.all()  # Show all students if no search query is provided

        return render(request, 'authapp/all_students.html', {
            'students': students,
            'search_query': search_query,  # Pass None if no search query
        })

class AllStaffView(LoginRequiredMixin, View):
    def get(self, request):
        staff = Staff.objects.all()
        return render(request, 'authapp/all_staff.html', {'staff': staff}) 

class AllStaffSearchView(LoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            staff = Staff.objects.filter(position__icontains=search_query)
        else:
            staff = Staff.objects.all()  # Show all staff if no search query is provided

        return render(request, 'authapp/all_staff.html', {
            'staff': staff,
            'search_query': search_query,
        })
    
class AllTeachersView(LoginRequiredMixin, View):
    def get(self, request):
        teachers = Teacher.objects.all()
        return render(request, 'authapp/all_teachers.html', {'teachers': teachers})
    
class AllTeachersSearchView(LoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get("search", "").strip()
        if search_query:
            # Search by subject taught or class teacher
            teachers = Teacher.objects.filter(
                models.Q(subject_taught__icontains=search_query) |
                models.Q(class_name__icontains=search_query)
            )
        else:
            teachers = Teacher.objects.all()  # Show all teachers if no search query is provided

        return render(request, 'authapp/all_teachers.html', {
            'teachers': teachers,
            'search_query': search_query,
        })

