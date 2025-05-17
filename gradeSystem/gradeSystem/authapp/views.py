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
    