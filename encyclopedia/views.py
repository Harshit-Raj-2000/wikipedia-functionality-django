import random
from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util

import markdown2

class entry_form(forms.Form):
    title = forms.CharField(label="Title",widget=forms.TextInput(attrs={'placeholder':"Add Title"}))
    content = forms.CharField(label="Content",widget=forms.Textarea(attrs={'placeholder':"Add Content"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def view_page(request,page):
    content = util.get_entry(page)
    if content:
        return render(request, "encyclopedia/page.html", {
            "title" : page,
            "content": markdown2.markdown(content)
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message" : "Page does not exist!!"
        })

def searchpages(request):
    if request.method == "POST":
        page_value = request.POST.get('q')
        all_pages = util.list_entries()
        if page_value in all_pages :
            return HttpResponseRedirect(reverse("viewpage",kwargs={"page":page_value}))
        else:
            similar_pages = []
            for each in all_pages:
                if page_value in each:
                    similar_pages.append(each)
            return render(request, "encyclopedia/similarpages.html", {
                "similar_pages": similar_pages
            })

def new_page(request):
    if request.method == "POST":
        form = entry_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if title in util.list_entries():
                return render(request, "encyclopedia/error.html", {
                    "message" : "This article already exists"
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("viewpage",args=[title]))

    return render(request, "encyclopedia/newpage.html", {
        "form" : entry_form()
    })

def edit_page(request, page_title):
    if request.method == "POST":
        form = entry_form(request.POST)
        if form.is_valid():
            title = page_title
            content = form.cleaned_data['content']
            util.save_entry(title,content)
            return HttpResponseRedirect(reverse("viewpage",args=[title]))
    data = {
        'title': page_title,
        'content': util.get_entry(page_title)
    }
    editable_form = entry_form(data)
    editable_form.fields['title'].widget.attrs['readonly'] = True
    return render(request, "encyclopedia/editpage.html", {
        "form": editable_form,
        "title": page_title
    })

def random_page(request):
    page_list = util.list_entries()
    random_index = random.randint(0,len(page_list)-1)
    return HttpResponseRedirect(reverse("viewpage",args=[page_list[random_index]]))

    




    


