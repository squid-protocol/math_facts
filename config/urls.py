"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

from math_app.api import api


def trigger_error(request):
    return 1 / 0

urlpatterns = [
    path("sentry-debug/", trigger_error),
    path("admin/", admin.site.urls),
    # Mount the Django Ninja API at /api/
    path("api/", api.urls),
    # Forward all other traffic to the math_app
    path("", include("math_app.urls")),
]
