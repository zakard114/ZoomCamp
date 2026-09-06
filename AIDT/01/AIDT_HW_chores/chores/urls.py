from django.urls import path

from . import views

urlpatterns = [
    path("", views.chore_list, name="chore_list"),
    path("chores/new/", views.chore_create, name="chore_create"),
    path("chores/<int:pk>/edit/", views.chore_edit, name="chore_edit"),
    path("chores/<int:pk>/delete/", views.chore_delete, name="chore_delete"),
    path("chores/<int:pk>/toggle/", views.chore_toggle, name="chore_toggle"),
    path("members/", views.member_list, name="member_list"),
    path("members/new/", views.member_create, name="member_create"),
]
