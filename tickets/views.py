from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import AccountForm, CreateAccountForm, TicketCreateForm, TicketEditForm, TicketUpdateForm
from .models import Ticket
from .services import add_ticket_update, create_ticket, create_user_account, delete_ticket, list_tickets, update_ticket


def _is_admin(user):
    return hasattr(user, 'profile') and user.profile.is_admin


def home(request):
    if request.user.is_authenticated:
        return redirect('ticket_list')
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('ticket_list')

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('ticket_list')

    return render(request, 'tickets/login.html', {'form': form})


@login_required
def create_account_view(request):
    if not _is_admin(request.user):
        messages.error(request, 'You do not have permission to create accounts.')
        return redirect('ticket_list')

    if request.method == 'POST':
        form = CreateAccountForm(request.POST)
        if form.is_valid():
            try:
                create_user_account(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    role=form.cleaned_data['role'],
                )
                messages.success(request, f"Account '{form.cleaned_data['username']}' created successfully.")
                return redirect('create_account')
            except Exception as e:
                messages.error(request, str(e))
    else:
        form = CreateAccountForm()

    return render(request, 'tickets/create_account.html', {'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def ticket_list(request):
    if request.method == 'POST':
        form = TicketCreateForm(request.POST)
        if form.is_valid():
            create_ticket(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                created_by=request.user,
                assigned_to=form.cleaned_data['assigned_to'],
            )
            messages.success(request, 'Ticket created successfully.')
            return redirect('ticket_list')
    else:
        form = TicketCreateForm()

    status_filter = request.GET.get('status') or None
    if _is_admin(request.user):
        tickets = list_tickets(status=status_filter)
    else:
        tickets = Ticket.objects.filter(
            Q(created_by=request.user) | Q(assigned_to=request.user)
        ).order_by('-created_at')
        if status_filter:
            tickets = tickets.filter(status=status_filter)

    return render(
        request,
        'tickets/ticket_list.html',
        {
            'form': form,
            'tickets': tickets,
            'status_filter': status_filter or '',
            'status_choices': Ticket.STATUS_CHOICES,
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        update_form = TicketUpdateForm(request.POST)
        if update_form.is_valid():
            add_ticket_update(
                ticket=ticket,
                update_text=update_form.cleaned_data['update_text'],
                updated_by=request.user,
            )
            messages.success(request, 'Ticket update added.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        update_form = TicketUpdateForm()

    return render(
        request,
        'tickets/ticket_detail.html',
        {
            'ticket': ticket,
            'update_form': update_form,
            'updates': ticket.updates.select_related('updated_by').all().order_by('-timestamp'),
        },
    )


@login_required
@require_http_methods(["GET", "POST"])
def ticket_edit(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == 'POST':
        form = TicketEditForm(request.POST, instance=ticket)
        if form.is_valid():
            update_ticket(
                ticket.id,
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                status=form.cleaned_data['status'],
                assigned_to=form.cleaned_data['assigned_to'],
            )
            messages.success(request, 'Ticket updated successfully.')
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketEditForm(instance=ticket)

    return render(request, 'tickets/ticket_edit.html', {'ticket': ticket, 'form': form})


@login_required
@require_http_methods(["POST"])
def ticket_delete(request, ticket_id):
    delete_ticket(ticket_id)
    messages.success(request, 'Ticket deleted.')
    return redirect('ticket_list')


@login_required
@require_http_methods(["GET", "POST"])
def account_page(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account updated successfully.')
            return HttpResponseRedirect(reverse('account'))
    else:
        form = AccountForm(instance=request.user)

    assigned_count = Ticket.objects.filter(assigned_to=request.user).count()
    created_count = Ticket.objects.filter(created_by=request.user).count()

    return render(
        request,
        'tickets/account.html',
        {
            'form': form,
            'assigned_count': assigned_count,
            'created_count': created_count,
        },
    )