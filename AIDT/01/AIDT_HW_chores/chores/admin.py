from django.contrib import admin

from .models import Chore, Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Chore)
class ChoreAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "assignee", "due_date", "is_done")
    list_filter = ("is_done",)
    search_fields = ("title", "notes")
