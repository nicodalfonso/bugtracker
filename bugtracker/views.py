from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from bugtracker.models import BugHunter
from bugtracker.forms import LoginForm

# Create your views here.
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["username"], password=data["password"]
            )
            if user:
                login(request, user)
                return HttpResponseRedirect(
                    request.GET.get("next", reverse("homepage"))
                )

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("homepage"))
    form = LoginForm()
    return render(request, "generic_form.html", {"form": form})


@login_required
def index_view(request):
    return render(request, "index.html")