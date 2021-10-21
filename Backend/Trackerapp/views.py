from django.db.models.fields import IPAddressField
from django.shortcuts import render
from rest_framework import generics, serializers,status,views, permissions
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect, resolve_url
from django.http import Http404
from rest_framework import generics, serializers, status, filters
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import *
from .serializers import *
from .permissions import *
from .models import CustomUser
from .serializers import (
    RegisterSerializer, SetNewPasswordSerializer,
     LoginSerializer, ResetPasswordEmailRequestSerializer, LogoutSerializer)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, Token
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .renderers import UserRender
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
from django.http import HttpResponsePermanentRedirect
import os
import django_filters
from rest_framework.parsers import JSONParser, MultiPartParser
 



# Create your views here.
# Start of Authentication classes apiviews

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']



class RegisterView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    renderer_classes = (UserRender,)

    def post(self, request):
        permission_classes = (AllowAny,)
        #permission_classes = (IsAdminOrReadOnly,)
        user = request.data
        serializer =self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data =serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token

        # current_site=get_current_site(request).domain
        # relativeLink=reverse('email-verify')
        # absoluteurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body='Welcome to Trackerapp  \n'
        data={'email_body':email_body,'to_email':user.email, 'email_subject':'Welcome'}

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer =  self.serializer_class(data=request.data)

        email = request.data.get('email', '')
        
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64=urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site=get_current_site(request=request).domain
            relativeLink=reverse(
                'password-reset-confirmation', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = request.data.get('redirect_url', '')

            absoluteurl = 'http://'+current_site+relativeLink
            email_body='Hello, \nClick on the link below to reset your password  \n'+ absoluteurl+'?redirect_url='+redirect_url
            data={'email_body':email_body,'to_email':user.email, 'email_subject':'Reset your password'}

            Util.send_email(data)
        return Response({'Successful reset: ' 'A link has been sent to your email for password reset'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer


    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)


            if not PasswordResetTokenGenerator().check_token(user, token):

                if len(redirect_url)>3:
                    return CustomRedirect(redirect_url+'?token_valid=False')

                else:
                     return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            
            if redirect_url and len(redirect_url)>3:
                return CustomRedirect(redirect_url+'?token_valid=True&?message=Valid credentials&?uidb64='+uidb64+'&?token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')



        except DjangoUnicodeDecodeError:
                if not PasswordResetTokenGenerator().check_token(user, token):
                    return CustomRedirect(redirect_url+'?token_valid=False')


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message': 'Password has been set successfully'}, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


# End of authenticaton classes apiviews

class CustomUsersList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ProjectsList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filterset_fields = ['cohort', 'style', 'owner']


class StudentsList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filterset_fields = ['cohort',]


class CohortsList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer

    def post(self, request, format=None):
        serializers = NewCohortSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class StylesList(generics.ListAPIView):
    #permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    queryset = DevStyle.objects.all()
    serializer_class = StyleSerializer

    def post(self, request, format=None):
        serializers = NewStyleSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserView(APIView):
    #permission_classes = (IsAdminOrReadOnly, IsAuthenticated)
    
    def get_custom_user(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)

        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        custom_user = self.get_custom_user(pk)
        serializers = CustomUserSerializer(custom_user)
        return Response(serializers.data)


class StudentProfileView(APIView):
    #permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_student(self, pk):
        try:
            return Student.objects.get(pk=pk)

        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_student(pk)
        serializers = StudentSerializer(student)
        return Response(serializers.data)


class StudentProjectsView(APIView):
    # permission_classes = (IsAuthenticated,)
    def get_student(self, pk):
        try:
            return Student.objects.get(pk=pk)

        except Student.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        student = self.get_student(pk)
        projects = student.projects_owned
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data)


class ProjectProfileView(APIView):
    #permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)

        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        if project and project.owner.user==request.user:
            project.delete()
            return Response({"status":"ok"}, status=status.HTTP_200_OK)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectMembersView(APIView):
    #permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)

        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectMembersSerializer(project)
        return Response(serializers.data)


class CohortProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get_cohort(self, pk):
        try:
            return Cohort.objects.get(pk=pk)

        except Cohort.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cohort = self.get_cohort(pk)
        serializers = CohortSerializer(cohort)
        return Response(serializers.data)

    def delete(self, request, pk, format=None):
        #permission_classes = (IsAdminOrReadOnly,)

        cohort = self.get_cohort(pk)
        if cohort:
            cohort.delete()
            return Response({"status":"ok"}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CohortProjectsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filterset_fields = ['style', 'cohort',]
    # filter_fields = (
    #     'style',
    #     'cohort',
    # )

    def get_cohort(self, pk):
        try:
            return Cohort.objects.get(pk=pk)

        except Cohort.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cohort = self.get_cohort(pk)
        projects = cohort.projects
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data)


class StyleProfileView(APIView):
    #permission_classes = (IsAdminOrReadOnly, IsAuthenticated)

    def get_style(self, pk):
        try:
            return DevStyle.objects.get(pk=pk)

        except DevStyle.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        style = self.get_style(pk)
        serializers = StyleSerializer(style)
        return Response(serializers.data)

    def delete(self, request, pk, format=None):
        style = self.get_style(pk)
        if style:
            style.delete()
            return Response({"status":"ok"}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class StyleProjectsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    filterset_fields = ['cohort',]

    def get_style(self, pk):
        try:
            return DevStyle.objects.get(pk=pk)

        except DevStyle.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        style = self.get_style(pk)
        projects = style.projects
        serializers = ProjectSerializer(projects, many=True)
        return Response(serializers.data)


class NewProjectView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = NewProjectSerializer

    def post(self, request, format=None):
        serializers = NewProjectSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)
            
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentSearch(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'email', 'first_name', 'surname']


class ProjectSearch(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'owner__user__username', 'owner__first_name', 'owner__surname', 'members__user__username']


class UpdateCustomUserView(generics.UpdateAPIView): 
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateCustomUserSerializer


class UpdateStudentView(generics.UpdateAPIView):  
    queryset = Student.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateStudentSerializer


class UpdateProjectView(generics.UpdateAPIView): 
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProjectSerializer


class UpdateProjectMembersView(generics.UpdateAPIView): 
    queryset = Project.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProjectMembersSerializer

    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)

        except Project.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        members = project.members
        serializers = StudentInfoSerializer(members, many=True)
        return Response(serializers.data)


class CurrentUserView(generics.ListAPIView): 
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        current_user = request.user
        serializers = CustomUserSerializer(current_user)
        return Response(serializers.data)


class CurrentUserProfileView(generics.ListAPIView): 
    #permission_classes = (IsAuthenticated,)

    def get(self, request):
        current_user = self.request.user
        profile = current_user.profile
        serializers = StudentSerializer(profile)
        return Response(serializers.data)


# class UploadProjectImageView(APIView):
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (
#         MultiPartParser,
#         JSONParser,
#     )

#     @staticmethod
#     def post(request):
#         file = request.data.get('project_image')

#         upload_data = cloudinary.uploader.upload(file)
#         return Response({
#             'status': 'success',
#             'data': upload_data,
#         }, status=201)


# class UploadProfilePicView(APIView):
#     permission_classes = (IsAuthenticated,)
#     parser_classes = (
#         MultiPartParser,
#         JSONParser,
#     )

#     @staticmethod
#     def post(request):
#         file = request.data.get('profile_pic')

#         upload_data = cloudinary.uploader.upload(file)
#         return Response({
#             'status': 'success',
#             'data': upload_data,
#         }, status=201)