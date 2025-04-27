from django.db import models

# Create your models here.
gender_choices = (("Male", "Male"),
                  ("Female", "Female"),)


class_choices = (("1st Year", "1st Year"),
                 ("2nd Year", "2nd Year"),
                 ("3rd Year", "3rd Year"),
                 ("4th Year", "4th Year"),)

subject_choices = (("Mathematics", "Mathematics"),
                   ("Science", "Science"),
                   ("English", "English"),
                   ("History", "History"),
                   ("Geography", "Geography"),
                   ("Computer Science", "Computer Science"),
                   ("Physical Education", "Physical Education"),
                   ("Art", "Art"),
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
                   ("Foreign Language", "Foreign Language"),)

position_choices = (("Principal", "Principal"),
                    ("Vice Principal", "Vice Principal"),
                    ("Head of Department", "Head of Department"),
                    ("Teacher", "Teacher"),
                    ("Counselor", "Counselor"),
                    ("Librarian", "Librarian"),
                    ("Administrator", "Administrator"),
                        )
    
class Student(models.Model):
    
    id = models.CharField(max_length=10, primary_key=True),    
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    class_name = models.CharField(choices=class_choices, max_length=50, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    address = models.CharField(max_length=200, null=False, blank=False)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    date_registered = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.full_name} - {self.id}"
    
    
    
class Staff(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    position = models.CharField(choices=position_choices, max_length=100, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)  
    date_registered = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.id}"

class Teacher(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    subject_taught = models.CharField(choices=subject_choices, max_length=100, null=True)
    date_of_birth = models.DateField()
    class_teacher = models.CharField(choices=class_choices, max_length=50, null=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_registered = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.full_name} - {self.id}"