from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('tickets/', views.ticket_list, name='ticket-list'),
    path('tickets/<int:ticket_id>/', views.ticket_detail, name='ticket-detail'),
    path('tickets/<int:ticket_id>/edit/', views.ticket_edit, name='ticket-edit'),
    path('tickets/<int:ticket_id>/delete/', views.ticket_delete, name='ticket-delete'),
    path('account/', views.account_page, name='account'),
    path('create-account/', views.create_account_view, name='create_account'),
]