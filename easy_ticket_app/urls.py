
from django.urls import path

from . import views
from tickets import views as ticket_views

urlpatterns = [
    path('', views.login_signup_page, name='root'),
    path('login/', views.login_signup_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('tickets-page/', ticket_views.ticket_list, name='tickets_page'),
    path('tickets/', ticket_views.ticket_list, name='ticket_list'),
    path('tickets/<int:ticket_id>/', ticket_views.ticket_detail, name='ticket_detail'),
    path('tickets/<int:ticket_id>/edit/', ticket_views.ticket_edit, name='ticket_edit'),
    path('tickets/<int:ticket_id>/delete/', ticket_views.ticket_delete, name='ticket_delete'),
    path('account/', ticket_views.account_page, name='account'),
]
