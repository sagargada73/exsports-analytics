from django.shortcuts import render, HttpResponse

def index(request):
    context_data = {}
    return render(request, 'base.html', context_data)


def setTeam(request):
    if request.method == 'POST':
        team = request.POST.get('team')
        context_data = {
            'team_name': team
        }
        return render(request, 'dashboard.html', context_data)