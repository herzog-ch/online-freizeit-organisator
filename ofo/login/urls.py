from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_view, name='login'),  # http://<domain>/login
    path('logout', views.logout_view, name='logout'),  # http://<domain>/logout
    path('signup', views.signup_view, name='signup')  # http://<domain>/signup
]
