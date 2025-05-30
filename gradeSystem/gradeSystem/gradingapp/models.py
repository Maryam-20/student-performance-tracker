from django.db import models
from gradeSystem.authapp.models import *

# Create your models here.
Grade = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('F', 'F'),
    )
Department_choices = (
                    ("Science", "Secience"),
                    ("Art", "Art"),
                    ("Commercial", "Commercial"),
                    )

class AcademicSession(models.Model):
    session_name = models.CharField(max_length=20, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.session_name


class Term(models.Model):
    term_choices = (
        ('First Term', 'First Term'),
        ('Second Term', 'Second Term'),
        ('Third Term', 'Third Term'),
    )
    term_name = models.CharField(max_length=20, choices=term_choices, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('term_name', 'session')

    def __str__(self):
        return f'{self.session.session_name} - {self.get_term_name_display()}'


class Classes(models.Model):
    class_name = models.CharField(max_length=50, unique=True, db_index=True) #THIS SHOULDN'T BE UNIQUE
    class_teacher = models.ForeignKey('authapp.Teacher', on_delete=models.CASCADE, null=True, blank=True, db_index=True)
    no_of_students = models.IntegerField(default=0)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, null=True, blank=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        teacher_name = self.class_teacher.full_name if self.class_teacher else "No Teacher Assigned"
        return f'{self.class_name} - {teacher_name}'


class JnrClasses(Classes):
    subjects_offered = models.ManyToManyField('Subjects', related_name='jnr_classes', blank=True)
    no_of_subjects_offered = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Save the instance first to ensure it has a primary key
        super().save(*args, **kwargs)
        # Update the number of subjects offered
        self.no_of_subjects_offered = self.subjects_offered.count()
        # Save again to persist the updated field
        super().save(update_fields=['no_of_subjects_offered'])

class SnrClasses(Classes):
    department = models.CharField(choices=Department_choices, max_length=50, null=True, blank=True)
    subjects_offered = models.CharField(max_length=500, null=True, blank=True)
    no_of_subjects_offered = models.IntegerField(default=0)
    
        
class Subjects(models.Model):
    
    """ 
    Table to declare the subjects the school offer 
    """
    subject_choices = (("Mathematics", "Mathematics"),
                     ("English Language", "English Language"),
                   ("History", "History"),
                   ("Geography", "Geography"),
                   ("Computer Science", "Computer Science"),
                   ("Music", "Music"),
                   ("Economics", "Economics"),
                   ("Psychology", "Psychology"),
                    ("Sociology", "Sociology"),
                   ("Philosophy", "Philosophy"),
                   ("Business Studies", "Business Studies"),
                   ("Accounting", "Accounting"),
                   ("Statistics", "Statistics"),
                   ("Chemistry", "Chemistry"),
                   ("Physics", "Physics"),
                   ("Biology", "Biology"),
                   ("Literature", "Literature"),
                   ("Government", "Government"),
                   ("Civic Education", "Civic Education"),
                   ("Agricultural Science", "Agricultural Science"),
                   ("Technical Drawing", "Technical Drawing"),
                   ("Fine Arts", "Fine Arts"),
                   ("Physical and Health Education", "Physical and Health Education"),
                   ("Home Economics", "Home Economics"),
                   ("Food and Nutrition", "Food and Nutrition"),
                   ("Foreign Language", "Foreign Language"),)
    
    subject_name = models.CharField(max_length=50, choices=subject_choices, db_index=True)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE, null=True, blank=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE, null=True, blank=True)
    teachers = models.ManyToManyField('authapp.Teacher', through='SubjectTeacherAssignment', related_name='subjects')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject_name} - {self.session.session_name if self.session else "No Session"} - {self.term.term_name if self.term else "No Term"}'

