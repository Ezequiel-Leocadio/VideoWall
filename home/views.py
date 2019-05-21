from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    home = ''
    return render(request, 'home.html', {'home': home})
