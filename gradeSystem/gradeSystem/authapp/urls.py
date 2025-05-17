from django.urls import path
from .views import *


urlpatterns = [
    path('my_profile/<int:userid>/', myProfileView.as_view(), name='my_profile'),
    path('all_students/', AllStudentsView.as_view(), name='all_students'),
    path('all_students/search/', AllStudentSearchView.as_view(), name='all_students_search'),
    path('all_staff/', AllStaffView.as_view(), name='all_staff'),
    path('all_staff/search/', AllStaffSearchView.as_view(), name='all_staff_search'),
    path('all_teachers/', AllTeachersView.as_view(), name='all_teachers'),
    path('all_teachers/search/', AllTeachersSearchView.as_view(), name='all_teachers_search'),
    # path('signup/', SignupView.as_view(), name='signup'),
    # Add other URL patterns here as needed
]
