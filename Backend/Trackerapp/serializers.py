from django.db.models import fields
from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token
from .models import *
from rest_framework_simplejwt.tokens import Token
from .models import CustomUser, Student, Project, Cohort, DevStyle
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework.parsers import JSONParser, MultiPartParser



class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=68, min_length=6,)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password  = attrs.get('password', '')

        # if not username.isalnum():
        #     raise serializers.ValidationError('The username should only contain alphanumeric characters')

        return attrs
    
    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


# class EmailVerificationSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(max_length=500)

#     class Meta:
#         model = CustomUser
#         fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=3)
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    username=serializers.CharField(max_length=68, min_length=3, read_only=True)
    tokens=serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model= CustomUser
        fields = ['email', 'username', 'password', 'tokens']

    def validate(self, attrs):
        email=attrs.get('email', '')
        password=attrs.get('password', '')
        # filtered_user_by_email = CustomUser.objects.filter(email=email)
        # user=auth.authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider !='email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider
        #     )

        user = auth.authenticate(email=email,password=password)

        if not user:
            raise AuthenticationFailed('Confirm if your credentials are valid, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled for inactivity')



        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens,
        }

        return super().validate(attrs)


    # def validate_email(self, value):
    #     user = self.context['request'].user

    #     if CustomUser.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})

    #     return value

    # def validate_username(self, value):

    #     user = self.context['request'].user
    #     if CustomUser.objects.exclude(pk=user.pk).filter(username=value).exists():
    #         raise serializers.ValidationError({"username": "This username is already in use."})

    #     return value

    # def update(self, instance, validated_data):
    #     instance.email = validated_data['email']
    #     instance.username = validated_data['username']

    #     instance.save()

    #     return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'invalid_token': ('Token is expired or invalid')

    }
    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('invalid_token')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')

    def create(self, validated_data):
        return CustomUser(**validated_data)


class StudentSerializer(serializers.ModelSerializer):
    projects_owned = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    is_dev = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    cohort = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Student
        fields = ('id', 'user', 'first_name', 'surname', 'bio', 'profile_pic', 'email', 'cohort', 'projects_owned', 'is_dev', 'github_profile')

    def create(self, validated_data):
        return Student(**validated_data)


class StudentInfoSerializer(serializers.ModelSerializer):
    
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Student
        fields = ('user',)

    def create(self, validated_data):
        return Student(**validated_data)


class ProjectSerializer(serializers.ModelSerializer):
    owner = StudentInfoSerializer()
    members = StudentInfoSerializer(many=True,)

    cohort = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    style = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Project
        fields = ('id', 'title', 'project_image', 'description', 'owner', 'members', 'cohort', 'style', 'github_link', 'date')

    def create(self, validated_data):
        return Project(**validated_data)


class ProjectMembersSerializer(serializers.ModelSerializer):
    owner = StudentInfoSerializer()
    members = StudentInfoSerializer(many=True,)

    class Meta:
        model = Project
        fields = ('title', 'owner', 'members')

    def create(self, validated_data):
        return Project(**validated_data)


class ProjectMemberGithubSerializer(serializers.ModelSerializer):
    
    members = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='github_profile'
    )

    class Meta:
        model = Project
        fields = ('members',)

    def create(self, validated_data):
        return Project(**validated_data)


class StudentProjectGithubSerializer(serializers.ModelSerializer):
    
    projects_owned = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='github_link'
    )

    is_dev = serializers.SlugRelatedField(
        read_only=True,
        many=True,
        slug_field='github_link'
    )

    class Meta:
        model = Student
        fields = ('projects_owned', 'is_dev')

    def create(self, validated_data):
        return Student(**validated_data)


class CohortMemberGithubSerializer(serializers.ModelSerializer):
    
    students = serializers.SlugRelatedField(
        read_only=True,
        slug_field='github_profile'
    )

    class Meta:
        model = Cohort
        fields = ('students',)

    def create(self, validated_data):
        return Cohort(**validated_data)


