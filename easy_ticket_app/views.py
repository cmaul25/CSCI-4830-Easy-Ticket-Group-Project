from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Comment, Category, Priority, Status


# View all tickets
@login_required
def ticket_list(request):
    tickets = Ticket.objects.all().order_by('-created_at')

    return render(request, "tickets/ticket_list.html", {
        "tickets": tickets
    })


# View tickets assigned to the logged-in user
@login_required
def my_tickets(request):
    tickets = Ticket.objects.filter(
        assigned_to=request.user
    ).order_by('-created_at')

    return render(request, "tickets/my_tickets.html", {
        "tickets": tickets
    })


# View tickets by status (example: Open, Closed)
@login_required
def tickets_by_status(request, status_name):
    tickets = Ticket.objects.filter(
        status__name=status_name
    ).order_by('-created_at')

    return render(request, "tickets/tickets_by_status.html", {
        "tickets": tickets,
        "status": status_name
    })


# View a single ticket with comments
@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    comments = ticket.comments.all().order_by('created_at')

    return render(request, "tickets/ticket_detail.html", {
        "ticket": ticket,
        "comments": comments
    })


# Create a new ticket
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


# Add a comment to a ticket
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
