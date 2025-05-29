from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts.views import SignupView, UserListViewSet, StudentList, TeacherList

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserListViewSet, basename='user')
router.register(r'students', StudentList, basename='student')
router.register(r'teachers', TeacherList, basename='teacher')
urlpatterns = [
    #account url 수정
    path('', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]+ router.urls