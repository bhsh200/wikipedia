from django.shortcuts import render
from . import util
from django.http import HttpResponse
import markdown2
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random

class NewEntryForm(forms.Form):
    entry=forms.CharField(label="New Title")
    content=forms.CharField(widget=forms.Textarea)

class EditForm(forms.Form):
    content=forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request,name):
    entry=util.get_entry(name) 
    if entry is None:
        return HttpResponse("Page Not Found")
    else:
        markdowner=Markdown()
        return render(request,"encyclopedia/title.html",{
        "data":markdowner.convert(entry), 
        "edit_name":name
        }

    )

def newPage(request):
    entries=util.list_entries()
    if request.method=="POST":
        form=NewEntryForm(request.POST)
        if form.is_valid():
            entru=form.cleaned_data["entry"]
            content=form.cleaned_data["content"]
            if entru not in util.list_entries():
                util.save_entry(entru,content)
                return HttpResponseRedirect(reverse("index"))
            else: return HttpResponse("This entry already exists")
        else:
            return render(request,"encyclopedia/newpage.html",{
                "form":form
            })

    return render(request, "encyclopedia/newpage.html",{
        "form":NewEntryForm()
    })

def editPage(request,edit_name):
    page=util.read_page(edit_name)
    if request.method=="POST":
        form=EditForm(request.POST)
        if form.is_valid():
            content=form.cleaned_data["content"]
            util.write_page(edit_name,content)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"encyclopedia/editpage.html",{
                "form":form,
                "edit_name":edit_name
            })
    return render(request, "encyclopedia/editpage.html",{
        "form":EditForm(initial={'content': page}),
        "edit_name":edit_name
    })
def randomPage(request):
    entries=util.list_entries()
    page=random.choice(entries)
    return HttpResponseRedirect(reverse('title',args=(page,)))

def searchPage(request):
    search=request.GET.get('q','')
    page=util.get_entry(search)
    if page is not None:
        return HttpResponseRedirect(reverse('title', args=(search,)))
    else:
        substrings=[]
        for x in util.list_entries():
            if search.lower() in x.lower():
                substrings.append(x)
        return render(request, "encyclopedia/index.html",{
            "entries": substrings
        })