class CohortProjectsGithubSerializer(serializers.ModelSerializer):
    
    projects = serializers.SlugRelatedField(
        read_only=True,
        slug_field='github_link'
    )

    class Meta:
        model = Cohort
        fields = ('projects',)

    def create(self, validated_data):
        return Cohort(**validated_data)


class CohortSerializer(serializers.ModelSerializer):
    students = StudentInfoSerializer(many=True,)
    projects = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )
  
    class Meta:
        model = Cohort
        fields = ('id', 'name', 'details', 'projects', 'students')

    def create(self, validated_data):
        return Cohort(**validated_data)


class StyleProjectsGithubSerializer(serializers.ModelSerializer):
    
    projects = serializers.SlugRelatedField(
        read_only=True,
        slug_field='github_link'
    )

    class Meta:
        model = DevStyle
        fields = ('projects',)

    def create(self, validated_data):
        return DevStyle(**validated_data)


class StyleSerializer(serializers.ModelSerializer):
    projects = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = DevStyle
        fields = ('id', 'name', 'description', 'projects')

    def create(self, validated_data):
        return DevStyle(**validated_data)


class NewProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('title', 'description', 'owner', 'style', 'github_link', 'date')

    def create(self, validated_data):
        return Project.objects.create(**validated_data)



class NewCohortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cohort
        fields = ('name', 'details')

    def create(self, validated_data):
        return Cohort.objects.create(**validated_data)


class NewStyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DevStyle
        fields = ('name', 'description')

    def create(self, validated_data):
        return DevStyle.objects.create(**validated_data)


class UpdateCustomUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        extra_kwargs = {
            'username': {'required': True},
        }


class UpdateStudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = Student
        fields = ('first_name', 'surname', 'cohort', 'email', 'bio', 'github_profile')
        extra_kwargs = {
            'first_name': {'required': True},
            'surname': {'required': True},
            'cohort': {'required': True},
            'email': {'required': True},
            'github_profile': {'required': True},
        }

    # def validate_email(self, value):
    #     user = self.context['request'].user

    #     if Student.objects.exclude(pk=user.pk).filter(email=value).exists():
    #         raise serializers.ValidationError({"email": "This email is already in use."})

    #     return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.surname = validated_data['surname']
        #instance.profile_pic = validated_data['profile_pic']
        instance.cohort = validated_data['cohort']
        instance.email = validated_data['email']
        instance.bio = validated_data['bio']
        instance.github_profile = validated_data['github_profile']

        instance.save()

        return instance


class UpdateProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('title', 'description', 'owner', 'cohort', 'style', 'github_link')
        extra_kwargs = {
            'owner': {'required': True},
            'title': {'required': True},
            'style': {'required': True},
        }

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        #instance.project_image = validated_data['project_image']
        instance.description = validated_data['description']
        instance.owner = validated_data['owner']
        instance.cohort = validated_data['cohort']
        instance.style = validated_data['style']
        instance.github_link = validated_data['github_link']

        instance.save()

        return instance


class UpdateProjectMembersSerializer(serializers.ModelSerializer):
    #members = StudentSerializer(many=True,)
    class Meta:
        model = Project
        fields = ('members',)
        #filter_horizontal = ('members',)
        extra_kwargs = {
            'members': {'required': True},
        }

    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.members = validated_data('members', instance.members)
        instance.set()
        return instance


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=3)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']  


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The password reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return user
            
        except Exception as e:
            raise AuthenticationFailed('The password reset link is invalid', 401)

        return super().validate(attrs)


# class UpdateProjectImageSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Project
#         fields = ('project_image',)
#         extra_kwargs = {
#             'project_image': {'required': True},
#         }

#     def update(self, instance, validated_data):
#         instance.project_image = validated_data['project_image']

#         instance.save()

#         return instance


# class UpdateProfilePicSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Student
#         fields = ('profile_pic',)
#         extra_kwargs = {
#             'profile_pic': {'required': True},
#         }

#     def update(self, instance, validated_data):
#         instance.profile_pic = validated_data['profile_pic']

#         instance.save()

#         return instance