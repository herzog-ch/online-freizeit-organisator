from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_event, name='new_event'),
    path('user_search', views.user_search, name='user_search'),
    path('overview', views.overview, name='overview'),
    path('', views.new_event, name='new_event_index'),
    path('<int:event_id>/', views.detail, name='detail')
    # ex: /polls/5/results/
    # path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    # path('<int:question_id>/vote/', views.vote, name='vote'),
]
