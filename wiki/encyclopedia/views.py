from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.urls import reverse
import secrets

from . import util
import markdown2
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    tit = forms.CharField(label="ENTER TITLE", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-8'}))
    cont = forms.CharField(label="ENTER CONTENT", widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10}))
    edit = forms.BooleanField(label="EDIT", initial=False)

# index page with hyperlink

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Display of entries for existing and non-existing

def entry(request, entry):
    mark_conv = Markdown()
    cont = util.get_entry(entry)
    if cont is None:
        return render(request, "encyclopedia/nonexist.html", {
            "Title":entry
        })
    return render(request, "encyclopedia/entry.html", {
        "details":mark_conv.convert(cont),
        "Title":entry
        
    })

# For entering a New Page

def newadd(request):
    if request.method == 'POST':
        form_data = NewEntryForm(request.POST)
        if form_data.is_valid():
            title = form_data.cleaned_data["tit"]
            content = form_data.cleaned_data["cont"]

            if (util.get_entry(title) is None or form_data.cleaned_data["edit"] is True):
                util.save_entry(title, content)
                return HttpResponse(reverse("entry", kwargs={"entry": title}))
            else:
                return render(request, "encyclopedia/newentry.html", {
                    "form": form_data
                })

        else:
            return render(request, "encyclopedia/newentry.html", {
                "form": form_data,
                "exist": False
            })   
    else:
        return render(request, "encyclopedia/newentry.html", {
            "form": NewEntryForm(),
            "exist": True
        })

# for Rendering Random Page

def random(request):
    lst = util.list_entries()
    entry = secrets.choice(lst)
    if entry is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': entry}))
    else:
        return render(request, "encyclopedia/nonexist.html", {
            'Title': "Sorry!"
        })


# for search

def search_entry(request):
    value = request.GET.get('q','')
    if util.get_entry(value) is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={"entry": value}))

    else:
        sub_entries = []
        for i in util.list_entries():
            if value.upper() in i.upper():
                sub_entries.append(i)
        return render(request, "encyclopedia/index.html", {
            "entries": sub_entries
        })
    return render(request, "encyclopedia/nonexist.html", {
        "Title": value
    })

# for editing page

def edit(request, entry):
    content = util.get_entry(entry)
    if content is None:
        return render(request, "encyclopedia/nonexist.html", {
            "Title": entry
        })
    else:
        form = NewEntryForm()
        form.fields["tit"].initial = entry     
        form.fields["cont"].initial = content
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "Title": form.fields["tit"].initial
        })  




