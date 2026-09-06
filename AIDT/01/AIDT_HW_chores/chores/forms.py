from django import forms

from .models import Chore, Member


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["name"]


class ChoreForm(forms.ModelForm):
    class Meta:
        model = Chore
        fields = ["title", "notes", "due_date", "assignee"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
