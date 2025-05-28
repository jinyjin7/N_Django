from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts.views import SignupView

urlpatterns = [
    #account url 수정
    path('', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
]