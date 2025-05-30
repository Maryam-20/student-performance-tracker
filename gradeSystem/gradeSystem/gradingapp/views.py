from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from gradeSystem.authapp.models import *
from gradeSystem.gradingapp.forms import *
from django.views import View
from django.contrib import messages

# Create your views here.
class StudentDashboardView(LoginRequiredMixin, View):
    
    """ 
    Student Dashboard Logic
    
    """
    def get(self, request):
        try:
            # Get the logged-in student's information
            student = Student.objects.get(user=request.user)

            # Get the student's subject scores and results
            # subjects_scores = SubjectScore.objects.filter(student=student)
            # student_results = StudentResults.objects.filter(student=student)

            return render(request, 'gradingapp/student_dashboard.html', {
                'student': student,
                # 'subjects_scores': subjects_scores,
                # 'student_results': student_results,
            })
        except Student.DoesNotExist:
            return render(request, 'gradingapp/student_dashboard.html', {
                'error': 'You are not a student.',
            })

class TeacherDashboardView(LoginRequiredMixin, View):
    
    """
    Teacher's Dashboard Logic
    """
    
    def get(self, request):
        try:
            # Get the logged-in teacher's staff profile
            staff = Staff.objects.get(user=request.user)
            if not staff.user.is_teacher:
                return redirect('home')  # Redirect non-teachers to the home page

            # Get the teacher profile
            teacher = Teacher.objects.get(staff=staff)
            print("Teacher", teacher)

            # Get the subjects and classes assigned to the teacher
            assignments = SubjectTeacherAssignment.objects.filter(teacher=teacher)

            return render(request, 'gradingapp/teacher_dashboard.html', {
                'teacher': teacher,
                'assignments': assignments,
            })
        except (Staff.DoesNotExist, Teacher.DoesNotExist):
            return redirect('home')  # Redirect if the user is not a teacher



class TeacherSubjectsView(LoginRequiredMixin, View):
    
    """ 
    Logic for a teacher to know the subject and the class  they are assigned to teach
    """
    
    def get(self, request):
        try:
            # Get the logged-in teacher's assignments
            staff = Staff.objects.get(user=request.user)
            teacher = Teacher.objects.get(staff=staff)
            assignments = SubjectTeacherAssignment.objects.filter(teacher=teacher)

            return render(request, 'gradingapp/teacher_subjects.html', {
                'teacher': teacher,
                'assignments': assignments,
            })
        except (Staff.DoesNotExist, Teacher.DoesNotExist):
            return redirect('home')



class EnterScoresView(LoginRequiredMixin, View):
    
    """ 
    Logic for a Subject Teacher to Enter Students of  a class score in the subject
    
    """
    
    def get(self, request, subject_id, class_id):
        try:
            # Get the subject and class
            subject = Subjects.objects.get(id=subject_id)
            class_name = Classes.objects.get(id=class_id)
            print("Class name:", class_name ,"\n" "Subject id: ", subject)
            students = Student.objects.filter(class_name=class_name)
            print("Students:", students)

            scores = {
            score.student.id: score for score in SubjectScore.objects.filter(
                class_name=class_name,
                subject=subject,
                term=class_name.term,
                session=class_name.session
            )
            }

            return render(request, 'gradingapp/enter_scores.html', {
                'subject': subject,
                'class_name': class_name,
                'students': students,
                'scores': scores
            })

        except (Subjects.DoesNotExist, Classes.DoesNotExist):
            messages.error(request, "Invalid subject or class.")
            return redirect('teacher_dashboard')

    def post(self, request, subject_id, class_id):
        try:
            # Get the subject and class
            subject = Subjects.objects.get(id=subject_id)
            class_name = Classes.objects.get(id=class_id)
            students = Student.objects.filter(class_name=class_name)

            for student in students:
                # Get or create the SubjectScore instance for the student
                score, created = SubjectScore.objects.get_or_create(
                    student=student,
                    class_name=class_name,
                    subject=subject,
                    term=class_name.term,
                    session=class_name.session,
                )

                # Update scores if provided
                first_ca = request.POST.get(f'first_ca_{student.id}')
                second_ca = request.POST.get(f'second_ca_{student.id}')
                exam_score = request.POST.get(f'exam_score_{student.id}')

                # Validate scores
                if first_ca:
                    first_ca = float(first_ca)
                    if first_ca > 20:
                        messages.error(request, f"First CA score for {student.full_name} cannot exceed 20.")
                        return redirect(request.path)
                    score.first_ca = first_ca

                if second_ca:
                    second_ca = float(second_ca)
                    if second_ca > 20:
                        messages.error(request, f"Second CA score for {student.full_name} cannot exceed 20.")
                        return redirect(request.path)
                    score.second_ca = second_ca

                if exam_score:
                    exam_score = float(exam_score)
                    if exam_score > 90:
                        messages.error(request, f"Exam score for {student.full_name} cannot exceed 90.")
                        return redirect(request.path)
                    score.exam_score = exam_score

                # Compute total scores only if all fields are filled
                # if score.first_ca is not None and score.second_ca is not None and score.exam_score is not None:
                #     score.save()  # This will trigger the `save` method in the model to compute totals
                score.save()
            messages.success(request, "Scores have been successfully submitted.")
           # Redirect to the broadsheet page with filters applied
            return redirect(f'/school-portal/v1/grading/broadsheet/?class_name={class_id}&subject={subject_id}&term={class_name.term.id}&session={class_name.session.id}')
        except (Subjects.DoesNotExist, Classes.DoesNotExist):
            messages.error(request, "An error occurred while submitting scores.")
            return redirect('teacher_dashboard')    
 
 
