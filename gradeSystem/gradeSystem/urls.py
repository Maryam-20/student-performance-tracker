"""
URL configuration for gradeSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gradeSystem.authapp.views import SignupView, CustomLogoutView
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

base_url = 'school-portal/v1'

urlpatterns = [
    path(f'{base_url}/admin/', admin.site.urls),
    path(f'{base_url}/auth/', include('gradeSystem.authapp.urls')),
    path(f'{base_url}/grading/', include('gradeSystem.gradingapp.urls')),
    path(f'{base_url}/performance/', include('gradeSystem.performanceTrackingApp.urls')),
    path(f'{base_url}/auth/', include('django.contrib.auth.urls')),
    path(f'{base_url}/auth/register/$',SignupView.as_view(), name='signup'),
    path(f'{base_url}/auth/logout/', CustomLogoutView.as_view(), name='logout'),
    # path(f'{base_url}/auth/login/$', SignupView.as_view(), name='login'),
    path(f'{base_url}/home/', TemplateView.as_view(template_name='index.html'), name='home'),
]
