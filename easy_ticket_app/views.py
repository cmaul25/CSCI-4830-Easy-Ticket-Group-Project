from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


# pull information from models.py
from .models import Ticket, Comment, Category, Priority, Status

mock_tickets = [
    {
        "id": 1,
        "title": "Computer not turning on",
        "description": "Power button does nothing",
        "created_at": datetime(2026, 3, 28, 10, 30)
    },
    {
        "id": 2,
        "title": "WiFi not working",
        "description": "Cannot connect to network",
        "created_at": datetime(2026, 3, 29, 9, 15)
    },
    {
        "id": 3,
        "title": "Blue screen error",
        "description": "System crashes randomly",
        "created_at": datetime(2026, 3, 27, 14, 5)
    }
]

# Login and signup page
def login_signup(request):
    error_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        action = request.POST.get("action") # action is login button or signup button

        if action == "login":
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                error_message = "Incorrect username or password"

        elif action == "signup":
            if User.objects.filter(username=username).exists():
                error_message = "Account already exists"
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect("home")
            
    return render(request, "login.html", {"error": error_message})

# Homepage with newest tickets first
def home(request):
    sorted_tickets = sorted(mock_tickets, key=lambda x: x["created_at"], reverse=True)
    return render(request, "home.html", {"tickets": sorted_tickets})


# Placeholder search page
def search(request):
    return render(request, "search.html")


# Placeholder all tickets page (UI only)
def view_tickets_page(request):
    return render(request, "tickets.html")


# Display all tickets, with most recent appearing first
@login_required
def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at')

    return render(request, "tickets/ticket_list.html", {
        "tickets": tickets
    })


# Display tickets assigned to the signed-in user only
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(
        assigned_to=request.user
    ).order_by('-created_at')

    return render(request, "tickets/my_tickets.html", {
        "tickets": tickets
    })


# Display tickets by current status (open, closed, work in progress, etc)
@login_required
def tickets_by_status(request, status_name):
    tickets = Ticket.objects.filter(
        status__name=status_name
    ).order_by('-created_at')

    return render(request, "tickets/tickets_by_status.html", {
        "tickets": tickets,
        "status": status_name
    })


# View a specific ticket, pulling information about attached comments
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comments = ticket.comments.all().order_by('created_at')

    return render(request, "tickets/ticket_detail.html", {
        "ticket": ticket,
        "comments": comments
    })


# Create a new ticket by gathering information such as category, priority, status, etc
@login_required
def create_ticket(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        category_id = request.POST.get("category")
        priority_id = request.POST.get("priority")

        category = Category.objects.get(id=category_id)
        priority = Priority.objects.get(id=priority_id)
        status = Status.objects.get(name="Open")

        Ticket.objects.create(
            title=title,
            description=description,
            created_by=request.user,
            category=category,
            priority=priority,
            status=status
        )

        return redirect("ticket_list")

    categories = Category.objects.all()
    priorities = Priority.objects.all()

    return render(request, "tickets/create_ticket.html", {
        "categories": categories,
        "priorities": priorities
    })


# Creates a comment tied to a specific ticket
@login_required
def add_comment(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        content = request.POST.get("content")

        Comment.objects.create(
            ticket=ticket,
            author=request.user,
            content=content
        )

    return redirect("ticket_detail", ticket_id=ticket.id)
