from datetime import date

from django.test import Client, TestCase
from django.urls import reverse

from .models import Todo


class TodoModelTests(TestCase):
    def test_str_returns_title(self):
        todo = Todo.objects.create(title="Buy milk")
        self.assertEqual(str(todo), "Buy milk")

    def test_resolved_defaults_to_false(self):
        todo = Todo.objects.create(title="Clean")
        self.assertFalse(todo.resolved)


class TodoViewTests(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="localhost")

    def test_home_lists_todos(self):
        Todo.objects.create(title="Visible task")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Visible task")

    def test_create_todo_with_due_date(self):
        response = self.client.post(
            reverse("create_todo"),
            {"title": "Ship homework", "due_date": "2026-08-15", "resolved": False},
        )
        self.assertRedirects(response, reverse("home"))
        todo = Todo.objects.get(title="Ship homework")
        self.assertEqual(todo.due_date, date(2026, 8, 15))
        self.assertFalse(todo.resolved)

    def test_edit_todo(self):
        todo = Todo.objects.create(title="Old title")
        response = self.client.post(
            reverse("edit_todo", args=[todo.pk]),
            {"title": "New title", "due_date": "", "resolved": False},
        )
        self.assertRedirects(response, reverse("home"))
        todo.refresh_from_db()
        self.assertEqual(todo.title, "New title")

    def test_delete_todo(self):
        todo = Todo.objects.create(title="Remove me")
        response = self.client.post(reverse("delete_todo", args=[todo.pk]))
        self.assertRedirects(response, reverse("home"))
        self.assertFalse(Todo.objects.filter(pk=todo.pk).exists())

    def test_toggle_resolved(self):
        todo = Todo.objects.create(title="Toggle me", resolved=False)
        response = self.client.post(reverse("toggle_resolved", args=[todo.pk]))
        self.assertRedirects(response, reverse("home"))
        todo.refresh_from_db()
        self.assertTrue(todo.resolved)
