from django.urls import path
from . import views

app_name = 'tournament'

urlpatterns = [
    path('<int:tournament_id>/', views.index, name='tournament'),
]