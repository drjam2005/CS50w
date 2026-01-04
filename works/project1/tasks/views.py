from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django import forms


class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")


def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []

    if request.method == "POST":
        task = request.POST.get("del")
        tasks = request.session["tasks"]
        if task in tasks:
            tasks.remove(task)
        request.session["tasks"] = tasks

    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["task"]
            request.session["tasks"] += [data]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })

    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