class SubjectTeacherAssignment(models.Model):
    """  
    Assign a Teacher to a Subject Per class
    """
    
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey('authapp.Teacher', on_delete=models.CASCADE, related_name='assignments')
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name='subject_assignments')
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.subject.subject_name} - {self.teacher.full_name} - {self.class_name.class_name}'
    
    
class SubjectScore(models.Model):
    
    """ 
    Table for Student of a class scores in a subject Per term and session
    """
    
    student = models.ForeignKey('authapp.Student', on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    first_ca = models.FloatField(null=True, blank=True) # Continuous Assessment 1 carries 20marks
    second_ca = models.FloatField(null=True, blank=True) # Continuous Assessment 2 carries 20marks
    total_ca = models.FloatField(null=True, blank=True) # Toatl Continuos Assessment carries 40marks. total_ca = first_ca + second_ca
    exam_score = models.FloatField(null=True, blank=True) # Exam score carries 90marks
    total_score = models.FloatField(null=True, blank=True) #Total Score carries 130marks. total_ca + exam_score
    total_score_in_percentage = models.FloatField(null=True, blank=True) #total_score / 130 * 100
    grade = models.CharField(choices=Grade, max_length=2, null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    date_submitted = models.DateField(auto_now_add=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['student', 'class_name']),  # Composite index on student and class_name
            models.Index(fields=['term', 'session']),  # Composite index on term and session
        ]
        unique_together = ('student', 'subject', 'term', 'session')  # Ensure unique scores per student, subject, term, and session

    def __str__(self):
        return f'{self.student.full_name} - {self.subject.subject_name} - {self.term.term_name} - {self.session.session_name}'
    
    def save(self, *args, **kwargs):
        if self.first_ca is not None and self.second_ca is not None and self.exam_score is not None:
            self.total_ca = self.first_ca + self.second_ca
            self.total_score = self.total_ca + self.exam_score
            self.total_score_in_percentage = (self.total_score / 130) * 100
            if self.total_score_in_percentage >= 70:
                self.grade = 'A'
                self.remark = 'Excellent'
            elif 60 <= self.total_score_in_percentage < 70:
                self.grade = 'B'
                self.remark = 'Very Good'
            elif 50 <= self.total_score_in_percentage < 60:
                self.grade = 'C'
                self.remark = 'Good'
            elif 45 <= self.total_score_in_percentage < 50:
                self.grade = 'D'
                self.remark = 'Fair'
            elif 40 <= self.total_score_in_percentage < 45:
                self.grade = 'E'
                self.remark = 'Pass'
            else:
                self.grade = 'F'
                self.remark = 'Fail'
        else:
        # Reset calculated fields if incomplete
            self.total_ca = None
            self.total_score = None
            self.total_score_in_percentage = None
            self.grade = None
            self.remark = None
            
        super().save(*args, **kwargs)
    
class StudentResults(models.Model):
    student = models.ForeignKey('authapp.Student', on_delete=models.CASCADE)
    class_name = models.ForeignKey(Classes, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(SubjectScore)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    total_score_obtainable = models.FloatField(null=True, blank=True) #total_score_obtainable = 130 * no_of_subjects
    total_score_in_all_subjects = models.FloatField(null=True, blank=True) #Addition of all subject total scores
    average_score = models.FloatField(null=True, blank=True) #total_score_in_all_subjects / total_score_obtainable
    average_score_in_percentage = models.FloatField(null=True, blank=True) #average_score * 100
    class_position = models.CharField(null=True, blank=True)
    remark = models.CharField(max_length=100, null=True, blank=True)
    class_teacher_comment = models.TextField(null=True, blank=True)
    principal_comment = models.TextField(null=True, blank=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.student.full_name} - {self.average_score_in_percentage} - {self.term.term_name}'
    
    def save(self, *args, **kwargs):
        if self.subjects.exists():
            self.total_score_obtainable = 130 * self.subjects.count()
            self.total_score_in_all_subjects = sum([subject.total_score for subject in self.subjects.all()])
            self.average_score= self.total_score_in_all_subjects / self.total_score_obtainable
            self.average_score_in_percentage = self.average_score  * 100
        super().save(*args, **kwargs)