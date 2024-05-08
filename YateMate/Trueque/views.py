from django.shortcuts import render


def list_publication(request):
     return render(request, "list_publication.html")
