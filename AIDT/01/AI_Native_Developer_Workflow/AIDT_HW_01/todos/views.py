from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import TodoForm
from .models import Todo


def home(request):
    """List todos and show a form to create a new one."""
    todos = Todo.objects.order_by("resolved", "due_date", "id")
    form = TodoForm()
    return render(request, "home.html", {"todos": todos, "form": form})


@require_POST
def create_todo(request):
    form = TodoForm(request.POST)
    if form.is_valid():
        form.save()
    return redirect("home")


def edit_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = TodoForm(instance=todo)
    return render(request, "home.html", {"todos": Todo.objects.order_by("resolved", "due_date", "id"), "form": form, "editing": todo})


@require_POST
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.delete()
    return redirect("home")


@require_POST
def toggle_resolved(request, pk):
    todo = get_object_or_404(Todo, pk=pk)
    todo.resolved = not todo.resolved
    todo.save(update_fields=["resolved"])
    return redirect("home")
