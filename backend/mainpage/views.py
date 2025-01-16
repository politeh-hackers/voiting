from django.shortcuts import render


def MainPageClientView(request):
    return render(request, "MainPage.html")
