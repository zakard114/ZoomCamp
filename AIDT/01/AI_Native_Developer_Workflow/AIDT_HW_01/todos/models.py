from django.db import models


class Todo(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    resolved = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
