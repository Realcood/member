from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.member_reg, name='member_reg'),  # URL에 슬래시 유지
    path('login/', views.member_login, name='member_login'),
    path('logout/', views.member_logout, name='member_logout'),
    
    # 낙상방지 시스템 페이지 URL 추가
    path('fall_prevention/', views.fall_prevention, name='fall_prevention'),
]