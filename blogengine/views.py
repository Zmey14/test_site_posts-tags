from django.http import HttpResponse
from django.shortcuts import redirect


def redirect_website(request):
    return redirect('vacancy_url', permanent=True)
