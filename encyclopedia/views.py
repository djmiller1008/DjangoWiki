from django.shortcuts import redirect
from django.shortcuts import render
import markdown2

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
    

def new(request):
    return render(request, "encyclopedia/new.html")
    
        