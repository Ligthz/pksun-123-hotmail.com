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
from .models import *
from .my_db import *
from mysite.settings import MEDIA_ROOT
import pickle
import os
import datetime
import mysite.core.models
import csv
import mysite.core.models as models


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

def add_data_once(request):
    csv_path = os.path.join(MEDIA_ROOT,"null.csv")
    datas = []
    with open(csv_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in spamreader:
            datas.append(row)

    parameter = datas[0][:]
    datas = datas[1:]

    print(parameter)
    print(datas)

    for data in datas:
        list1 = Product(
            Brand = data[2],
            Barcodes = data[1],
            Name = data[3],
            PackSize = data[4],
            CtnQty = data[5],
            RCP = data[6],
            RSP = data[7],
            RetailerMargin = data[8],
            FastPay = data[9],
            UlkPurchase = data[0]
        )
        #list1.save()

    return render(request, 'tester.html', {"data": datas})
    

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
        counter = request.POST.get("counter")
        counter = int(counter)
        counter += 1
        if counter == 1:
            area = request.POST.get("area")
            codes = []
            objs = models.outlet.objects.filter(Area=area)
            for obj in objs:
                codes.append(str(obj.Code)+" : "+str(obj.CompanyName))
            return render(request, 'order_land.html',{"area":area,"codes":codes,"counter":counter})
        else:
            outlets = request.POST.get("outlet")
            outlets = outlets.split(" : ")
            outlet = outlets[1]
            code = outlets[0]
            tdy_date = get_date()
            objs = Product.objects.all()
            products = []
            for obj in objs:
                products.append([obj.Name,obj.RCP,obj.RSP])
            return render(request, 'order.html',{"outlet":outlet,"code":code,"date":tdy_date,"products":products,"o_items":o_items,"r_items":r_items,"c_items":c_items})

    else:
        counter = 0
        areas = []
        objs = models.outlet.objects.all()
        for obj in objs:
            if obj.Area not in areas:
                areas.append(obj.Area)
        areas.sort()
        return render(request, 'order_land.html',{"areas":areas,"counter":counter})

        

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

