from django.urls import path
from . import views

urlpatterns = [
    path('', views.overview, name='overview'),
    path('new', views.new_event, name='new_event'),
    path('user_search', views.user_search, name='user_search'),
    path('<int:event_id>/', views.detail, name='detail'),
    path('delete', views.delete_event, name='delete_event')
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
