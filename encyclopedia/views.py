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
        return render(request, "encyclopedia/error.html", {"title": title, "message": 'page does not exist'})
    else:
        return render(request, "encyclopedia/wiki.html", 
            {"title": title, "content": markdown(content)})
    
def search(request):
    if request.method == 'POST':
        query = request.POST.get('q', None) 
        if query:
            content = util.get_entry(query)
            if content:
                return redirect(reverse('wiki', kwargs={'title': query})
                )
            else:
                suggestions = [entry for entry in entries if query.lower() in entry.lower()]
                if suggestions:
                    return render(request, "encyclopedia/search.html", {"title": query, "suggestions": suggestions})
                else:
                    return render(request, "encyclopedia/error.html", {'title': query, "message": 'page does not exist'})


def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST['title']
        content = request.POST['content']
        titleExist = util.get_entry(title)
        if titleExist is not None:
            return render(request, "encyclopedia/error.html", {
                'title': title, "message": "Entry page already exists"
            })
        else:
            util.save_entry(title, content)
            return render(request, "encyclopedia/wiki.html", {
                "title": title,
                "content": markdown(content)
            })


def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']
        content = util.get_entry(title)
        
        return render(request, "encyclopedia/edit.html",{
            "title": title,
            "content": content
        })
    
def save_edit(request):
    if request.method =="POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": markdown(content)
        })


def randomize(request):
    entry = random.choice(entries)
    content = util.get_entry(entry)
    try:
        return render(request, "encyclopedia/wiki.html", 
                  {"title": entry, "content": markdown(content)})
    except FileNotFoundError:
        return None


