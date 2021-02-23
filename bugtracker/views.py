from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
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
            filer = BugHunter.objects.get(username=request.user.username)
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
    if request.method == "POST":
        current_ticket = Ticket.objects.get(id=id)
        print(request.POST.keys())
        if "assign" in request.POST.keys():
            print("assign")
            current_ticket.assigned_to = request.user
            current_ticket.status = "IN_PROGRESS"
        elif "complete" in request.POST.keys():
            print("complete")
            current_ticket.assigned_to = None
            current_ticket.completed_by = request.user
            current_ticket.status = "DONE"
        elif "invalid" in request.POST.keys():
            print("invalid")
            current_ticket.assigned_to = None
            current_ticket.completed_by = None
            current_ticket.status = "INVALID"
        current_ticket.save()

    current_ticket = Ticket.objects.get(id=id)
    can_complete = current_ticket.assigned_to == request.user
    return render(
        request, "ticket.html", {"ticket": current_ticket, "can_complete": can_complete}
    )


@login_required
def edit_view(request, id):
    editable = Ticket.objects.get(id=id)
    values = model_to_dict(editable)

    if request.method == "POST":
        form = FileTicketForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            editable.title = data["title"]
            editable.description = data["description"]
            editable.save()
            return HttpResponseRedirect(reverse("ticket_view", args={id}))

    return render(
        request,
        "generic_form.html",
        {"form": FileTicketForm(initial=values)},
    )


@login_required
def hunter_view(request, id):
    hunter = BugHunter.objects.get(id=id)
    filed = Ticket.objects.filter(filed_by=hunter)
    assigned = Ticket.objects.filter(assigned_to=hunter)
    completed = Ticket.objects.filter(completed_by=hunter)
    return render(
        request,
        "hunter.html",
        {
            "hunter": hunter,
            "all": {*filed, *assigned, *completed},
            "filed": filed,
            "assigned": assigned,
            "completed": completed,
        },
    )
