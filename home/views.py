from django.shortcuts import render

def home(request):
    home = ''
    return render(request, 'home.html', {'home': home})
