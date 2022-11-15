from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.toppage_template, name="toppage_template"),
    path("salary/", include("salary.urls")),
]
