from django.urls import path
from django.contrib import admin
from user import views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index, name='index'),
    path('register', views.Signup.as_view(), name='register_api'),
    path('login', views.Login.as_view(), name='login_api'),
    path('validate/<str:token>', views.ValidateToken.as_view(), name='validate'),

]