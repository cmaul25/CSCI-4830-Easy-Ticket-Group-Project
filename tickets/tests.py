from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import Ticket
from .services import add_ticket_update, create_ticket, delete_ticket, update_ticket


class TicketServiceTests(TestCase):
    def setUp(self):
        self.creator = User.objects.create_user(username='isaac', password='pass12345')
        self.assignee = User.objects.create_user(username='mason', password='pass12345')

    def test_create_ticket(self):
        ticket = create_ticket(
            title='Laptop not turning on',
            description='The laptop will not boot after an update.',
            created_by=self.creator,
            assigned_to=self.assignee,
        )
        self.assertEqual(ticket.title, 'Laptop not turning on')
        self.assertEqual(ticket.created_by, self.creator)
        self.assertEqual(ticket.assigned_to, self.assignee)

    def test_update_ticket_status(self):
        ticket = create_ticket(
            title='Printer issue',
            description='Printer shows offline.',
            created_by=self.creator,
        )
        updated = update_ticket(ticket.id, status='in_progress', assigned_to=self.assignee)
        self.assertEqual(updated.status, 'in_progress')
        self.assertEqual(updated.assigned_to, self.assignee)

    def test_add_ticket_update(self):
        ticket = create_ticket(
            title='Wi-Fi issue',
            description='Cannot connect to campus Wi-Fi.',
            created_by=self.creator,
        )
        update = add_ticket_update(ticket=ticket, update_text='Checked adapter settings.', updated_by=self.creator)
        self.assertEqual(update.ticket, ticket)
        self.assertEqual(ticket.updates.count(), 1)

    def test_invalid_create_ticket_raises_validation_error(self):
        with self.assertRaises(ValidationError):
            create_ticket(title='', description='', created_by=self.creator)

    def test_delete_ticket_is_idempotent(self):
        ticket = create_ticket(title='Mouse issue', description='Mouse disconnects randomly.', created_by=self.creator)
        delete_ticket(ticket.id)
        delete_ticket(ticket.id)
        self.assertFalse(Ticket.objects.filter(id=ticket.id).exists())


class TicketViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='isaac', password='pass12345')
        self.client.login(username='isaac', password='pass12345')

    def test_ticket_list_page_loads(self):
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ticket Dashboard')

    def test_create_ticket_from_view(self):
        response = self.client.post(
            reverse('ticket-list'),
            {
                'title': 'Monitor issue',
                'description': 'Second monitor is flickering.',
                'assigned_to': '',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Ticket.objects.filter(title='Monitor issue').exists())

    def test_account_page_updates_profile(self):
        response = self.client.post(
            reverse('account'),
            {
                'username': 'isaac',
                'first_name': 'Isaac',
                'last_name': 'Hart',
                'email': 'isaac@example.com',
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Isaac')

    def test_ticket_detail_adds_update(self):
        ticket = create_ticket(title='VPN issue', description='VPN disconnects often.', created_by=self.user)
        response = self.client.post(
            reverse('ticket-detail', args=[ticket.id]),
            {'update_text': 'Restarted the VPN client and tested again.'},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ticket.updates.count(), 1)
