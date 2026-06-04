from django.urls import path
from . import views

app_name = 'math_app'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('utility/', views.utility_dashboard, name='utility_dashboard'),
]