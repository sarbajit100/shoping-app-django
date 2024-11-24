from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login_page"),
    path('loginuser/',views.login_user,name='loginuser'),
    path('register/', views.register_page, name="register_page"),
    path('registeruser/', views.register_user, name="register_user"),
    path('captcha/', include('captcha.urls')),
]