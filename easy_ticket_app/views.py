
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from tickets.models import Ticket


def login_signup_page(request):
    if request.user.is_authenticated:
        return redirect('tickets_page')

    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        action = request.POST.get('action')

        if not username or not password:
            error_message = 'Username and password are required.'
        elif action == 'login':
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('tickets_page')
            error_message = 'Incorrect username or password'
        elif action == 'signup':
            if User.objects.filter(username=username).exists():
                error_message = 'Username already exists'
            else:
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('tickets_page')

    return render(request, 'login+signup.html', {'error': error_message})


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    recent_tickets = Ticket.objects.select_related('created_by', 'assigned_to').order_by('-created_at')[:5]
    return render(request, 'home.html', {'tickets': recent_tickets})


def search(request):
    if not request.user.is_authenticated:
        return redirect('login')

    query = (request.GET.get('q') or '').strip()
    selected_status = (request.GET.get('status') or '').strip()

    tickets = Ticket.objects.select_related('created_by', 'assigned_to').all().order_by('-created_at')
    if query:
        tickets = tickets.filter(title__icontains=query) | tickets.filter(description__icontains=query)
        tickets = tickets.order_by('-created_at')
    if selected_status and selected_status != 'All':
        tickets = tickets.filter(status=selected_status)

    statuses = [{'name': value, 'label': label} for value, label in Ticket.STATUS_CHOICES]
    return render(request, 'search.html', {
        'tickets': tickets,
        'query': query,
        'selected_status': selected_status,
        'statuses': statuses,
    })


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('login')
