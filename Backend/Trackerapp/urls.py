from os import name
from django.urls import include, path
from .views import (
     RegisterView, LoginAPIView, PasswordTokenCheckAPI, 
     RequestPasswordResetEmail, SetNewPasswordAPIView, LogoutAPIView)
from rest_framework import views

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


from django.conf.urls import url, include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404


urlpatterns = [
# authentication url paths
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    # path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name='request-reset-email'),
    path('password-reset/<uidb64>/<token>/',PasswordTokenCheckAPI.as_view(), name='password-reset-confirmation' ),
    path('password-reset-success/', SetNewPasswordAPIView.as_view(), name='password-reset-success'),

    ## Cleaner urls

    url(r'^api/users/$', CustomUsersList.as_view(), name='api_customusers'),    # All CustomUsers
    url(r'^api/users/(?P<pk>[0-9]+)/$', CustomUserView.as_view(), name='api_customuser_profile'),    # CustomUserProfile
    url(r'^api/users/(?P<pk>[0-9]+)/update/$', UpdateCustomUserView.as_view(), name='api_update_customuser'),    # Update CustomUser

    url(r'^api/cohorts/$', CohortsList.as_view(), name='api_cohorts'),    # Get all Cohorts + Create
    url(r'api/cohorts/(?P<pk>[0-9]+)/$', CohortProfileView.as_view(), name='api_cohort'),    # Cohort by id + Delete + All Projects in a Cohort
    url(r'api/cohorts/(?P<pk>[0-9]+)/projects/$', CohortProjectsView.as_view(), name='api_cohort_projects'),    # Cohort Projects

    url(r'^api/styles/$', StylesList.as_view(), name='api_styles'),    # Get all Styles + Create
    url(r'api/styles/(?P<pk>[0-9]+)/$', StyleProfileView.as_view(), name='api_style'),    # DevStyle by id + Delete
    url(r'api/styles/(?P<pk>[0-9]+)/projects/$', StyleProjectsView.as_view(), name='api_style_projects'),    # Projects by DevStyle

    url(r'^api/projects/$', ProjectsList.as_view(), name='api_projects'),    # Get all Projects
    url(r'^api/projects/new/$', NewProjectView.as_view(), name='api_projects_new'),    # Create new project
    url(r'api/projects/(?P<pk>[0-9]+)/$', ProjectProfileView.as_view(), name='api_project'),    # Project by id + Delete + ProjectMembers
    url(r'api/projects/(?P<pk>[0-9]+)/update/$', UpdateProjectView.as_view(), name='api_project_update'),    # Update Project
    url(r'api/projects/(?P<pk>[0-9]+)/members/$', ProjectMembersView.as_view(), name='api_project_members'), # Project Members
    url(r'api/projects/(?P<pk>[0-9]+)/members/update/$', UpdateProjectMembersView.as_view(), name='api_project_members_update'),    # Update Project Members

    url(r'^api/students/$', StudentsList.as_view(), name='api_students'),    # Get all Students
    url(r'api/students/(?P<pk>[0-9]+)/$', StudentProfileView.as_view(), name='api_student'),    # Student by id + StudentProjects
    url(r'api/students/(?P<pk>[0-9]+)/projects/$', StudentProjectsView.as_view(), name='api_student_projects'),    # Student Projects
    url(r'api/students/(?P<pk>[0-9]+)/update/$', UpdateStudentView.as_view(), name='api_student_update'),    # Update Student profile

    url(r'api/search/projects/$', ProjectSearch.as_view(), name='api_project_search'),    # Project search
    url(r'api/search/students/$', StudentSearch.as_view(), name='api_student_search'),    # Student search

    url(r'api/user/$', CurrentUserView.as_view(), name='api_user'),    # Current User
    url(r'api/user/profile/$', CurrentUserProfileView.as_view(), name='api_user_profile'),    # Current User Profile
]