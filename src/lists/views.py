from django.http import HttpResponse
from django.shortcuts import redirect,render
from lists.models import Item, List
from django.core.exceptions import ValidationError
from django.utils.html import escape

def home_page(request):
    # if request.method == "POST":
    #     Item.objects.create(text = request.POST["item_text"])
    #     return redirect("/lists/the-only-list-in-the-world/")

    return render(request, "home.html")

def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    return render(request, "list.html", {"list": our_list})

def new_list(request):
    nulist = List.objects.create()
    item = Item(text = request.POST["item_text"], list = nulist)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        nulist.delete()
        error = escape("You can't have an empty list item")
        return render(request, "home.html", {"error": error})
    return redirect(f"/lists/{nulist.id}/")

def add_item(request, list_id):
    our_list = List.objects.get(id= list_id)
    Item.objects.create(text= request.POST["item_text"], list= our_list)
    return redirect(f"/lists/{our_list.id}/")