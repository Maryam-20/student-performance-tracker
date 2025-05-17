from django.urls import path
from .views import myProfileView


urlpatterns = [
    path('my_profile/<int:userid>/', myProfileView.as_view(), name='my_profile'),
    # path('signup/', SignupView.as_view(), name='signup'),
    # Add other URL patterns here as needed
]
