from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from bugtracker.models import BugHunter, Ticket
from bugtracker.forms import FileTicketForm, LoginForm

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
    return render(request, "generic_form.html", {"form": LoginForm(), "title": "Login"})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login_page"))


@login_required
def index_view(request):
    tickets = {
        "NEW": Ticket.objects.filter(status="NEW"),
        "IN_PROGRESS": Ticket.objects.filter(status="IN_PROGRESS"),
        "DONE": Ticket.objects.filter(status="DONE"),
        "INVALID": Ticket.objects.filter(status="INVALID"),
    }
    return render(request, "index.html", {"tickets": tickets})


@login_required
def file_view(request):
    if request.method == "POST":
        form = FileTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            filer = BugHunter.objects.filter(username=request.user.username).first()
            ticket = Ticket.objects.create(
                title=data["title"], description=data["description"], filed_by=filer
            )
            if ticket:
                return HttpResponseRedirect(reverse("homepage"))

    return render(
        request,
        "generic_form.html",
        {"form": FileTicketForm(), "title": "File A Ticket"},
    )


@login_required
def ticket_view(request, id):
    return render(
        request, "ticket.html", {"ticket": Ticket.objects.filter(id=id).first()}
    )


@login_required
def hunter_view(request, id):
    hunter = BugHunter.objects.filter(id=id).first()
    filed = Ticket.objects.filter(filed_by=hunter)
    print(filed)
    assigned = Ticket.objects.filter(assigned_to=hunter)
    completed = Ticket.objects.filter(completed_by=hunter)
    return render(
        request,
        "hunter.html",
        {
            "hunter": hunter,
            "filed": filed,
            "assigned": assigned,
            "completed": completed,
        },
    )
