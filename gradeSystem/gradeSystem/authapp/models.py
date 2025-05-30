from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from gradeSystem.gradingapp.models import Classes
# Create your models here.
gender_choices = (("Male", "Male"),
                  ("Female", "Female"),)


grade_level_choices = (("Year 7", "Year 7"),
                 ("Year 8", "Year 8"),
                 ("Year 9", "Year 9"),
                 ("Year 10", "Year 10"),
                 ("Year 11", "Year 11"),
                 ("Year 12", "Year 12"),
                 ("Subject Teacher", "Subject Teacher"),
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


class AllUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        # if 'date_of_birth' not in extra_fields or not extra_fields['date_of_birth']:
        #     raise ValueError('The Date of Birth field must be set')
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
    
    """
    Override the Django's User's Model
     
    """
    
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
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
    """
    Student Table     
    """
    id = models.BigAutoField( primary_key=True)  
    user = models.OneToOneField(AllUser, on_delete=models.CASCADE, null=True, blank=True)  
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    grade_level = models.CharField(choices=grade_level_choices, max_length=50, null=True, blank=False) #Current grade level
    class_name = models.ForeignKey(
            Classes,
            on_delete=models.CASCADE,
            related_name="students",
            null=False,
            
        )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    date_updated = models.DateField(auto_now=True)
    
    def __str__(self):
        return f"{self.full_name} - {self.id}"
    
        
    
class Staff(models.Model):
    
    """
    Staff Table     
    """
    
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(AllUser, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    position = models.CharField(choices=position_choices, max_length=100, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)  
    date_updated = models.DateField(auto_now=True)
    
    date_of_birth = models.DateField(null=True, blank=True)
  
    
    USERNAME_FIELD = 'email'
    
    def __str__(self):
        return f"{self.full_name} - {self.id}"
    

class Teacher(models.Model):
    
    """
    Teacher's Table     
    """
    
    id = models.BigAutoField( primary_key=True)
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=False, blank=False)
    gender = models.CharField(choices=gender_choices, max_length=10, null=False, blank=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    subject_taught = models.CharField(choices=subject_choices, max_length=100, null=True)
    class_teacher = models.CharField(choices=grade_level_choices,  max_length=50, null=True)
    class_names = models.ManyToManyField('gradingapp.Classes', related_name= "teachers")
    date_updated = models.DateField(auto_now=True)


    def __str__(self):
        return f"{self.full_name} - {self.subject_taught}"
    

@receiver(post_save, sender=AllUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:  # Create a Staff Instance Table
            Staff.objects.create(
                user=instance,
                full_name=instance.get_full_name(),
            )
        else:  # Create Student Instance Table
             
            # Dynamically assign a default class
            default_class, _ = Classes.objects.get_or_create(
                class_name="Default Class",
                defaults={'no_of_students': 0, 'date_created': now()}
            )
            Student.objects.create(
                user=instance,
                full_name=instance.get_full_name(),
                class_name=default_class,  # Assign the default class
                
            )
    else:
        # Handle updates to is_staff
        if instance.is_staff:
            # If the user is now a staff, delete the Student profile (if it exists)
            Student.objects.filter(user=instance).delete()
            # Create a Staff profile if it doesn't already exist
            Staff.objects.get_or_create(
                user=instance,
                defaults={'full_name': instance.get_full_name()},
            )
        else:
            # If the user is now a student, delete the Staff profile (if it exists)
            Staff.objects.filter(user=instance).delete()
            # Create a Student profile if it doesn't already exist
            default_class, _ = Classes.objects.get_or_create(
                class_name="Default Class",
                defaults={'no_of_students': 0, 'date_created': now()}
            )
            Student.objects.get_or_create(
                user=instance,
                defaults={
                    'full_name': instance.get_full_name(),
                    'class_name': default_class,
                },
            )

@receiver(post_save, sender=AllUser)
def create_or_update_teacher_profile(sender, instance, created, **kwargs):
    if created:
        # If the user is created and is a teacher, ensure a Staff profile exists first
        if instance.is_teacher:
            staff, _ = Staff.objects.get_or_create(
                user=instance,
                defaults={'full_name': instance.get_full_name()},
            )
            Teacher.objects.create(
                staff=staff,
                full_name=staff.full_name,
                gender=staff.gender,
                phone_number=staff.phone_number,
                # date_of_birth=staff.date_of_birth,
            )
    else:
        # If the user is updated to a teacher, ensure a Teacher profile exists
        if instance.is_teacher:
            staff = Staff.objects.filter(user=instance).first()
            if staff:
                Teacher.objects.get_or_create(
                    staff=staff,
                    defaults={
                        'full_name': staff.full_name,
                        'gender': staff.gender,
                        'phone_number': staff.phone_number,
                        # 'date_of_birth': staff.date_of_birth,
                    },
                )
        else:
            # If the user is no longer a teacher, delete the Teacher profile (if it exists)
            Teacher.objects.filter(staff__user=instance).delete()