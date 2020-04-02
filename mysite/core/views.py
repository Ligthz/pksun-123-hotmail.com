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
from .my_db import *
from mysite.settings import MEDIA_ROOT

import datetime


o_items = ['Item','RCP','RSP','Bal','Order','D.Qty','D.FP','Unit.AD','Remark' ]
r_items = ['Item','RCP','Qty','D.B.Qty','D.A.Qty','Remark' ]
c_items = ['Invoice','CN','DN','Amount']
all_items = [o_items,r_items,c_items]

class Login(TemplateView):
    template_name = './registration/login.html'

def get_date():
    tdy_date = datetime.datetime.now()
    tdy_date = str(tdy_date).split(" ")[0]
    return tdy_date


def Home(request):
    datas = []

        
    return render(request, 'home.html',{"datas":datas})

def login(request):
    u_id = request.POST.get('id')
    u_pass = request.POST.get('passw')
    print(u_id)
    print(u_pass)
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


def order_form_process(requests):
    inp = [{},{},{}]
    for key, value in requests.POST.items():
        if key == "csrfmiddlewaretoken" or key == "outlet":
            pass
        else:
            split_key = key.split("_")
            actual_key = all_items[int(split_key[0])][int(split_key[1])]
            if actual_key in inp[int(split_key[0])]:
                inp[int(split_key[0])][actual_key].append(value)
            else:
                inp[int(split_key[0])][actual_key] = [value]

    rw = []
    for k, inpt in enumerate(inp):
        for keys in inpt:
            pass
        rw.append(len(inp[k][keys])) #find the rw of respectivei input

    outp = [[],[],[]]
    for k, out in enumerate(outp):
        for i in range(rw[k]):
            outp[k].append([])
            for item in all_items[k]:
                buff = inp[k][item][i]
                outp[k][-1].append(buff)
    return outp


@login_required
def order(request):
    if request.method == 'POST':
        outlet = request.POST.get("outlet")
        tdy_date = get_date()
        return render(request, 'order.html',{"outlet":outlet,"date":tdy_date,"o_items":o_items,"r_items":r_items,"c_items":c_items})

    else:
        return render(request, 'order_land.html')

        

@login_required
def order_post(request):
    outlet = request.POST.get("outlet")
    tdy_date = get_date()
    
    outp = order_form_process(request)

    return render(request, 'order_post.html',{"outlet":outlet,"date":tdy_date,"o_items":o_items,"r_items":r_items,"c_items":c_items, "outp":outp})


@login_required
def order_confirm(request):
    outlet = request.POST.get("outlet")
    tdy_date = get_date()
    outp = order_form_process(request)

    return render(request, 'order_confirm.html',{"outlet":outlet,"date":tdy_date,"o_items":o_items,"r_items":r_items,"c_items":c_items, "outp":outp})



@login_required
def secret_page(request):
    list1 = create_item("Tim's List", False)  # create a ToDoList 
    list1.save()  # saves the ToDoList in the database

    all_list  = all_item()  # gets the ToDoList object(s) with name "Tim's List"
    find_list  = find_item("all",False)  # gets the ToDoList object(s) with name "Tim's List"
    #for i_list in find_list:
    #    i_list.delete()
    print(find_list)
    print(all_list)
    #delete_all_item()
    print(all_list[0])
    delete_item(all_list[0])
    all_list  = all_item()  # gets the ToDoList object(s) with name "Tim's List"
    print(all_list)
    # Since we defined a relationship between Item and ToDoList each ToDoList has an "item_set"
    #list1.complete = True  # change the name of the list
    #list1.save()  # save changes
    #list1.delete()  # delete the list
    return render(request, 'secret_page.html')


class SecretPage(LoginRequiredMixin, TemplateView):
    template_name = 'secret_page.html'


@login_required
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'


def MQTT(request):
    return render(request, 'thread.html')

def up_graph(request):
    return render(request, 'up_graph.html')