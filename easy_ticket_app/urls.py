from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="login"),
    path("login", views.login_signup, name="login"),
    path("home/", views.home, name="home")
    path("search/", views.search, name="search"),
    path("tickets-page/", views.view_tickets_page, name="tickets_page"),
  
    path("tickets/", views.ticket_list, name="ticket_list"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("tickets/status/<str:status_name>/", views.tickets_by_status, name="tickets_by_status"),
    path("tickets/<int:ticket_id>/", views.ticket_detail, name="ticket_detail"),
    path("tickets/create/", views.create_ticket, name="create_ticket"),
    path("tickets/<int:ticket_id>/comment/", views.add_comment, name="add_comment"),
]
