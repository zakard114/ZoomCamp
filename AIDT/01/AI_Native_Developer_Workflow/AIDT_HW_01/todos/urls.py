from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create/", views.create_todo, name="create_todo"),
    path("<int:pk>/edit/", views.edit_todo, name="edit_todo"),
    path("<int:pk>/delete/", views.delete_todo, name="delete_todo"),
    path("<int:pk>/toggle/", views.toggle_resolved, name="toggle_resolved"),
]
