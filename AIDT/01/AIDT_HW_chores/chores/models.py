from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Chore(models.Model):
    title = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    assignee = models.ForeignKey(
        Member,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="chores",
    )
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["is_done", "due_date", "title"]

    def __str__(self) -> str:
        return self.title
