from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters
from .models import BaseUser,Student,Teacher
from .serializers import SignupSerializer, UserListSerializer, StudentListSerializer, TeacherListSerializer
from rest_framework.pagination import PageNumberPagination


# 커스텀 페이지네이션
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100


class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "회원가입이 완료되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def index(request):
    return render(request, 'registration/index.html')

# User목록 전체 조회시,커스텀 필터 > baseuser모델 속성값에 없는 student와 teacher를 가져오기 위해
class UserFilter(django_filters.FilterSet):
    user_type = django_filters.CharFilter(method='filter_user_type',label='사용자 유형')
    is_admin = django_filters.BooleanFilter(label='관리자 여부')

    class Meta:
        model = BaseUser
        fields = ['is_admin']

    def filter_user_type(self, queryset, name, value):
        type_filters = {
            '학생': queryset.filter(student__isnull=False),
            '선생님': queryset.filter(teacher__isnull=False),
            '관리자': queryset.filter(is_admin=True),
            '기타': queryset.filter(
                student__isnull=True, teacher__isnull=True, is_admin=False
            )
        }
        return type_filters.get(value, queryset)

# 공통 리스트
class BaseListViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

# 유저 리스트 전체 조회
class UserListViewSet(BaseListViewSet):
    queryset = BaseUser.objects.all().order_by('name')
    serializer_class = UserListSerializer
    filterset_class = UserFilter
    search_fields = ['name', 'email']
    ordering = ['name']
    ordering_fields = ['name', 'date_joined']

# 학생 리스트 조회
class StudentList(BaseListViewSet):
    queryset = Student.objects.all().order_by('grade')
    serializer_class = StudentListSerializer
    search_fields = ['user__name', 'grade', 'classroom', 'school__name']
    ordering = ['grade']
    ordering_fields = ['grade']

# 선생님 리스트 조회
class TeacherList(BaseListViewSet):
    queryset = Teacher.objects.all().order_by('user__name')
    serializer_class = TeacherListSerializer
    search_fields = ['user__name', 'user__email', 'subject','school__name']
    ordering = ['user__name']
    ordering_fields = ['user__name']