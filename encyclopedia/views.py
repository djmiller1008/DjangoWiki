from django.shortcuts import redirect
from django.shortcuts import render
from django import forms
import markdown2
import random

from . import util



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry_name):
    entry_content = util.get_entry(entry_name)
 
    if entry_content is None:
        return render(request, "encyclopedia/entry.html", {
            "entry_content": "Page Not Found",
            "entry_title": "Not Found"
        })
    else: 
        return render(request, "encyclopedia/entry.html", {
            "entry_content": markdown2.markdown(entry_content),
            "entry_title": entry_name
        })

def search_results(request):
    query = request.POST['q'] #working now for exact typing. Need to check for capitalized
    possible_entries = []                   
    entries = util.list_entries()
    for entry in entries:
        
        if entry.lower() == query.lower():
            return redirect('wiki:entry', entry_name=entry)
        elif query.lower() in entry.lower():
            possible_entries.append(entry)

    
    
    return render(request, "encyclopedia/search_results.html", {
        "possible_entries": possible_entries
    })
    

class NewEntryForm(forms.Form):
    title = forms.CharField(label = 'Title')
    content = forms.CharField(widget=forms.Textarea())


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if title in util.list_entries():
                error = "An entry with this title already exists!"
                return render(request, "encyclopedia/new.html", {
                    "error": error,
                    "form": NewEntryForm()
                })
            else: 
                util.save_entry(title, content)
                return redirect("wiki:entry", entry_name=title)

    else: 
        return render(request, "encyclopedia/new.html", {
            "form": NewEntryForm()
    })


class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())
    
def edit(request, entry_title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(entry_title, content)
            return redirect('wiki:entry', entry_name=entry_title)
    else:
        content = util.get_entry(entry_title)
        form = EditForm({'content': content})
        return render(request, "encyclopedia/edit.html", {
            "entry_title": entry_title,
            "form": form
        })

def random_page(request):
    entries = util.list_entries()
    entry_name = random.choice(entries)
    return redirect('wiki:entry', entry_name)
