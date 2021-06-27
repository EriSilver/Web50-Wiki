from django.shortcuts import render
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect
from random import random

entries = util.list_entries()

def title(request, title):

    entry = util.get_entry(title)
    if not entry:
        entry = "The requested page was not found."

    return render(request, "encyclopedia/pages.html", {
        "entry": entry,
        "title": title,
        "entries": entries
    })  

def index(request):
    if request.method == "POST":
        input = request.POST["input"]
        if not input:
            return HttpResponseRedirect("/")
        titles = ""
        print(input)
        print(entries)
        for e in entries:
            if input.lower() in e.lower():
                titles = e
                continue

        print(titles, "///////////////////")    
        if not titles:
            titles = input

        print(titles, "*********************")
        return title(request, titles)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": entries
        })


def create(request):
    form = util.createForm()

    if request.method == "GET":
        return render(request, "encyclopedia/create.html", {
            "entries": entries,
            'form' : form
            })
    else:
        print("\n\n", dict(request.POST),"\n", dict(request.POST)["content"][0], "\n\n")
        form = util.createForm(request.POST)
        print(form)
        if not form.is_valid():
            msg = "Title Required."
            return render(request, "encyclopedia/create.html", {
                "msg" : msg,
                "form" : form, 
                "entries": entries
            })
        
        titles = form.cleaned_data["title"]
        for e in entries:
            if titles.lower() == e.lower():
                msg = "Title Already Exists."
                return render(request, "encyclopedia/create.html", {
                    "form": form,
                    "title": titles,
                    "msg": msg,
                    "entries": entries
                })

        content = request.POST["content"]
        
        with open(f"entries/{titles}.md", "w") as newfile:
            newfile.write(content)
        
        entries.append(titles)
        return title(request, titles)
        

def edit(request):
    post = dict(request.POST)
    print(post)
    if "edit_page" in post:
        title = post["edit_page"][0]

        entry = util.get_entry(title)
        print(entry)
        if not entry:
            entry = "Data Retrieval Error\nPlease, refresh the page and try again."

        return render(request, "encyclopedia/edit.html", {
            "entries": entries,
            "title": title,
            "content": entry
        })

    if "title" in post:
        title = post["title"][0]
        entry = util.get_entry(title)
        print(entry)
        if not entry:
            entry = "Data Retrieval Error\nPlease, refresh the page and try again."
        content = post["content"][0].rstrip()
        if not content or entry == content:
            if not content:
                msg = "Page Content Is Required <br> <h1 style='color:red;'>AND DO NOT FUCKING HACK!!!</h1>"
            elif entry == content:
                msg = "Page content has not changed."

            return render(request, "encyclopedia/edit.html", {
                "entries": entries,
                "title": title,
                "content": entry, 
                "msg": msg
            })
        
        with open(f"entries/{title}.md", "w") as filw:
            filw.write(content)
        
        return render(request, "encyclopedia/pages.html", {
            "entries": entries,
            "title": title,
            "entry": content
        })

    return HttpResponseRedirect("/")
        

def rand(request):
    titles = entries[(int(random() * 100)) % len(entries)]
    return title(request, titles)

    ## markdown