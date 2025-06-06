from django.shortcuts import render, redirect, get_object_or_404
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
            
            student_results = StudentResults.objects.filter(student=student).order_by('-session__start_date', '-term__start_date')
            latest_result = student_results.first()  # This will be None if 
            # Get the student's subject scores and results
            # subjects_scores = SubjectScore.objects.filter(student=student)
            # student_results = StudentResults.objects.filter(student=student)

            return render(request, 'gradingapp/student_dashboard.html', {
                'student': student,
                'student_results': student_results,
                'result': latest_result,  # Pass the latest result (can be None)
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
            
            # Now check if all subjects are entered for this student
                subjects_offered = []
                if hasattr(class_name, 'jnrclasses'):
                    subjects_offered = class_name.jnrclasses.subjects_offered.all()
                subject_scores = SubjectScore.objects.filter(
                    student=student,
                    class_name=class_name,
                    term=class_name.term,
                    session=class_name.session,
                    subject__in=subjects_offered,
                    total_score__isnull=False
                )
                if subjects_offered and subject_scores.count() == subjects_offered.count():
                    student_result, created = StudentResults.objects.get_or_create(
                        student=student,
                        class_name=class_name,
                        term=class_name.term,
                        session=class_name.session,
                    )
                    # if created:
                    student_result.save()  # Save immediately if just created
                    # At this point, student_result.id is guaranteed to exist
                    student_result.subjects.set(subject_scores)
                    student_result.save()
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
    
    def get(self, request, subject_id=None, class_id=None):
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
  



class StudentResultDetailView(LoginRequiredMixin, View):
    def get(self, request, result_id):
        result = get_object_or_404(StudentResults, id=result_id)
        # Optionally, restrict access to only the student or staff
        # if request.user != result.student.user and not request.user.is_staff:
        #     return HttpResponseForbidden()
        return render(request, 'gradingapp/student_result_detail.html', {'result': result})  


class StudentScoresAndResultView(LoginRequiredMixin, View):
    def get(self, request):
        student = Student.objects.get(user=request.user)
        # Get current class, term, session (customize as needed)
        class_name = student.class_name
        term = class_name.term
        session = class_name.session

        # Subjects offered by the class (junior)
        subjects_offered = []
        if hasattr(class_name, 'jnrclasses'):
            subjects_offered = class_name.jnrclasses.subjects_offered.all()

        # Subject scores for this student
        subject_scores = SubjectScore.objects.filter(
            student=student,
            class_name=class_name,
            term=term,
            session=session,
            subject__in=subjects_offered
        )

        # Student result for this class/term/session
        student_result = StudentResults.objects.filter(
            student=student,
            class_name=class_name,
            term=term,
            session=session
        ).first()

        return render(request, 'gradingapp/student_scores_and_result.html', {
            'subject_scores': subject_scores,
            'student_result': student_result,
            'subjects_offered': subjects_offered,
            'class_name': class_name,
            'term': term,
            'session': session,
            'student': student,
        })   
        
        
        