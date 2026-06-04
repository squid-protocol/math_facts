from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "math_app"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("analytics/", views.analytics_view, name="analytics"),
    path("utility/", views.utility_dashboard, name="utility_dashboard"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("faq/", TemplateView.as_view(template_name="faq.html"), name="faq"),
]
