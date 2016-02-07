from django.shortcuts import render
from library.db import L


def shelves(request):
    text = 'dummy'
    
    library = L()
    shelves = library.shelves()

    return render(request, "shelves.html", {'shelves': shelves})

def shelf(request, shelf=None):
    library = L()
    shelf = library.shelf(shelf)

    return render(request, "shelf.html", {'shelf': shelf})

def book(request, shelf=None, book=None):
   
    library = L()
    book = library.book(book)

    return render(request, "book.html", {'shelf': shelf, 'book': book})

def page(request, shelf=None, book=None, page=None):
    
    library = L()
    page = library.page(page)

    return render(request, "page.html", {'shelf': shelf, 'book': book, 'page': page})
