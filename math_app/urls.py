from django.urls import path, re_path
from django.views.generic import TemplateView

from . import views

app_name = "math_app"

urlpatterns = [
    path("utility/", views.utility_dashboard, name="utility_dashboard"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(
            template_name="sitemap.xml", content_type="application/xml"
        ),
    ),
    # Catch-all routes everything else to the Vue SPA shell
    re_path(r"^.*$", views.index_view, name="index"),
]