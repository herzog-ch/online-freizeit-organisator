from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_event, name='new_event'),
    path('user_search', views.user_search, name='user_search'),
    path('', views.new_event, name='new_event_index')
]
