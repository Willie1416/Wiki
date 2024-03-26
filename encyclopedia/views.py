from django.shortcuts import render
from markdown2 import markdown
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

import random
from . import util

# Global list for all funtions to use to see list
entries = util.list_entries()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    content = util.get_entry(title)
    
    if content is None:
        return render(request, "encyclopedia/error.html", {"title": title})
    else:
        return render(request, "encyclopedia/wiki.html", 
            {"title": title, "content": markdown(content)})
    
def search(request):
    if request.method == 'POST':
        query = request.POST.get('q', None) # Gets search query
        if query:
            content = util.get_entry(query)
            if content:
                return redirect(reverse('wiki', kwargs={'title': query})
                )
            else:
                suggestions = [entry for entry in entries if query.lower() in entry.lower()]
                if suggestions:
                    return render(request, "encyclopedia/suggestions.html", {"title": query, "suggestions": suggestions})
                else:
                    return render(request, "encyclopedia/error.html", {"title": query})


def create(request):
    return render(request, "encyclopedia/create.html")

def randomize(request):
    entry = random.choice(entries)
    content = util.get_entry(entry)
    return render(request, "encyclopedia/wiki.html", 
                  {"title": entry, "content": markdown(content)})


