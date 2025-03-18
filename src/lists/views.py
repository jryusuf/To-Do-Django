from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape
from lists.forms import ItemForm, ExistingListItemForm

def home_page(request):
    # if request.method == "POST":
    #     Item.objects.create(text = request.POST["item_text"])
    #     return redirect("/lists/the-only-list-in-the-world/")

    return render(request, "home.html", {"form": ItemForm()})

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=our_list)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=our_list, data= request.POST)
        if form.is_valid():
            form.save()
            return redirect(our_list)
    else:
        form = ExistingListItemForm(for_list=our_list)
    return render(request, "list.html", {"list": our_list, "form": form})

def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})