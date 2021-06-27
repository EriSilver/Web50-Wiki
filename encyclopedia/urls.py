from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("edit", views.edit, name="edit"),
    path("random", views.rand, name="random"),
    path("<str:title>", views.title, name="titlepage")
]
