from django.urls import path
from .views import *


urlpatterns = [
    path('my_profile/<int:userid>/', MyProfileView.as_view(), name='my_profile'),
    path('all_students/', AllStudentsView.as_view(), name='all_students'),
    path('all_students/search/', AllStudentSearchView.as_view(), name='all_students_search'),
    path('all_staff/', AllStaffView.as_view(), name='all_staff'),
    path('all_staff/search/', AllStaffSearchView.as_view(), name='all_staff_search'),
    path('all_teachers/', AllTeachersView.as_view(), name='all_teachers'),
    path('all_teachers/search/', AllTeachersSearchView.as_view(), name='all_teachers_search'),
    path('edit_student/<int:pk>/', EditStudentView.as_view(), name='edit_student'),
    path('edit_staff_or_teacher/<int:pk>/', EditStaffOrTeacherView.as_view(), name='edit_staff_or_teacher'),
    # Add other URL patterns here as needed
]