class BroadsheetView(LoginRequiredMixin, View):
    
    """
    Broadsheet Page Logic
     
    """
    
    def get(self, request):
        # Get filter parameters from the request
        class_name_id = request.GET.get('class_name')
        term_id = request.GET.get('term')
        session_id = request.GET.get('session')
        subject_id = request.GET.get('subject')

        # Filter the SubjectScore queryset based on the filters
        scores = SubjectScore.objects.all()

        if class_name_id:
            scores = scores.filter(class_name_id=class_name_id)
        if term_id:
            scores = scores.filter(term_id=term_id)
        if session_id:
            scores = scores.filter(session_id=session_id)
        if subject_id:
            scores = scores.filter(subject_id=subject_id)

        # Get all filter options for the dropdowns
        classes = Classes.objects.all()
        terms = Term.objects.all()
        sessions = AcademicSession.objects.all()
        subjects = Subjects.objects.all()

        return render(request, 'gradingapp/broadsheet.html', {
            'scores': scores,
            'classes': classes,
            'terms': terms,
            'sessions': sessions,
            'subjects': subjects,
        })
  
  
        
class CheckResultsView(LoginRequiredMixin, View):
    def get(self, request):
        # Logic for checking results can go here
        student = Student.objects.get(user=request.user)
        student_results = StudentResults.objects.filter(student=student)
        return render(request, 'gradingapp/check_results.html')


class CheckSubjectScoresView(LoginRequiredMixin, View):
    def get(self, request):
        # Logic for checking scores can go here
        student = Student.objects.get(user=request.user)
        subjects_scores = SubjectScore.objects.filter(student=student)
        return render(request, 'gradingapp/check_scores.html')
     
class SubjectScoreEntryView(LoginRequiredMixin, View):
    def get(self, request, subject_id=None, class_id=None):
        try:
            # Check if the logged-in user is a teacher
            staff = Staff.objects.get(user=request.user)
            if staff.user.is_teacher:
                if subject_id and class_id:
                    subject = Subjects.objects.get(id=subject_id)
                    class_name = Classes.objects.get(id=class_id)
                    students = Student.objects.filter(class_name=class_name)
                    form = SubjectScoreForm(initial={'subject': subject, 'class_name': class_name})
                    return render(request, 'gradingapp/subject_score_entry.html', {'form': form, 'students': students})
                else:
                    subjects = Subjects.objects.filter(teachers=staff.teacher)
                    return render(request, 'gradingapp/teacher_dashboard.html', {'subjects': subjects})
            else:
                return redirect('home')  # Redirect non-teachers to the home page or another view
        except Staff.DoesNotExist:
            return redirect('home')  # Redirect if the user is not a staff member

    def post(self, request, subject_id=None, class_id=None):
        try:
            staff = Staff.objects.get(user=request.user)
            if staff.user.is_teacher:
                if subject_id and class_id:
                    subject = Subjects.objects.get(id=subject_id)
                    class_name = Classes.objects.get(id=class_id)
                    form = SubjectScoreForm(request.POST)
                    if form.is_valid():
                        form.save()
                        return redirect('teacher_dashboard')  # Redirect to the teacher's dashboard
                    students = Student.objects.filter(class_name=class_name)
                    return render(request, 'gradingapp/subject_score_entry.html', {'form': form, 'students': students})
                else:
                    return redirect('home')  # Redirect non-teachers to the home page or another view
        except Staff.DoesNotExist:
            return redirect('home')  # Redirect if the user is not a staff member