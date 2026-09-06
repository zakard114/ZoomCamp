from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from .forms import ChoreForm, MemberForm
from .models import Chore, Member


def chore_list(request: HttpRequest) -> HttpResponse:
    chores = Chore.objects.select_related("assignee")
    return render(request, "chores/chore_list.html", {"chores": chores})


@require_http_methods(["GET", "POST"])
def chore_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ChoreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("chore_list")
    else:
        form = ChoreForm()
    return render(request, "chores/chore_form.html", {"form": form, "heading": "Add chore"})


@require_http_methods(["GET", "POST"])
def chore_edit(request: HttpRequest, pk: int) -> HttpResponse:
    chore = get_object_or_404(Chore, pk=pk)
    if request.method == "POST":
        form = ChoreForm(request.POST, instance=chore)
        if form.is_valid():
            form.save()
            return redirect("chore_list")
    else:
        form = ChoreForm(instance=chore)
    return render(
        request,
        "chores/chore_form.html",
        {"form": form, "heading": "Edit chore", "chore": chore},
    )


@require_POST
def chore_delete(request: HttpRequest, pk: int) -> HttpResponse:
    chore = get_object_or_404(Chore, pk=pk)
    chore.delete()
    return redirect("chore_list")


@require_POST
def chore_toggle(request: HttpRequest, pk: int) -> HttpResponse:
    chore = get_object_or_404(Chore, pk=pk)
    chore.is_done = not chore.is_done
    chore.save(update_fields=["is_done"])
    return redirect("chore_list")


def member_list(request: HttpRequest) -> HttpResponse:
    members = Member.objects.all()
    return render(request, "chores/member_list.html", {"members": members})


@require_http_methods(["GET", "POST"])
def member_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("member_list")
    else:
        form = MemberForm()
    return render(request, "chores/member_form.html", {"form": form})
