from django.shortcuts import render
import markdown
from . import util
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import SuspiciousFileOperation
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import random

def index(request):

    if request.method == "POST":

        formm = (request.POST)
        q = request.POST.get('q')
        
        return HttpResponseRedirect(reverse("wiki:callme", args=[q]))
        
        #task = formm.cleaned_data["task"]
            #Name.append(task)
            #request.session["tasks"] += [task]
            #taskname = task.lowe()
            #return cpage(taskname)
   
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def cpages(request,name):
    entry = util.get_entry(name)
    if entry is not None:
        return render(request, "encyclopedia/cpage.html", {
            "data": markdown.markdown(entry),
            "name": name,
        })
    
    # If no exact match, check for partial matches
    entries = util.list_entries()
    partial_matches = [entry for entry in entries if name.lower() in entry.lower()]
    
    if partial_matches:
        return render(request, "encyclopedia/search.html", {
            #"query": name,
            "entries": partial_matches,
        })
    else:
        return render(request, "encyclopedia/cpage.html",{
        "data":None
        })


def newpage(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        try:
            util.save_entry(title, content)
            # Redirect to the newly created page or any other appropriate action
            return HttpResponseRedirect(reverse('wiki:callme', args=[title]))
        except SuspiciousFileOperation as e:
            
            initial_data = {'title': title, 'content': content}  # Preserve entered data
            error_message = str(e)  # Get the error message
            return render(request, "encyclopedia/newpage.html", {
                "error_message": error_message,
                "form": initial_data,  # Pass form data back to the template
            })
        
    return render(request, "encyclopedia/newpage.html")


def edit(request,name):
    if request.method=="POST":
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title != name:
            util.save_entry(title,content)
            util.default_storage.delete(f"entries/{name}.md")
        else:
            filename = f"entries/{title}.md"
            if default_storage.exists(filename):
                default_storage.delete(filename)
            default_storage.save(filename, ContentFile(content))
        return HttpResponseRedirect(reverse("wiki:callme", args=[title]))

    content = util.get_entry(name)
    if content is None:
        return render(request,"encyclopedia/cpage.html",{
            "data": "No Data Found",
            "name": name,
        })
    
    return render(request, "encyclopedia/editpage.html",{
        "form":{
            "name": name,
            "content":content
        }
    })


def random_page(request):
    entries = util.list_entries()
    if not entries:
        return render(request,"encyclopedia/cpage.html",{
            "data":"No Entries Found"
        })
    random_entries = random.choice(entries)
    return HttpResponseRedirect(reverse('wiki:callme', args = [random_entries] ))
    
    