from django.test import TestCase
from django.urls import reverse

from .models import Chore, Member


class ModelTests(TestCase):
    def test_create_member_and_chore_with_assignee(self):
        member = Member.objects.create(name="Alex")
        chore = Chore.objects.create(
            title="Wash dishes",
            notes="After dinner",
            assignee=member,
        )
        self.assertEqual(str(member), "Alex")
        self.assertEqual(str(chore), "Wash dishes")
        self.assertFalse(chore.is_done)
        self.assertEqual(chore.assignee.name, "Alex")


class ViewTests(TestCase):
    def setUp(self):
        self.member = Member.objects.create(name="Sam")
        self.chore = Chore.objects.create(title="Vacuum", assignee=self.member)

    def test_chore_list_shows_title_and_assignee(self):
        response = self.client.get(reverse("chore_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Vacuum")
        self.assertContains(response, "Sam")

    def test_create_chore(self):
        response = self.client.post(
            reverse("chore_create"),
            {
                "title": "Take out trash",
                "notes": "",
                "due_date": "",
                "assignee": self.member.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Chore.objects.filter(title="Take out trash").exists())

    def test_toggle_completion(self):
        self.assertFalse(self.chore.is_done)
        response = self.client.post(reverse("chore_toggle", args=[self.chore.pk]))
        self.assertEqual(response.status_code, 302)
        self.chore.refresh_from_db()
        self.assertTrue(self.chore.is_done)

    def test_edit_and_delete_chore(self):
        response = self.client.post(
            reverse("chore_edit", args=[self.chore.pk]),
            {
                "title": "Vacuum living room",
                "notes": "Weekly",
                "due_date": "",
                "assignee": self.member.pk,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.title, "Vacuum living room")

        response = self.client.post(reverse("chore_delete", args=[self.chore.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Chore.objects.filter(pk=self.chore.pk).exists())

    def test_create_member(self):
        response = self.client.post(reverse("member_create"), {"name": "Jordan"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Member.objects.filter(name="Jordan").exists())
