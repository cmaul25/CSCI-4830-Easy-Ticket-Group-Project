from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from .models import Ticket, TicketUpdate


# -------- Ticket CRUD --------

def create_ticket(*, title: str, description: str, created_by: User, assigned_to: User | None = None) -> Ticket:
    if not title or not description:
        raise ValidationError("Title and description are required.")
    ticket = Ticket.objects.create(
        title=title.strip(),
        description=description.strip(),
        created_by=created_by,
        assigned_to=assigned_to
    )
    return ticket


def get_ticket(ticket_id: int) -> Ticket:
    return Ticket.objects.get(id=ticket_id)


def list_tickets(*, status: str | None = None, created_by: User | None = None, assigned_to: User | None = None):
    qs = Ticket.objects.all().order_by('-created_at')
    if status:
        qs = qs.filter(status=status)
    if created_by:
        qs = qs.filter(created_by=created_by)
    if assigned_to:
        qs = qs.filter(assigned_to=assigned_to)
    return qs


@transaction.atomic
def update_ticket(ticket_id: int, **fields) -> Ticket:
    """
    Allowed fields: title, description, status, assigned_to
    """
    allowed = {"title", "description", "status", "assigned_to"}
    if not fields:
        raise ValidationError("No fields provided to update.")
    if any(k not in allowed for k in fields.keys()):
        raise ValidationError(f"Only these fields can be updated: {sorted(allowed)}")

    ticket = Ticket.objects.select_for_update().get(id=ticket_id)

    # Validate status choice if provided
    if 'status' in fields:
        valid_statuses = {c[0] for c in Ticket.STATUS_CHOICES}
        if fields['status'] not in valid_statuses:
            raise ValidationError(f"Invalid status '{fields['status']}'. Must be one of {sorted(valid_statuses)}")

    for key, value in fields.items():
        setattr(ticket, key, value)
    ticket.save()
    return ticket


def delete_ticket(ticket_id: int) -> None:
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        # idempotent delete
        return
    ticket.delete()


# -------- TicketUpdate (comments/progress logs) --------

def add_ticket_update(*, ticket: Ticket, update_text: str, updated_by: User) -> TicketUpdate:
    if not update_text or not update_text.strip():
        raise ValidationError("Update text is required.")
    return TicketUpdate.objects.create(
        ticket=ticket,
        update_text=update_text.strip(),
        updated_by=updated_by
    )


def list_ticket_updates(ticket_id: int):
    return TicketUpdate.objects.filter(ticket_id=ticket_id).order_by('timestamp')