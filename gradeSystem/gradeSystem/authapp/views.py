from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.views.generic.edit import UpdateView
from django.views.generic import TemplateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login, authenticate
from .forms import *
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



class MyProfileView(LoginRequiredMixin, View):
    def get(self, request, userid):
        # Check if the logged-in user is a superuser
        if request.user.is_superuser and request.user.id == userid:
            staff = Staff.objects.filter(user_id=userid).first()
            # Superuser viewing their own profile
            return render(request, 'authapp/my_profile.html', {
                'profile_user': request.user,
                'student': None,
                'staff': staff,
                'teacher': None,
            })

        # Get the student's profile
        student = Student.objects.filter(user_id=userid).first()
        staff = Staff.objects.filter(user_id=userid).first()
        teacher = None

        # If the user is a staff and is a teacher, get the teacher profile
        if staff and Teacher.objects.filter(staff=staff).exists():
            teacher = Teacher.objects.filter(staff=staff).first()
            
            # FOR DEBUG PURPOSE
            print("Teacher:", teacher)
            print("Subject Taught:", teacher.subject_taught if teacher else "N/A")
            print("Class Teacher:", teacher.class_teacher if teacher else "N/A")
            print("Class Names:", teacher.class_names.all() if teacher else "N/A")
        
        # Handle case where no matching profile is found
        if not student and not staff:
            return render(request, 'authapp/my_profile.html', {
                'profile_user': None,
                'student': None,
                'staff': None,
                'teacher': None,
                'error_message': "No profile found for the given user ID.",
            })

        return render(request, 'authapp/my_profile.html', {
            'profile_user': student.user if student else staff.user,
            'student': student,
            'staff': staff,
            'teacher': teacher,
        })

class AllStudentsView(LoginRequiredMixin, View):
    """ 
    For Viewing all Student
    """
    def get(self, request):
        students = Student.objects.all()
        staff = Staff.objects.all()
        return render(request, 'authapp/all_students.html', {'students': students, 'staff': staff})


class AllStudentSearchView(LoginRequiredMixin, View):
    
    """ 
    To Search Student Based filter query(filter b class_name e.g 7A, 8B)
    """
    
    def get(self, request):
        search_query = request.GET.get('search', '')
        if search_query:
            students = Student.objects.filter(class_name__icontains=search_query)
        else:
            students = Student.objects.all()  # Show all students if no search query is provided
            staff = Staff.objects.all()
        return render(request, 'authapp/all_students.html', {
            'students': students,
            'staff': staff,
            'search_query': search_query,  # Pass None if no search query
        })

class AllStaffView(LoginRequiredMixin, View):
    """ 
    For Viewing All Staff
    """
    
    def get(self, request):
        staff = Staff.objects.all()
        return render(request, 'authapp/all_staff.html', {'staff': staff}) 

class AllStaffSearchView(LoginRequiredMixin, View):
    """ 
    To search staff based on filter query(filter by staff role e.g Head of School, 
    
    Teacher, Bursar, Counsellor e.t.c)
    """
    
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
    
    """ 
    To View All Teachers
    """
    def get(self, request):
        
        teachers = Teacher.objects.all()  # Ensure staff is prefetched
        # for teacher in teachers:
        #     teacher.class_names_str = ", ".join([cls.name for cls in teacher.class_names.all()])
        return render(request, 'authapp/all_teachers.html', {'teachers': teachers})
        # teachers = Teacher.objects.all()
        # staff = Staff.objects.all()
        # return render(request, 'authapp/all_teachers.html', {'teachers': teachers, 'staff':staff})
    
class AllTeachersSearchView(LoginRequiredMixin, View):
    
    """ 
    Search Teacher Based on Filter Query(search by subject or class_name)
    """
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
            staff = Staff.objects.all()

        return render(request, 'authapp/all_teachers.html', {
            'teachers': teachers,
            'staff': staff,
            'search_query': search_query,
        })


