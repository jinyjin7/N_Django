from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model

from accounts.models import BaseUser, Student, Teacher

User = get_user_model()

# 회원가입 API
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("비밀번호가 일치하지 않습니다.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

# 유저 리스트 시리얼라이저
class UserListSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(read_only=True)

    class Meta:
        model = BaseUser
        fields = ('source_id','name','email','user_type','is_active','is_admin')

    def get_user_type(self, obj):
        return obj.user_type

class StudentListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    school = serializers.CharField(source='school.name')

    class Meta:
        model = Student
        fields = ('id','name', 'email', 'school','grade','classroom')

class TeacherListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    school = serializers.CharField(source='school.name')

    class Meta:
        model = Teacher
        fields = ('id','name', 'email', 'school','subject')