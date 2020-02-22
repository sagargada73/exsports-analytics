from django.shortcuts import render, HttpResponse

def index(request):
    context_data = {}
    return render(request, 'dashboard.html', context_data)


def setCategory(request):
    category = request.POST.category;
    print(category)
    context_data = {}
    return render(request, 'dashboard.html', context_data)