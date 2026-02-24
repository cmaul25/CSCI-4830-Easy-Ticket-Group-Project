from django.http import HttpResponse

def home(request):
    return HttpResponse("Easy Ticket System is running!")
