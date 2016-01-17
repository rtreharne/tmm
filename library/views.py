from django.shortcuts import render
from library.db import L


def shelves(request):
    text = 'dummy'
    
    # create library object
    library = L()
    #shelves = library.shelves()

    return render(request, "shelves.html", {'shelves': L.shelves})
