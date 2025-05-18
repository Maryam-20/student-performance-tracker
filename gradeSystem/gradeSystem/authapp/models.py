from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
# Create your models here.
gender_choices = (("Male", "Male"),
                  ("Female", "Female"),)


grade_level_choices = (("Year 7", "Year 7"),
                 ("Year 8", "Year 8"),
                 ("Year 9", "Year 9"),
                 ("Year 10", "Year 10"),
                 ("Year 11", "Year 11"),
                 ("Year 12", "Year 12"),
                 )

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


position_choices = (("Head of School", "Heaad of School"),
                    ("Ass Head of School", "Ass Head of School"),
                    ("Head of Department", "Head of Department"),
                    ("Teacher", "Teacher"),
                    ("Counselor", "Counselor"),
                    ("Librarian", "Librarian"),
                    ("Administrator", "Administrator"),
                    ("Bursar", "Bursar"),
                        )
# filepath: c:\performance_tracker\gradeSystem\gradeSystem\authapp\models.py


class AllUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class AllUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)

    objects = AllUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name
       
class Student(models.Model):
    id = models.CharField(max_length=10, primary_key=True)  
    user = models.OneToOneField(AllUser, on_delete=models.CASCADE, null=True, blank=True)  
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    grade_level = models.CharField(choices=grade_level_choices, max_length=50, null=True, blank=False) #Current grade level
    class_name = models.CharField(max_length=50, null=True, blank=False) #Current class
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=100)
    # date_registered = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    # is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    
    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['full_name', 'phone_number', 'gender',  'address', 'date_of_birth']

    def __str__(self):
        return f"{self.full_name} - {self.id}"
    
        
    
class Staff(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    user = models.OneToOneField(AllUser, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    position = models.CharField(choices=position_choices, max_length=100, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)  
    # date_registered = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    # password = models.CharField(max_length=100)
    # is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False) 
    date_of_birth = models.DateField(null=True, blank=True)
    # email = models.EmailField(unique=True)
    
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['full_name', 'phone_number', 'gender',  'address', 'date_of_birth']
    
    def __str__(self):
        return f"{self.full_name} - {self.id}"
    

class Teacher(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, null=True, blank=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    subject_taught = models.CharField(choices=subject_choices, max_length=100, null=True)
    date_of_birth = models.DateField()
    class_teacher = models.CharField(max_length=50, null=True)
    # email = models.EmailField(unique=True)
    # password = models.CharField(max_length=10)
    # is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    # date_registered = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.full_name} - {self.id}"
    

@receiver(post_save, sender=AllUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:  # staff registration
            Staff.objects.create(user=instance,
                                 full_name=instance.get_full_name(), 
                                 email=instance.email,
                                 date_of_birth=instance.date_joined.date()
                                )
        else:  # student registration
            Student.objects.create(
                user=instance,
                full_name=instance.get_full_name(),
                date_of_birth=instance.date_joined.date()
                )


@receiver(post_save, sender=Staff)        
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.is_teacher:  # Check if the staff is a teacher
        Teacher.objects.create(staff=instance)