# View for editing student information
class EditStudentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "authapp/edit_student.html"
    context_object_name = "student"

    def test_func(self):
        # Authorization logic for editing student information
        user = self.request.user
        if user.is_superuser:
            return True
        try:
            staff = Staff.objects.get(user=user)
            return staff.position in ["Head of School", "Ass Head of School"] or staff.is_teacher
        except Staff.DoesNotExist:
            return False

    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to edit student information.")
        return redirect("home")

    def form_valid(self, form):
        messages.success(self.request, "Student information updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return redirect("all_students").url  # Redirect to the student dashboard


# View for editing staff/teacher information
# class EditStaffOrTeacherView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Staff
#     template_name = "authapp/edit_staff_or_teacher.html"
#     context_object_name = "staff"
#     form_class = StaffForm  # Default
    
#     def test_func(self):
#         user = self.request.user
#         if user.is_superuser:
#             return True
#         try:
#             staff = Staff.objects.get(user=user)
#             return staff.position in ["Head of School", "Ass Head of School"]
#         except Staff.DoesNotExist:
#             return False

#     def get_form(self, form_class=None):
#         staff = self.get_object()
#         teacher = Teacher.objects.filter(staff=staff).first()
#         if teacher:
#             form_class = TeacherForm
#             return form_class(self.request.POST or None, instance=teacher)
#         else:
#             form_class = StaffForm
#             return form_class(self.request.POST or None, instance=staff)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         staff = self.get_object()
#         context['is_teacher'] = Teacher.objects.filter(staff=staff).exists()
#         context['form'] = self.get_form()  # Include the correct form instance
#         return context

#     def form_valid(self, form):
#         try:
#             instance = form.save(commit=False)
#             if isinstance(form, TeacherForm):
#                 instance.staff = self.get_object()
#                 instance.save()
#                 form.save_m2m()
#                 messages.success(self.request, f"Teacher {instance.full_name}'s information updated successfully.")
#             else:
#                 instance.save()
#                 messages.success(self.request, f"Staff {instance.full_name}'s information updated successfully.")
#             return redirect(self.get_success_url())
#         except Exception as e:
#             print("Error while saving the form:", str(e))
#             messages.error(self.request, f"An error occurred while saving the form: {str(e)}")
#             return self.form_invalid(form)

#     def get_success_url(self):
#         if self.object.user.is_teacher:
#             return reverse("all_teachers")
#         return reverse("all_staff")

#     def handle_no_permission(self):
#         messages.error(self.request, "You are not authorized to edit staff/teacher information.")
#         return redirect("home")


class EditStaffOrTeacherView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Staff
    template_name = "authapp/edit_staff_or_teacher.html"
    context_object_name = "staff"
    form_class = StaffForm  # Default form

    def test_func(self):
        user = self.request.user
        if user.is_superuser:
            return True
        try:
            staff = Staff.objects.get(user=user)
            return staff.position in ["Head of School", "Ass Head of School"]
        except Staff.DoesNotExist:
            return False

    # def get_form(self, form_class=None):
    #     staff = self.get_object()
    #     teacher = Teacher.objects.filter(staff=staff).first()

    #     # Determine the referring page
    #     referer = self.request.META.get('HTTP_REFERER', '')
    #     if "all_teachers" in referer: #and teacher:
    #         # Use TeacherForm if coming from the "All Teachers" page and the user is a teacher
    #         form_class = TeacherForm
    #         return form_class(self.request.POST or None, instance=teacher)
    #     else:
    #         # Use StaffForm otherwise
    #         form_class = StaffForm
    #         return form_class(self.request.POST or None, instance=staff)
    def get_form_class(self):
        edit_type = self.request.POST.get("edit_type") or self.request.GET.get("edit_type")
        if edit_type == "teacher":
            return TeacherForm
        return StaffForm

    def get_form(self, form_class=None):
        staff = self.get_object()
        if form_class is None:
            form_class = self.get_form_class()

        if form_class == TeacherForm:
            teacher = Teacher.objects.filter(staff=staff).first()
            return form_class(self.request.POST or None, instance=teacher)
        else:
            return form_class(self.request.POST or None, instance=staff)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = self.get_object()
        context['is_teacher'] = Teacher.objects.filter(staff=staff).exists()
        context['form'] = context.get('form')  # Include the correct form instance
        context['referer'] = self.request.META.get('HTTP_REFERER', '')
        return context

    def form_valid(self, form):
        try:
            instance = form.save(commit=False)
            if isinstance(form, TeacherForm):
                print("FORRMM:", form.cleaned_data)
                instance.staff = self.get_object()
                print("CLEANED FORRMM:", form.cleaned_data)
                instance.save()
                form.save_m2m()
                messages.success(self.request, f"Teacher {instance.full_name}'s information updated successfully.")
            else:
                instance.save()
                messages.success(self.request, f"Staff {instance.full_name}'s information updated successfully.")
            return redirect(self.get_success_url())
        except Exception as e:
            print("Error while saving the form:", str(e))
            messages.error(self.request, f"An error occurred while saving the form: {str(e)}")
            return self.form_invalid(form)

    # def get_success_url(self):
    #     staff = self.get_object()
    #     if Teacher.objects.filter(staff=staff).exists():
    #         return reverse("all_teachers")
    #     return reverse("all_staff")
    
    def get_success_url(self):
        edit_type = self.request.POST.get("edit_type") or self.request.GET.get("edit_type")
        if edit_type == "teacher":
            return reverse("all_teachers")
        return reverse("all_staff")
    
    def handle_no_permission(self):
        messages.error(self.request, "You are not authorized to edit staff/teacher information.")
        return redirect("home")