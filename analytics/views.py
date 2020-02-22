from django.shortcuts import render, HttpResponse

def index(request):
    context_data = {}
    return render(request, 'dashboard.html', context_data)


def setCategory(request):
    team = request.POST.team;
    print(team)
    context_data = {}
    return render(request, 'dashboard.html', context_data)