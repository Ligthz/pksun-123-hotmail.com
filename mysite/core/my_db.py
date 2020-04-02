from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import BookForm
from .models import Book, Item

def create_item(txt,compl):
    list1 = Item(text=txt, complete=compl)  # create a ToDoList 
    list1.save()  # saves the ToDoList in the database
    return list1

def all_item():
    return Item.objects.all()  # gets the ToDoList object(s) with name "Tim's List"

def delete_all_item():
    all_list  = all_item()  # gets the ToDoList object(s) with name "Tim's List"
    for i_list in all_list:
        i_list.delete()

def delete_item(t_item):
    t_item.delete()

def find_item(txt,compl):
    if txt == "all":
        return Item.objects.filter(complete=compl)  # gets the ToDoList object(s) with name "Tim's List"
    elif compl == "all":
        return Item.objects.filter(text=txt)  # gets the ToDoList object(s) with name "Tim's List"
    else:
        return Item.objects.filter(text=txt, complete=compl)  # gets the ToDoList object(s) with name "Tim's List"

