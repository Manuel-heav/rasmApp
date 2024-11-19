from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from openpyxl import Workbook
from itertools import chain
import csv
import xlwt
from django.http import JsonResponse


from .filters import ERABudgetFilter
from tablib import Dataset
#import StringIO
#import xlsxwriter
from .resources import ERABudgetResource


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import formset_factory, inlineformset_factory, modelformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_pivot.pivot import pivot 
from django_pandas.io import read_frame
import sqlite3
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
from pandas.io.formats.style import Styler
from django.contrib.auth import get_user
from django.contrib import messages
from django.db.models import Q, Count, Sum, QuerySet, FloatField, F, Max, Prefetch
from .models import *
from .forms import *
from collections import defaultdict
#from .decorators import unauthenticated_user, allowed_users


# Create your views here.

def get_username(request):
    user = get_user(request)
    if user.is_authenticated:
        username = user.username
        return HttpResponse(f"Logged-in user: {username}")
    else:
        return HttpResponse("No user is logged in")


def registerPage(request):
    form = CreateUserForm
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form':form}
    return render(request, 'rasmApp/register.html', context)

def loginPage(request):
    user = get_user(request)
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        username = user.username
        if username=="alemgena":
            return redirect('home_alemgena')
            #return redirect('alemgena')
        elif username=="adigrat":
            return redirect('home_adigrat')
            #return redirect('adigratl')
        elif username=="kombolcha":
            return redirect('home_kombolcha')
            #return redirect('kombolchal')
        elif username=="debremarkos":
            return redirect('home_debremarkos')
            #return redirect('debremarkosl')
        elif username=="gondar":
            return redirect('home_gondar')
            #return redirect('gondarl')
        elif username=="shashamane":
            return redirect('home_shashamane')
            #return redirect('shashamanel')
        elif username=="nekemte":
            return redirect('home_nekemte')
            #return redirect('nekemte')
        elif username=="diredawa":
            return redirect('home_diredawa')
            #return redirect('diredawal')
        elif username=="jimma":
            return redirect('home_jimma')
            #return redirect('jimmal')
        elif username=="sodo":
            return redirect('home_sodo')
            #return redirect('sodol')
        elif username=="gode":
            return redirect('home_gode')
            #return redirect('godel')
        elif user is not None:
            login(request, user)
            return redirect('maindashboard')
        else:
            messages.success(request, ("There was an error logging in. Try Again "))
            return redirect('login')
    else:
        context = {}
        return render(request, 'rasmApp/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def Home(request):
    return render(request,'rasmApp/home.html')

def alemgena_home(request):
    return render(request,'rasmApp/home_alemgena.html')

def alemgenahamle(request):
    return render(request,'rasmApp/alemgena_hamle.html')

def alemgenanehase(request):
    return render(request,'rasmApp/alemgena_nehase.html')

def alemgenasep(request):
    return render(request,'rasmApp/alemgena_sep.html')

def alemgenaoct(request):
    return render(request,'rasmApp/alemgena_oct.html')

def alemgenanov(request):
    return render(request,'rasmApp/alemgena_nov.html')

def alemgenadec(request):
    return render(request,'rasmApp/alemgena_dec.html')

def alemgenajan(request):
    return render(request,'rasmApp/alemgena_jan.html')

def alemgenafeb(request):
    return render(request,'rasmApp/alemgena_feb.html')

def alemgenamar(request):
    return render(request,'rasmApp/alemgena_mar.html')

def alemgenaapr(request):
    return render(request,'rasmApp/alemgena_apr.html')

def alemgenamay(request):
    return render(request,'rasmApp/alemgena_may.html')

def alemgenajun(request):
    return render(request,'rasmApp/alemgena_jun.html')

def adigrat_home(request):
    return render(request,'rasmApp/home_adigrat.html')

def kombolcha_home(request):
    return render(request,'rasmApp/home_kombolcha.html')

def debremarkos_home(request):
    return render(request,'rasmApp/home_debremarkos.html')

def gondar_home(request):
    return render(request,'rasmApp/home_gondar.html')

def shashamane_home(request):
    return render(request,'rasmApp/home_shashamane.html')

def nekemte_home(request):
    return render(request,'rasmApp/home_nekemte.html')

def diredawa_home(request):
    return render(request,'rasmApp/home_diredawa.html')

def jimma_home(request):
    return render(request,'rasmApp/home_jimma.html')

def sodo_home(request):
    return render(request,'rasmApp/home_sodo.html')

def gode_home(request):
    return render(request,'rasmApp/home_gode.html')


def userPage(request):
    context = {}
    return render(request, 'rasmApp/user.html', context)

def maindashboard(request):
    return render(request, 'rasmApp/maindashboard.html')

@login_required(login_url='login')
def rams_dashboard(request):
    numbers = range(0, 12)  # Create a range from 0 to 11 (excluding 12)
    actionplans = ActionPlan.objects.all()
    budgetext = BudgetExt.objects.all()
    annual_budget=RMBudget.objects.all()
    budgetyr=ERABudget.objects.all()
    districtl = District.objects.all()
    
    
    total_budgetext = budgetext.count()
    total_actionplans = actionplans.count()
    total_abcount = annual_budget.count()
    total_budgetyr = budgetyr.count()
    budgetbydistrict = RMBudget.objects.annotate(Count('district'))
    districtbudget = ERABudget.objects.annotate(Count('bdistrict'))
    districtn = budgetbydistrict[0].district.districtname
    district0 = districtbudget[0].bdistrict
    
    context={'actionplans':actionplans, 'budgetext':budgetext, 'total_budgetext':total_budgetext, 'total_actionplans':total_actionplans, 'total_abcount':total_abcount, 'districtl':districtl, 'budgetbydistrict': budgetbydistrict, 'districtn':districtn, 'numbers': numbers, 'budgetyr':budgetyr, 'total_budgetyr':total_budgetyr, 'districtbudget':districtbudget, 'district0':district0}
    return render(request, 'rasmApp/dashboard.html', context)

def budgetext(request, pk):
    budgetext = BudgetExt.objects.get(id=pk)
    ap = budgetext.actionplan_set.all()
    ap_count = ap.count()
    
    context={'bext':budgetext, 'ap':ap, 'ap_count':ap_count}
    return render(request, 'rasmApp/budgetext.html', context)


def annual_budget(request, pk):
    anbudget = ERABudget.objects.get(id=pk)
    bap = anbudget.budgetedap_set.all()
    bap_count = bap.count()
    
    context={'anbudget':anbudget, 'bap':bap, 'bap_count':bap_count}
    return render(request, 'rasmApp/apperbudget.html', context) #budget for action plan 


def budget(request):
    return render(request, 'rasmApp/budget.html')

def createActionPlan(request, pk):
    user = get_user(request)
    ActionPlanFormSet = inlineformset_factory(BudgetExt, ActionPlan, fields=('budgetext','forTheMonth','actionPlanInBr','actionPlanInKm'), extra=12)
    budgetext = BudgetExt.objects.get(id=pk)
    formset = ActionPlanFormSet(queryset=ActionPlan.objects.none(), instance=budgetext)
    #form = ActionPlanForm(initial={'budgetext':budgetext})
        
    if request.method == 'POST':
        #form = ActionPlanForm(request.POST)
        formset = ActionPlanFormSet(request.POST, instance=budgetext)
        if formset.is_valid():
            formset.save()
            if user=="01":
                return redirect('alemgena')
            elif user=="02":
                return redirect('nekemte')
            else:
                return redirect('home')
    context = {'formset':formset,'budgetext':budgetext}
    return render(request, 'rasmApp/actionplan_form.html', context)


def createBudgetedAP(request, pk):
    user = get_user(request)
    BudgetedAPFormSet = inlineformset_factory(ERABudget, BudgetedAP, fields=('erabudget','month','bapinBr','bapinKm'), extra=12)
    erabudget = ERABudget.objects.get(id=pk)
    formset = BudgetedAPFormSet(queryset=BudgetedAP.objects.none(), instance=erabudget)
        
    if request.method == 'POST':
        formset = BudgetedAPFormSet(request.POST, instance=erabudget)
        if formset.is_valid():
            formset.save()
            if user=="01":
                return redirect('alemgena')
            elif user=="02":
                return redirect('nekemte')
            else:
                return redirect('home')
    context = {'formset':formset,'erabudget':erabudget}
    return render(request, 'rasmApp/budgetedap_form.html', context)


def aps_edit(request):
    context = {}
    form = APForm()
    aps = APSummary.objects.all()
    context['aps'] = aps
    context['title'] = 'AP Summary'
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form = APForm(request.POST)
            else:
                aps = APSummary.objects.get(id=pk)
                form = DistrictForm(request.POST, instance=aps)
            form.save()
            form = APForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            aps = APSummary.objects.get(id=pk)
            aps.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            aps = APSummary.objects.get(id=pk)
            form = APForm(instance=aps)

    context['form'] = form
    return render(request, 'rasmApp/apsedit.html', context)


def createaps(request):
    context = {} 
    #bap = BudgetedAP.objects.filter(month__icontains="ሐምሌ")    
    
    AccomplishmentFormSet = modelformset_factory(Accomplishment, fields=('erabudget', 'month', 'actionInBr', 'actionInKm', 'bremark1', 'bremark2'), extra=2)  
    formset = AccomplishmentFormSet(queryset=Accomplishment.objects.filter(month__icontains="ሐምሌ"))
    
    if request.method == 'POST':
        form = AccomplishmentFormSet(request.POST)
        instances = form.save(commit=False)
        
        for instance in instances:
            instance.save()
    
    context = { 'formset': formset}
    return render(request, 'rasmApp/apsformset.html', context)


@login_required(login_url='login')
def bactionp(request):
    context = {}
        
    q = request.GET.get('q')
    
    if q:
        bap = BudgetedAP.objects.filter(Q(erabudget__bprojectname__icontains=q)|Q(erabudget__broadsegment__icontains=q))
    else:
        bap = BudgetedAP.objects.all()
    
    p = Paginator(bap, 20)
    page_number = request.GET.get('page')
    

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    context = {'page_obj':page_obj,'bap': bap}
    return render(request, 'rasmApp/bapdetail.html', context)


def bactionpalemgena(request):
    context = {}
    q = request.GET.get('d')
    
    if q == 'አለምገና':
        bapalemgena=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains=q)#(Q(erabudget__bdistrict__districtname__icontains=q)|Q(month__icontains = 'ሐምሌ'))
    elif q == 'አዲግራት':
        bapalemgena=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains=q)
    else:
        bap = BudgetedAP.objects.all()
    
    context = {'bapalemgena':bapalemgena}
    
    return render(request, 'rasmApp/baplalemgena.html', context)

def bactionpadigrat(request):
    bapadigrat=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='አዲግራት')
    return render(request, 'rasmApp/bapladigrat.html', {'bapadigrat':bapadigrat})

def bactionpkombolcha(request):
    bapkombolcha=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ኮምቦልቻ')
    return render(request, 'rasmApp/baplkombolcha.html', {'bapkombolcha':bapkombolcha})

def bactionpdebremarkos(request):
    bapdebremarkos=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ደብረ ማርቆስ')
    return render(request, 'rasmApp/bapldebremarkos.html', {'bapdebremarkos':bapdebremarkos})

def bactionpgondar(request):
    bapgondar=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ጎንደር')
    return render(request, 'rasmApp/baplgondar.html', {'bapgondar':bapgondar})

def bactionpshashamane(request):
    bapshashamane=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ሻሸመኔ')
    return render(request, 'rasmApp/baplshashamane.html', {'bapshashamane':bapshashamane})

def bactionpnekemte(request):
    bapnekemte=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ነቀምት')
    return render(request, 'rasmApp/baplnekemte.html', {'bapnekemte':bapnekemte})

def bactionpdiredawa(request):
    bapdiredawa=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ድሬዳዋ')
    return render(request, 'rasmApp/bapldiredawa.html', {'bapdiredawa':bapdiredawa})

def bactionpjimma(request):
    bapjimma=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ጅማ')
    return render(request, 'rasmApp/bapljimma.html', {'bapjimma':bapjimma})

def bactionpsodo(request):
    bapsodo=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__icontains='ሶዶ')
    return render(request, 'rasmApp/baplsodo.html', {'bapsodo':bapsodo})

def bactionpgode(request):
    bapgode=BudgetedAP.objects.filter(erabudget__bdistrict__districtname__contains='ጎዴ')
    return render(request, 'rasmApp/baplgode.html', {'bapgode':bapgode})


def accomplist(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ሐምሌ' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሐምሌ' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አዲግራት' and m=='ሐምሌ':
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl.html', context)
    
def accomplist_nehase(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ነሃሴ' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ነሃሴ' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_nehase.html', context)
    
def accomplist_sep(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='መስከረም' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መስከረም' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_sep.html', context)
    
def accomplist_oct(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ጥቅምት' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥቅምት' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_oct.html', context)
    
def accomplist_nov(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ህዳር' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ህዳር' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_nov.html', context)
    
def accomplist_dec(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ታህሳስ' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ታህሳስ' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_dec.html', context)
    
def accomplist_jan(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ጥር' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ጥር' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_jan.html', context)
    
def accomplist_feb(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='የካቲት' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='የካቲት' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_feb.html', context)
    
def accomplist_mar(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='መጋቢት' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='መጋቢት' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_mar.html', context)
    
def accomplist_apr(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ሚያዚያ' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሚያዚያ' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_apr.html', context)
    
def accomplist_may(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ግንቦት' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ግንቦት' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_may.html', context)
    
def accomplist_jun(request):
    context = {}
    context['title'] = 'Accomplishment'
    l = ''
    wt = request.GET.get('wt')
    #acompsearch = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype__icontains=wt)
    
    d = request.GET.get('d')
    m = request.GET.get('m')

    if d == 'አለምገና' and m=='ሰኔ' and wt=='መደበኛ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ወቅታዊ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ከባድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና (OPRC)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ኦቨርሌይ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ኦቨርሌይ እና በአፈፃፀም ላይ የተመሰረተ መንገድ ጥገና':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የመሬት መንሸራተት እና ጎርፍ መከላከል ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የከተማ አስፋልት መንገድ ማስፋት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የከተማ የአስፋልት ማልበስ ስራ (PTS)':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ድልድይ መልሶ ግንባታ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ድልድይ/ፉካ ጥገና ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ድንገተኛ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የመንገድ ደህንነት ስራ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የማማከር አገልግሎት':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የሚዛን ጣቢያ ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የሚዛን ጣቢያ የማዘመን ስራዎች':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='የካሳ ክፍያ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    elif d == 'አለምገና' and m=='ሰኔ' and wt=='ኤርጎኖሚክስ':
        l = wt
        acomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=d), Q(bapmonth__icontains=m), Q(erabudget__bworktype__maintenancetype__icontains=wt))
    else:
        acomp = Accomplishment.objects.all()
    
    context = {'acomp':acomp, 'l':l}
    return render(request, 'rasmApp/accomplishl_jun.html', context)
    
def accomplishlist(request):
    context = {}
    name = request.GET.get('name')
    m = request.GET.get('m')

    if m=='ሐምሌ':
        acom = Accomplishment.objects.filter(Q(month__icontains=m), Q(erabudget__bdistrict__icontains=name))
        context = {'acom':acom}
        return render(request, 'rasmApp/accomplishlist.html', context)
    elif m=='ሐምሌ':
        acom = Accomplishment.objects.filter(Q(month__icontains=m), Q(erabudget__bdistrict__icontains=name))
        context = {'acom':acom}
        return render(request, 'rasmApp/accomplishlist.html', context)
    else:
        acom = Accomplishment.objects.all()
        return render(request, 'rasmApp/backtodistrict.html', context)
    

def ap_accomplishlistalemgena(request):
    #apacomp = BudgetedAP.objects.filter(Q(month__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='1'))
    apacomp = BudgetedAP.objects.all()
    context = {}
    context = {'apacomp':apacomp}
    return render(request, 'rasmApp/apaccomplstalemgena.html', context)

def accomplishlistalemgena(request):
    acom = BudgetedAP.objects.filter(Q(month=1), Q(erabudget__bdistrict__districtname__icontains='አለምገና'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishlalemgena.html', context)

def accomplishlistadigrat(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='አዲግራት'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishladigrat.html', context)

def accomplishlistkombolcha(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ኮምቦልቻ'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishlkombolcha.html', context)

def accomplishlistdebremarkos(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ደ/ማርቆስ'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishldebremarkos.html', context)

def accomplishlistgondar(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ጎንደር'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishlgondar.html', context)

def accomplishlistshashamane(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ሻሸመኔ'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishlshashamane.html', context)

def accomplishlistnekemte(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ነቀምት'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishlnekemte.html', context)

def accomplishlistdiredawa(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ድሬዳዋ'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishldiredawa.html', context)

def accomplishlistjimma(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ጅማ'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishljimma.html', context)

def accomplishlistsodo(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ሶዶ'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishlsodo.html', context)

def accomplishlistgode(request):
    acom = Accomplishment.objects.filter(Q(bapmonth__icontains='ሐምሌ'), Q(erabudget__bdistrict__icontains='ጎዴ'))
    context = {}
    context = {'acom':acom}
    return render(request, 'rasmApp/accomplishlgode.html', context)

def backtodis(request):
    return render(request, 'rasmApp/backtodistrict.html')

def apacompupd(request):
    context = {}
    form = AccomplishmentForm()
    #searchworkt=request.GET.get('workt')
    #searchmonths=request.GET.get('months')

    apacomp = Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname='አለምገና')&Q(erabudget__bworktype__maintenancetype='መደበኛ ጥገና')&Q(bapmonth='ሐምሌ'))
    
    #context['searchworkt'] = searchworkt
    #context['searchmonths'] = searchmonths
    context['apacomp'] = apacomp
    context['title'] = 'APAccomplishment'
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form = AccomplishmentForm(request.POST)
            else:
                apac = Accomplishment.objects.get(id=pk)
                form = AccomplishmentForm(request.POST, instance=apac)
            form.save(update_fields=['actionInBr', 'actionInKm','unit','securityproblem','duetocontracttermination','underprocurementprocess','resourceshortages','rightofwayissues','other'])
            form = AccomplishmentForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            apac = Accomplishment.objects.get(id=pk)
            apac.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            apac = Accomplishment.objects.get(id=pk)
            form = AccomplishmentForm(instance=apac)
    context['form'] = form
    return render(request, 'rasmApp/apacomp_upd.html', context)
    
def bapacoml(request):
    apac = ERABudget.objects.all()
    myFilter = ERABudgetFilter(request.GET, queryset=apac)
    apac = myFilter.qs
    context = {
        'apac': apac,
        'myFilter': myFilter,
    }
    return render(request, 'rasmApp/filterbapacoml.html', context)


def accomplish_new(request):
    context ={}
    form = AccomplishmentForm(request.POST or None)
    if form.is_valid():
        form.save()
         
    context['form']= form
    return render(request, 'rasmApp/accomplishmentnew.html', context)


def accomplishments(request, id):
    context = {}
    acom = Accomplishment.objects.get(id=id)
    form = AccomplishmentForm(request.POST or None, instance=acom)
    if form.is_valid():
        form.save()
        #return redirect('search_example')
        #return HttpResponse(id)
        #return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    context = {'acom':acom,'form': form}
    return render(request, 'rasmApp/accomplish.html', context)

def accomplish_edit(request):
    return HttpResponse()    



def createAPSummary(request, pk):
    user = get_user(request)
    APSummaryFormSet = inlineformset_factory(BudgetedAP, APSummary, fields=('budgetedap','actionInBr','actionInKm','bremark1','bremark2'))
    budgetedap = BudgetedAP.objects.get(id=pk)
    formset = APSummaryFormSet(queryset=APSummary.objects.none(), instance=budgetedap)
        
    if request.method == 'POST':
        formset = APSummaryFormSet(request.POST, instance=budgetedap)
        if formset.is_valid():
            formset.save()
            if user=="01":
                return redirect('alemgena')
            elif user=="02":
                return redirect('nekemte')
            else:
                return redirect('baplist')
    context = {'formset':formset,'budgetedap':budgetedap}
    return render(request, 'rasmApp/apsummary_form.html', context)



def updateActionPlan(request, pk):
    actionplan = ActionPlan.objects.get(id=pk)
    form = ActionPlanForm(instance=actionplan)
    if request.method == 'POST':
        form = ActionPlanForm(request.POST, instance=actionplan)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'rasmApp/actionplan_form.html', context)

def deleteOrder(request, pk):
    actionplan = ActionPlan.objects.get(id=pk)
    form = ActionPlanForm(instance=actionplan)
    if request.method == 'POST':
        actionplan.delete()
        return redirect('home')
    context = {'item': actionplan}
    return render(request, 'rasmApp/delete.html', context)

def deleteActionPlan(request, pk):
    actionplan = ActionPlan.objects.get(id=pk)
    if request.method == "POST":
        actionplan.delete()
        return redirect('/')
    context={'item':actionplan}
    return render(request, 'rasmApp/delete.html', context)

@login_required(login_url='login')
def budgetList(request):
    q = request.GET.get('q')
    
    if q:
        annual_budget=ERABudget.objects.filter(Q(bdistrict__districtname__icontains=q)|Q(bproject__project__icontains=q))
    else:
        annual_budget = ERABudget.objects.all()
    
    p = Paginator(annual_budget, 100)
    page_number = request.GET.get('page')
    
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    context = {'annual_budget':annual_budget, 'page_obj': page_obj}
    return render(request, 'rasmApp/budget_list.html', context)


def budgetlsearch(request):
    
    if request.method=="POST":
        searchbproject=request.POST.get('bproject')
        searchbcontractor=request.POST.get('bcontractor')
        bsearch=ERABudget.objects.filter(Q(bproject=searchbproject) | Q(bcontractor=searchbcontractor))

        return render(request,'rasmApp/budgetlistsearch.html',{"data":bsearch})
    else:
        bsearch=ERABudget.objects.all()
        return render(request,'rasmApp/budgetlistsearch.html',{"data":bsearch})


def bap_list(request):
    #q = request.GET.get('q')
    
    #if q:
    #    bap=BudgetedAP.objects.filter(Q(erabudget__bdistrict__icontains=q)|Q(month__icontains=q))
    #else:
    #    bap = BudgetedAP.objects.all()    
    bap=BudgetedAP.objects.filter(month__icontains="ሐምሌ")
    
    p = Paginator(bap, 100)
    page_number = request.GET.get('page')

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)

    #bap = BudgetedAP.objects.all()
    context = {'bap':bap, 'page_obj': page_obj}
    return render(request,'rasmApp/baplist.html', context )


def districtAll(request,pk):
    dist = District.objects.get(id=pk)
    context = {'dist':dist}
    return render(request, 'rasmApp/alldistrict.html', context )

#def summaryBudget(request, pk):
#    return render(request, 'rasmApp/groupbudget.html', {})

def districtalemgena(request):
    context = {}
    q = request.GET.get('d')
    
    if q == 'አለምገና':
        districtb = ERABudget.objects.filter(bdistrict__districtname__icontains=q)#(Q(erabudget__bdistrict__districtname__icontains=q)|Q(month__icontains = 'ሐምሌ'))
    elif q == 'አዲግራት':
        districtb = ERABudget.objects.filter(bdistrict__districtname__icontains=q)
    else:
        districtb = ERABudget.objects.all()
    
    context = {'districtb':districtb} 
    
    return render(request, 'rasmApp/alemgena.html', context)

def districtadigrat(request):
    adigrat = ERABudget.objects.filter(bdistrict__districtname__icontains="አዲግራት")
    context = {'adigrat':adigrat}
    return render(request, 'rasmApp/adigratl.html', context)

def districtkombolcha(request):
    kombolcha = ERABudget.objects.filter(bdistrict__districtname__icontains="ኮምቦልቻ")
    context = {'kombolcha':kombolcha}
    return render(request, 'rasmApp/kombolchal.html', context)

def districtdebremarkos(request):
    debremarkos = ERABudget.objects.filter(bdistrict__districtname__icontains="ደብረ ማርቆስ")
    context = {'debremarkos':debremarkos}
    return render(request, 'rasmApp/debremarkosl.html', context)

def districtgondar(request):
    gondar = ERABudget.objects.filter(bdistrict__districtname__icontains="ጎንደር")
    context = {'gondar':gondar}
    return render(request, 'rasmApp/gondarl.html', context)

def districtshashamane(request):
    shashamane = ERABudget.objects.filter(bdistrict__districtname__icontains="ሻሸመኔ")
    context = {'shashamane':shashamane}
    return render(request, 'rasmApp/shashamanel.html', context)

def districtnekemte(request):
    nekemt = ERABudget.objects.filter(bdistrict__districtname__icontains="ነቀምት")
    context = {'nekemt':nekemt}
    return render(request, 'rasmApp/nekemte.html', context)

def districtdiredawa(request):
    diredawa = ERABudget.objects.filter(bdistrict__districtname__icontains="ድሬዳዋ")
    context = {'diredawa':diredawa}
    return render(request, 'rasmApp/diredawal.html', context)

def districtjimma(request):
    jimma = ERABudget.objects.filter(bdistrict__districtname__icontains="ጅማ")
    context = {'jimma':jimma}
    return render(request, 'rasmApp/jimmal.html', context)

def districtsodo(request):
    sodo = ERABudget.objects.filter(bdistrict__districtname__icontains="ሶዶ")
    context = {'sodo':sodo}
    return render(request, 'rasmApp/sodol.html', context)

def districtgode(request):
    gode = ERABudget.objects.filter(bdistrict__districtname__icontains="ጎዴ")
    context = {'gode':gode}
    return render(request, 'rasmApp/godel.html', context)


def budgetedap(request):
    context = {}
    form = BudgetedAPForm()
    ap = BudgetedAP.objects.all()
    context['acplan'] = ap
    context['title'] = 'Action Plan'
    if request.method == 'POST':
        if 'save' in request.POST:
            pk = request.POST.get('save')
            if not pk:
                form = BudgetedAPForm(request.POST)
            else:
                ap = BudgetedAP.objects.get(id=pk)
                form = BudgetedAPForm(request.POST, instance=ap)
            form.save()
            form = BudgetedAPForm()
        elif 'delete' in request.POST:
            pk = request.POST.get('delete')
            ap = BudgetedAP.objects.get(id=pk)
            ap.delete()
        elif 'edit' in request.POST:
            pk = request.POST.get('edit')
            ap = BudgetedAP.objects.get(id=pk)
            form = BudgetedAPForm(instance=ap)

    context['form'] = form
    return render(request, 'rasmApp/bactionplan.html', context)


def apsummaryrpt(request):  #Action plan summary report
    #context = {}
    #acplan = BudgetedAP.objects.all()
    #if request.method == 'POST':
    #    ap_form = BudgetedAPForm(request.POST)
    #    apsummary_form = APSummaryForm(request.POST)
    #    if ap_form.is_valid() and apsummary_form.is_valid():
    #        ap_form.save()
    #        apsummary_form.save()
    #context = {'acplan':acplan, 'ap_form':ap_form, 'apsummary_form':apsummary_form}
    return render(request, 'rasmApp/bactionplan.html')



def summarydata(request):
    budgetsall = ERABudget.objects.all().order_by('id')
    budgetsall_pivot = pivot(ERABudget, 'bdistrict', 'bproject', 'budgetamount', include_total=True)
    
    ball = BudgetedAP.objects.all().order_by('-erabudget__bprojectname')
    ball_pivot = pivot(BudgetedAP, 'erabudget__bprojectname', 'month', 'bapinBr', include_total=True)
    
    
    return render(request,'rasmApp/budgetsummary.html',
                {'budgetsall':budgetsall,'budgetsall_pivot':budgetsall_pivot, 'ball':ball,'ball_pivot':ball_pivot})

def roadtypesummary(request):
    qs = BudgetExt.objects.all()
    pvt = pivot(BudgetExt, 'budget__projectName', 'roadT', 'lenToBeMaintained', include_total=True)
    
    return render(request,'rasmApp/roadsummary.html', {'qs':qs, 'pvt':pvt})


    
def AnnualBudgetS(request):
    qs = ERABudget.objects.all().values()
    df = pd.DataFrame(qs)
    pt = df.pivot_table(index='bdistrict', columns='bproject', values='budgetAmt', aggfunc='sum')
    pt.to_excel('MyPD.xlsx','Pivot_Data',startrow=2)
    
    
    return render(request,'rasmApp/annualbudget.html', {'pt':pt})

    #return HttpResponse(pt)

@login_required(login_url='login')
def export_to_excel(request, file_format):
    budgets = ERABudget.objects.all().values()
    df = pd.DataFrame(list(budgets))
    
    #file_format=request.GET.get('file_format')
    if file_format == 'excel':
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=budget.xlsx'
        df.to_excel(response, index=False, engine='openpyxl')
    elif file_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=budget.csv'
        df.to_csv(response, index=False)
    elif file_format == 'json':
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=budget.json'
        response.write(df.to_json(orient='records'))
    else:
        response = HttpResponse("Unsupported format", status=400)
    return response
    #return render(request, 'rasmApp/export.html')    


@login_required(login_url='login')
def ActionPlanList(request):
    context = {}
    aplist = BudgetedAP.objects.all()
    aplist_pivot = pivot(BudgetedAP, 'erabudget__bprojectname', 'month', 'bapinBr', include_total=True)
    
    context = {'aplist': aplist, 'aplist_pivot': aplist_pivot}
    return render(request, 'rasmApp/aplist.html', context)


@login_required(login_url='login')
def budgetperdisperprojtype(request):
    context = {}
    budgetlist = ERABudget.objects.all()
    budgetlist_pivot = pivot(ERABudget, 'bdistrict__districtname', 'bproject', 'budgetamount', include_total=True)

    context = {'budgetlist': budgetlist, 'budgetlist_pivot': budgetlist_pivot}
    return render(request, 'rasmApp/budgetpdispprojtype.html', context)

def worktypeperapnaccomp(request):
    context = {}
    aplist = BudgetedAP.objects.all()
    aplist_pivot = pivot(BudgetedAP, 'erabudget__bworktype__maintenancetype', 'month', 'bapinBr', include_total=True)

    context = {'aplist': aplist, 'aplist_pivot': aplist_pivot}
    return render(request, 'rasmApp/worktype_apaccomp.html', context)



def grouped_items(request):
    erabudget = ERABudget.objects.prefetch_related("budgetedap_set")
    busum = BudgetedAP.objects.count()   #.annotate(total_value1=Sum('bapinBr'))
    bp = BudgetedAP.objects.filter(erabudget__bprojectname__icontains="ሙከጡሪ ሴክሽን መደበኛ ጥገና").aggregate(total_value=Sum("bapinBr", output_field=FloatField()))   #.annotate(total_value1=Sum('bapinBr'))
    
    
    # Perform the GROUP BY query using Django's ORM
    grouped_data = BudgetedAP.objects.values('erabudget__bworktype__maintenancetype').annotate(
        total_value1=Sum('bapinBr'),
        total_value2=Sum('bapinKm'),
        total_value3=Sum('accomplishment__actionInBr'),
        total_value4=Sum('accomplishment__actionInKm'),
        group_count=Count('month')
    )

    # Calculate the sum of all values
    total_sum1 = BudgetedAP.objects.aggregate(total_sum1=Sum('bapinBr'))['total_sum1']
    total_sum2 = BudgetedAP.objects.aggregate(total_sum2=Sum('bapinKm'))['total_sum2']
    
    #tsum1 = sum(grouped_data.values_list('total_value1', flat=True))
    #tsum2 = sum(grouped_data.values_list('total_value2', flat=True))

    return render(request, 'rasmApp/grouped_items.html', {
        'grouped_data': grouped_data,
        'total_sum1': total_sum1, 
        'total_sum2': total_sum2,
        'erabudget':erabudget,
        'busum':busum,
        'bp':bp,
    })


def budgetsummary(request):
    budgets = ERABudget.objects.all()
    result = ERABudget.objects.values('bproject').annotate(total_price=Sum('budgetamount'),total_asphalt=Sum('basphalt'))    


    budgets_transposed_dd = defaultdict(list)  
    for budget in budgets:                                                        ## New   
        budgets_transposed_dd[budget.bdistrict].append((budget.bproject, budget.budgetamount))  ## New
    
    #cols = max(budgets_transposed_dd.values()) ## New
    
    return render(request,'rasmApp/groupbudget.html',
                {'budgets':budgets,
                'budgets_transposed_dd':dict(budgets_transposed_dd), 'result':result} )  ## New


@login_required(login_url='login')
def apperprojectpermonth(request):
    erabudget = ERABudget.objects.prefetch_related("budgetedap_set")

    return render(request, 'rasmApp/appprojectpmonth.html', {'erabudget':erabudget})

@login_required(login_url='login')
def summarybyworktype(request):
    context = {}
    allap = BudgetedAP.objects.values('erabudget__bworktype__maintenancetype', 'month').filter(Q(erabudget__bworktype__id=1)|Q(erabudget__bworktype__id=2)|Q(erabudget__bworktype__id=3)).annotate(SegmentCount=Count('erabudget__broadsegment')).annotate(APtotal_Km=Sum('bapinKm')).annotate(Acomptotal_Km=Sum('accomplishment__actionInKm')).order_by('erabudget__bworktype__maintenancetype')


    aps = BudgetedAP.objects.all().values('erabudget__bworktype__maintenancetype','month').filter(Q(erabudget__bworktype__id=1)|Q(erabudget__bworktype__id=2)|Q(erabudget__bworktype__id=3)).annotate(total_Br=Sum('bapinBr')).order_by('month')

    apsall = BudgetedAP.objects.all()
    apsall_pivot = pivot(BudgetedAP, 'erabudget__bworktype__maintenancetype', 'month', 'bapinKm', include_total=True)


    t_allap = list(zip(*allap))
    
    df = read_frame(allap)
    table_html = df.transpose().to_html()
    #allap = BudgetedAP.objects.filter(month__iexact = 'ሐምሌ') #[0:100] #filter(bworktype__iexact = 'መደበኛ ጥገና') #(bapinKm__exact = 0.5) #all()[0:100]#filter(bworktype="መደበኛ ጥገና").values()

    pivot_table_dictionary = pivot(BudgetedAP,
                               'erabudget__bworktype__maintenancetype',
                               'month',
                               'bapinBr')
    
    #return HttpResponse(table_html)
    context = {'allap':allap, 't_allap':t_allap, 'table_html': table_html, 'aps':aps, 'apsall':apsall,'apsall_pivot':apsall_pivot}
    return render(request, 'rasmApp/byworktype.html', context)

@login_required(login_url='login')
def acompsummarybyworktype(request):
    context = {}

    aps = BudgetedAP.objects.all().values('erabudget__bworktype__maintenancetype','month').filter(Q(erabudget__bworktype__id=1)|Q(erabudget__bworktype__id=2)|Q(erabudget__bworktype__id=3)).annotate(total_km=Sum('bapinKm')).order_by('month')

    aps_pivot = pivot(aps, 'erabudget__bworktype__maintenancetype', 'month', 'bapinKm', include_total=True)

    apsall = Accomplishment.objects.all()
    apsall_pivot = pivot(Accomplishment, 'erabudget__bworktype__maintenancetype', 'bapmonth', 'actionInKm', include_total=True)
        
    context = {'aps':aps, 'apsall':apsall,'apsall_pivot':apsall_pivot, 'aps_pivot':aps_pivot}
    return render(request, 'rasmApp/acompbyworktype.html', context)

    
@login_required(login_url='login')
def budgetperworktype(request):
    grouped_data = BudgetedAP.objects.exclude(Q(erabudget__bworktype__maintenancetype='የካሳ ክፍያ')| Q(erabudget__bworktype__maintenancetype='ኤርጎኖሚክስ')| Q(erabudget__bworktype__maintenancetype='የመንገድ ደህንነት ስራ')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ ስራዎች')| Q(erabudget__bworktype__maintenancetype='የማማከር አገልግሎት')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ የማዘመን ስራዎች')| Q(erabudget__bworktype__maintenancetype='ድልድይ መልሶ ግንባታ')| Q(erabudget__bworktype__maintenancetype='ድልድይ/ፉካ ጥገና ስራ')).values('erabudget__bworktype__maintenancetype').annotate(
        APtotalBr=Sum('bapinBr'),
        APtotalKm=Sum('bapinKm'),
        AcomptotalBr=Sum('accomplishment__actionInBr'),
        AcomptotalKm=Sum('accomplishment__actionInKm'),
        group_count=Count('month')
    )
    total_sum1 = grouped_data.aggregate(total_sum1=Sum('APtotalBr'))['total_sum1']
    total_sum2 = grouped_data.aggregate(total_sum2=Sum('APtotalKm'))['total_sum2']
    total_sum3 = grouped_data.aggregate(total_sum3=Sum('AcomptotalBr'))['total_sum3']
    total_sum4 = grouped_data.aggregate(total_sum4=Sum('AcomptotalKm'))['total_sum4']
    
    return render(request, 'rasmApp/budgetpworktype.html', {
        'grouped_data': grouped_data,
        'total_sum1': total_sum1, 
        'total_sum2': total_sum2,
        'total_sum3': total_sum3,
        'total_sum4': total_sum4
    })
    
def projectpermonth(request):
    ppm = BudgetedAP.objects.filter(month__icontains=1).annotate(
        comp=(F('accomplishment__actionInKm')/F('bapinKm'))*100)
    #apm = BudgetedAP.objects.values('month')
    
    apm = (BudgetedAP.objects
    .filter(month__icontains=2)
    .annotate(comp=(F('accomplishment__actionInKm')/F('bapinKm'))*100)#total=Sum('bapinBr')
    )
    zppm = zip(ppm, apm)
    
    ap = BudgetedAP.objects.all().values('month').annotate(total=Sum('bapinBr'))
    accomp = Accomplishment.objects.all().values('bapmonth')
    #zapaccomp = zip(ap, accomp)
    
    #apm = Accomplishment.objects.filter(month__icontains="ሐምሌ")
    #papm = ERABudget.objects.prefetch_related("budgetedap_set", "accomplishment_set")
    
    erabudgetap = ERABudget.objects.prefetch_related("budgetedap_set")
    erabudgetacomp = ERABudget.objects.prefetch_related("accomplishment_set")
    #zbapacomp = zip(erabudgetap, erabudgetacomp)
    
    projectl = ERABudget.objects.values('bproject').annotate(total_value = Sum('budgetamount'))
    ppm2 = BudgetedAP.objects.values('erabudget__bworktype','month','accomplishment__actionInKm').annotate(total_value = Sum('bapinKm')).order_by('month')
    
    
    #bapyr = BudgetedAP.objects.all()
    #baccompyr = Accomplishment.objects.all()
 
    #combined_queryset = list(chain(bapyr, baccompyr))
    
    
    workt = ERABudget.objects.values('bworktype').annotate(total_count= Count('bworktype')).annotate(total=Sum('budgetedap__bapinBr'))
    
    #budgetsall = ERABudget.objects.all().order_by('bproject')
    #budgetsall_pivot = pivot(ERABudget, 'bdistrict', 'bproject', 'budgetamount', include_total=True)  
    
    qs = BudgetedAP.objects.all()
    #df = read_frame(qs)
    df = read_frame(qs, fieldnames=['erabudget', 'month', 'bapinBr'])
    df = df.pivot_table(values='bapinBr', index='erabudget', columns='month')
    
    #ppm = BudgetedAP.objects.values('erabudget__bprojectname').annotate(group_count=Sum('bapinBr'))
    return render(request, 'rasmApp/ppm.html', {'ppm':ppm, 'projectl':projectl, 'df':df.to_html, 'ppm2':ppm2, 'apm':apm, 'zppm':zppm, 'ap': ap, 'workt': workt, 'erabudgetap':erabudgetap, 'erabudgetacomp':erabudgetacomp})

@login_required(login_url='login')
def budgetperprojectype(request):
    projectl = ERABudget.objects.values('bproject__project', 'bworktype__maintenancetype').annotate(total_value = Sum('budgetamount'))
    tsum = sum(projectl.values_list('total_value', flat=True))
    return render(request, 'rasmApp/budgetpproject.html',{'projectl':projectl, 'tsum':tsum})

@login_required(login_url='login')
def apcompaccomplish(request):
    #ppm = BudgetedAP.objects.filter(month__icontains=1).annotate(comp=(F('accomplishment__actionInBr')/F('bapinBr'))*100)
    
    ppm = BudgetedAP.objects.filter(month__icontains=1).annotate(
        comp=(F('accomplishment__actionInKm')/F('bapinKm'))*100)
    
    apm = (BudgetedAP.objects
    .filter(month__icontains=2)
    .annotate(comp=(F('accomplishment__actionInKm')/F('bapinKm'))*100)#total=Sum('bapinBr')
    )
    zppm = zip(ppm, apm)
    
    
    #q = request.GET.get('q')
    
    #if q:
    #    ppm = zppm.filter(erabudget__bprojectname__icontains=q)
    #else:
    #    zppm
    
    #p = Paginator(zppm, 20)
    #page_number = request.GET.get('page')    

    #try:
    #    page_obj = p.get_page(page_number)  # returns the desired page object
    #except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
    #    page_obj = p.page(1)
    #except EmptyPage:
        # if page is empty then return last page
    #    page_obj = p.page(p.num_pages)    
    
    return render(request, 'rasmApp/apcompacomplish.html',{'zppm':zppm})#, 'page_obj': page_obj})


def apwithacomp(request):
    appm1 = BudgetedAP.objects.filter(month__icontains="ሐምሌ").annotate(
        comp=(F('accomplishment__actionInKm')/F('bapinKm'))*100
    )

    appm2 = BudgetedAP.objects.filter(month__icontains="ሐምሌ").annotate(
        comp=(F('accomplishment__actionInKm')/F('bapinKm'))*100)
    #apm = BudgetedAP.objects.values('month')
    
    apm = (BudgetedAP.objects
    .filter(month__icontains="ነሃሴ")
    .annotate(comp=(F('accomplishment__actionInBr')/F('bapinBr'))*100)#total=Sum('bapinBr')
    )
    #zppm = zip(appm1, appm2)

    return render(request, 'rasmApp/ap_accomp.html',{'ppm':appm1})


@login_required(login_url='login')
def budgetperprojectname(request):
    q = request.GET.get('q')
    
    if q:
        bplst = BudgetedAP.objects.filter(Q(erabudget__bproject__project__icontains=q)|Q(erabudget__bprojectname__icontains=q)).values('erabudget__bprojectname', 'erabudget__bproject__project').annotate(total_value=Sum("bapinBr", output_field=FloatField())).order_by('id')
    else:
        bplst = BudgetedAP.objects.values('erabudget__bprojectname', 'erabudget__bproject__project').annotate(total_value=Sum("bapinBr", output_field=FloatField())).order_by('id')
    
    p = Paginator(bplst, 20)
    page_number = request.GET.get('page')
    pcount = p.count
    

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(p.num_pages)
    
    return render(request, 'rasmApp/budgetpprojectname.html',{'page_obj': page_obj, 'bplst':bplst, 'pcount':pcount})

def financerwithcontractor(request):
    gdata = ERABudget.objects.values('bfinancer__financerName','bcontractor','bworktype__maintenancetype').annotate(
        total_budget=Sum('budgetamount'),
        total_asphalt=Sum('basphalt'),
        total_gravel=Sum('bgravel'),
        group_count=Count('id')
    )

    # Calculate the sum of all values
    gtotal_budget = ERABudget.objects.aggregate(gtotal_budget=Sum('budgetamount'))['gtotal_budget']
    gtotal_asphalt = ERABudget.objects.aggregate(gtotal_asphalt=Sum('basphalt'))['gtotal_asphalt']
    gtotal_gravel = ERABudget.objects.aggregate(gtotal_gravel=Sum('bgravel'))['gtotal_gravel']
    
    return render(request, 'rasmApp/finwithcontractor.html', {
        'gdata': gdata,
        'total_sum_budget': gtotal_budget,
        'gtotal_asphalt':gtotal_asphalt,
        'gtotal_gravel':gtotal_gravel
    })

@login_required(login_url='login')
def financerpercontractor(request):
    ownfdata = ERABudget.objects.filter(Q(bfinancer__financerName__icontains='መንገድ ፈንድ')&Q(bcontractor__icontains='የራስ ሀይል ተቋራጭ')).values('bfinancer__financerName','bcontractor','bworktype__maintenancetype').annotate(
        total_budget=Sum('budgetamount'),
        total_asphalt=Sum('basphalt'),
        total_gravel=Sum('bgravel'),
        tsum=Sum('basphalt') + Sum('bgravel'),
        group_count=Count('id')
    )

    ownfbsum = ownfdata.aggregate(ownfbsum=Sum('total_budget'))['ownfbsum']
    ownfasphsum = ownfdata.aggregate(ownfasphsum=Sum('total_asphalt'))['ownfasphsum']
    ownfgrvsum = ownfdata.aggregate(ownfgrvsum=Sum('total_gravel'))['ownfgrvsum']
    
    pvtfdata = ERABudget.objects.filter(Q(bfinancer__financerName__icontains='መንገድ ፈንድ')&Q(bcontractor__icontains='የግል ሥራ ተቋራጭ')).values('bfinancer__financerName','bcontractor','bworktype__maintenancetype').annotate(
        total_budget=Sum('budgetamount'),
        total_asphalt=Sum('basphalt'),
        total_gravel=Sum('bgravel'),
        tsum=Sum('basphalt') + Sum('bgravel'),
        group_count=Count('id')
    )
    pvtbsum = pvtfdata.aggregate(pvtbsum=Sum('total_budget'))['pvtbsum']
    pvtasphsum = pvtfdata.aggregate(pvtasphsum=Sum('total_asphalt'))['pvtasphsum']
    pvtgrvsum = pvtfdata.aggregate(pvtgrvsum=Sum('total_gravel'))['pvtgrvsum']

    consultdata = ERABudget.objects.filter(Q(bfinancer__financerName__icontains='መንገድ ፈንድ')&Q(bcontractor__icontains='የማማከር አገልግሎት')).values('bfinancer__financerName','bcontractor','bworktype__maintenancetype').annotate(
        total_budget=Sum('budgetamount'),
        total_asphalt=Sum('basphalt'),
        total_gravel=Sum('bgravel'),
        tsum=Sum('basphalt') + Sum('bgravel'),
        group_count=Count('id')
    )
    consbsum = consultdata.aggregate(consbsum=Sum('total_budget'))['consbsum']
    consasphsum = consultdata.aggregate(consasphsum=Sum('total_asphalt'))['consasphsum']
    consgrvsum = consultdata.aggregate(consgrvsum=Sum('total_gravel'))['consgrvsum']

    purchasedata = ERABudget.objects.filter(Q(bfinancer__financerName__icontains='መንገድ ፈንድ')&Q(bcontractor__icontains='በግዢ ሂደት ላይ')).values('bfinancer__financerName','bcontractor','bworktype__maintenancetype').annotate(
        total_budget=Sum('budgetamount'),
        total_asphalt=Sum('basphalt'),
        total_gravel=Sum('bgravel'),
        tsum=Sum('basphalt') + Sum('bgravel'),
        group_count=Count('id')
    )
    purchbsum = purchasedata.aggregate(purchbsum=Sum('total_budget'))['purchbsum']
    purchasphsum = purchasedata.aggregate(purchasphsum=Sum('total_asphalt'))['purchasphsum']
    purchgrvsum = purchasedata.aggregate(purchgrvsum=Sum('total_gravel'))['purchgrvsum']

    return render(request, 'rasmApp/financerpercontractor.html', {
        'ownfdata': ownfdata,
        'pvtfdata': pvtfdata,
        'consultdata':consultdata,
        'purchasedata':purchasedata,
        'ownfbsum':ownfbsum,
        'ownfasphsum': ownfasphsum, 'ownfgrvsum': ownfgrvsum, 'pvtbsum': pvtbsum, 'pvtasphsum':pvtasphsum,
        'pvtgrvsum':pvtgrvsum, 'consbsum':consbsum, 'consasphsum':consasphsum, 'consgrvsum':consgrvsum,
        'purchbsum':purchbsum, 'purchasphsum':purchasphsum, 'purchgrvsum':purchgrvsum
    })

@login_required(login_url='login')
def bsummary(request):    
    alldata = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ከባድ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype').annotate(
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm'),
        comp=(Sum('actionInKm')/Sum('budgetedap__bapinKm'))*100
        ).order_by('budgetedap__month')
    
    htaplen = alldata.aggregate(htaplen=Sum('total_aplen'))['htaplen']
    htaccomplen = alldata.aggregate(htaccomplen=Sum('total_accomplen'))['htaccomplen']
    hper = (htaccomplen / htaplen)*100
    
    alldata2 = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ወቅታዊ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype').annotate(
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm'),
        comp=(Sum('actionInKm')/Sum('budgetedap__bapinKm'))*100
        ).order_by('budgetedap__month')
    
    rtaplen = alldata2.aggregate(rtaplen=Sum('total_aplen'))['rtaplen']
    rtaccomplen = alldata2.aggregate(rtaccomplen=Sum('total_accomplen'))['rtaccomplen']
    rper = (rtaccomplen / rtaplen)*100
    
    alldata3 = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='መደበኛ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype').annotate(
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm'),
        comp=(Sum('actionInKm')/Sum('budgetedap__bapinKm'))*100
        ).order_by('budgetedap__month')
    
    ptaplen = alldata3.aggregate(ptaplen=Sum('total_aplen'))['ptaplen']
    ptaccomplen = alldata3.aggregate(ptaccomplen=Sum('total_accomplen'))['ptaccomplen']
    pper = (ptaccomplen / ptaplen)*100

    
    return render(request, 'rasmApp/btemplate.html', {'alldata':alldata, 'alldata2':alldata2, 'alldata3':alldata3, 'htaplen':htaplen, 'htaccomplen':htaccomplen, 'rtaplen':rtaplen, 'rtaccomplen':rtaccomplen, 'ptaplen':ptaplen, 'ptaccomplen':ptaccomplen, 'hper':hper, 'rper':rper, 'pper':pper})    

@login_required(login_url='login')
def finbsummary(request):    
    alldata = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ከባድ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype').annotate(
        total_aplen=Sum('budgetedap__bapinBr'),
        total_accomplen=Sum('actionInBr'),
        comp=(Sum('actionInBr')/Sum('budgetedap__bapinBr'))*100
        ).order_by('budgetedap__month')
    
    htaplen = alldata.aggregate(htaplen=Sum('total_aplen'))['htaplen']
    htaccomplen = alldata.aggregate(htaccomplen=Sum('total_accomplen'))['htaccomplen']
    hper = (htaccomplen / htaplen)*100
    
    alldata2 = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ወቅታዊ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype').annotate(
        total_aplen=Sum('budgetedap__bapinBr'),
        total_accomplen=Sum('actionInBr'),
        comp=(Sum('actionInBr')/Sum('budgetedap__bapinBr'))*100
        ).order_by('budgetedap__month')
    
    rtaplen = alldata2.aggregate(rtaplen=Sum('total_aplen'))['rtaplen']
    rtaccomplen = alldata2.aggregate(rtaccomplen=Sum('total_accomplen'))['rtaccomplen']
    rper = (rtaccomplen / rtaplen)*100
    
    alldata3 = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='መደበኛ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype').annotate(
        total_aplen=Sum('budgetedap__bapinBr'),
        total_accomplen=Sum('actionInBr'),
        comp=(Sum('actionInBr')/Sum('budgetedap__bapinBr'))*100
        ).order_by('budgetedap__month')
    
    ptaplen = alldata3.aggregate(ptaplen=Sum('total_aplen'))['ptaplen']
    ptaccomplen = alldata3.aggregate(ptaccomplen=Sum('total_accomplen'))['ptaccomplen']
    pper = (ptaccomplen / ptaplen)*100

    
    return render(request, 'rasmApp/fin_maintenance_summary.html', {'alldata':alldata, 'alldata2':alldata2, 'alldata3':alldata3, 'htaplen':htaplen, 'htaccomplen':htaccomplen, 'rtaplen':rtaplen, 'rtaccomplen':rtaccomplen, 'ptaplen':ptaplen, 'ptaccomplen':ptaccomplen, 'hper':hper, 'rper':rper, 'pper':pper})    

def annualapvsaccomp(request):    
    alldata = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ከባድ ጥገና').values('bapmonth', 'erabudget__bworktype__maintenancetype','erabudget__broadsegment').annotate(
        #total_count=Count('erabudget__broadsegment'),
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm')
        ).order_by('budgetedap__month')
    
    alldata2 = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ወቅታዊ ጥገና').values('bapmonth', 'erabudget__bworktype__maintenancetype','erabudget__broadsegment').annotate(
        #total_count=Count('erabudget__broadsegment'),
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm')
        ).order_by('budgetedap__month')
    
    alldata3 = Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='መደበኛ ጥገና').values('bapmonth', 'erabudget__bworktype__maintenancetype','erabudget__broadsegment').annotate(
        #total_count=Count('erabudget__broadsegment'),
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm')
        ).order_by('budgetedap__month')
    
    
    heavymaintenanc=Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ከባድ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype','erabudget__broadsegment').annotate(
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm')
        ).order_by('budgetedap__month')
    
    periodicmaint=Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='ወቅታዊ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype','erabudget__broadsegment').annotate(
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm')
        ).order_by('budgetedap__month')
    
    routinmaint=Accomplishment.objects.filter(erabudget__bworktype__maintenancetype='መደበኛ ጥገና').values('bapmonth','erabudget__bworktype__maintenancetype','erabudget__broadsegment').annotate(
        total_aplen=Sum('budgetedap__bapinKm'),
        total_accomplen=Sum('actionInKm')
        ).order_by('budgetedap__month')
    
    htaplen = heavymaintenanc.aggregate(htaplen=Sum('total_aplen'))['htaplen']
    htaccomplen = heavymaintenanc.aggregate(htaccomplen=Sum('total_accomplen'))['htaccomplen']
    
    
    return render(request, 'rasmApp/yearlyapvsaccomp.html', {'alldata':alldata, 'alldata2':alldata2, 'alldata3':alldata3, 'heavymaintenanc':heavymaintenanc,'periodicmaint':periodicmaint, 'routinmaint':routinmaint, 'htaplen':htaplen, 'htaccomplen':htaccomplen})    


def export_to_csv(request):
    output = []
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    query_set = ERABudget.objects.all()
    #Header
    writer.writerow(['bdistrict', 'bfinancer', 'bproject', 'bprojectname','bworktype','bregion','bcontractor','bcontractorname','bconsultant','broadsegment','byear','budgetamount','basphalt','bgravel'])
    for b in query_set:
        output.append([b.bdistrict, b.bfinancer, b.bproject, b.bprojectname,b.bworktype,b.bregion,b.bcontractor,b.bcontractorname,b.bconsultant,b.broadsegment,b.byear,b.budgetamount,b.basphalt,b.bgravel])
    #CSV Data
    writer.writerows(output)
    return response


def search_accomplish(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አለምገና')&Q(erabudget__bworktype__maintenancetype=searchworkt)&Q(bapmonth=searchmonths))
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አለምገና')&Q(erabudget__bworktype__maintenancetype=searchworkt))#[0:100] 
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አለምገና')&Q(bapmonth=searchmonths))#[0:100] 
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='አለምገና')#[0:100]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/search_example.html', context_dict)

@login_required(login_url='login')
def accomplishment_admin(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('dist') and request.GET.get('workt') and request.GET.get('months'):
        searchdistrict=request.GET.get('dist')
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=searchdistrict)&Q(erabudget__bworktype__maintenancetype=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('dist') and request.GET.get('workt'):
        searchdistrict=request.GET.get('dist')
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=searchdistrict)&Q(erabudget__bworktype__maintenancetype=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('dist') and request.GET.get('months'):
        searchdistrict=request.GET.get('dist')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains=searchdistrict)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bworktype__maintenancetype=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('dist'):
        searchdistrict=request.GET.get('dist')
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains=searchdistrict).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(erabudget__bworktype__maintenancetype=searchworkt).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(bapmonth=searchmonths).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.all()[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/adminaccomplish.html', context_dict)

def accomplishment_update(request):
    
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አለምገና')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)        
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አለምገና')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100) 
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አለምገና')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100) 
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='አለምገና')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/accomplishment_reg.html', context_dict)

def accomplishment_update_adigrat(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አዲግራት')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አዲግራት')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100) 
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='አዲግራት')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100) 
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='አዲግራት')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/adigrataccompreg.html', context_dict)

def accomplish_upd_kombolcha(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ኮምቦልቻ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ኮምቦልቻ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ኮምቦልቻ')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ኮምቦልቻ')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/kombolchaaccompreg.html', context_dict)

def accomplish_upd_debremarkos(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ደብረ ማርቆስ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ደብረ ማርቆስ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ደብረ ማርቆስ')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ደብረ ማርቆስ')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/debremarkosaccompreg.html', context_dict)

def accomplish_upd_gondar(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጎንደር')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጎንደር')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጎንደር')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ጎንደር')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/gondaraccompreg.html', context_dict)

def accomplish_upd_shashamane(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ሻሸመኔ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ሻሸመኔ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ሻሸመኔ')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ሻሸመኔ')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/shashamaneaccompreg.html', context_dict)

def accomplish_upd_nekemte(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ነቀምት')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ነቀምት')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ነቀምት')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ነቀምት')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/nekemteaccompreg.html', context_dict)

def accomplish_upd_diredawa(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ድሬዳዋ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ድሬዳዋ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ድሬዳዋ')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ድሬዳዋ')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/diredawaaccompreg.html', context_dict)

def accomplish_upd_jimma(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጅማ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጅማ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጅማ')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ጅማ')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/jimmaaccompreg.html', context_dict)

def accomplish_upd_sodo(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ሶዶ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ሶዶ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ሶዶ')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ሶዶ')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/sodoaccompreg.html', context_dict)

def accomplish_upd_gode(request):
    searchworkt=request.GET.get('workt')
    searchmonths=request.GET.get('months')
    if request.GET.get('workt') and request.GET.get('months'):
        searchworkt=request.GET.get('workt')
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጎዴ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('workt'):
        searchworkt=request.GET.get('workt')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጎዴ')&Q(erabudget__bworktype__maintenancetype__icontains=searchworkt)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    elif request.GET.get('months'):
        searchmonths=request.GET.get('months')
        wtsearch=Accomplishment.objects.filter(Q(erabudget__bdistrict__districtname__icontains='ጎዴ')&Q(bapmonth=searchmonths)).annotate(comp=(F('actionInBr')/F('budgetedap__bapinBr'))*100, comp1=(F('actionInKm')/F('budgetedap__bapinKm'))*100)
    else:
        wtsearch=Accomplishment.objects.filter(erabudget__bdistrict__districtname__icontains='ጎዴ')[0:0]
    
    context_dict = {'data': wtsearch, 'worktype':searchworkt,'month': searchmonths}
    return render(request, 'rasmApp/godeaccompreg.html', context_dict)

def apaccompcomp(request):
    comppm = BudgetedAP.objects.filter(month='1').values('erabudget__bprojectname','bapinBr','bapinKm','accomplishment__actionInBr','accomplishment__actionInKm').annotate(compl=(F('accomplishment__actionInKm')/F('bapinKm'))*100, compf=(F('accomplishment__actionInBr')/F('bapinBr'))*100)
    ppm = BudgetedAP.objects.filter(month__icontains=1).annotate(
        comp=(F('accomplishment__actionInKm')/F('bapinKm'))*100)
    return render(request, 'rasmApp/apaccomp_comp.html', {'comppm':comppm})

def apaccompcompscnd(request):    
    comppmsecond = BudgetedAP.objects.filter(month=2).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projsecondzip = zip(comppmsecond,projapacompall)
    
    projaptpmbrsum = comppmsecond.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmsecond.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmsecond.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmsecond.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmsecond.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmsecond.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compscnd.html', {'projsecondzip':projsecondzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})

def apaccompcompthrd(request):    
    comppmthird = BudgetedAP.objects.filter(month=3).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projthirdzip = zip(comppmthird,projapacompall)
    
    projaptpmbrsum = comppmthird.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmthird.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmthird.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmthird.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmthird.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmthird.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compthrd.html', {'projthirdzip':projthirdzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})
    
def apaccompcompfrth(request):    
    comppmfourth = BudgetedAP.objects.filter(month=4).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projfourthzip = zip(comppmfourth,projapacompall)
    
    projaptpmbrsum = comppmfourth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmfourth.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmfourth.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmfourth.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmfourth.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmfourth.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compfrth.html', {'projfourthzip':projfourthzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})
    
def apaccompcompffth(request):    
    comppmfifth = BudgetedAP.objects.filter(month=5).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projfifthzip = zip(comppmfifth,projapacompall)
    
    projaptpmbrsum = comppmfifth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmfifth.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmfifth.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmfifth.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmfifth.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmfifth.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compffth.html', {'projfifthzip':projfifthzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})
    
def apaccompcompsixth(request):    
    comppmsixth = BudgetedAP.objects.filter(month=6).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projsixthzip = zip(comppmsixth,projapacompall)
    
    projaptpmbrsum = comppmsixth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmsixth.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmsixth.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmsixth.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmsixth.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmsixth.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compsixth.html', {'projsixthzip':projsixthzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})
    
def apaccompcompsevnth(request):    
    comppmseventh = BudgetedAP.objects.filter(month=7).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projseventhzip = zip(comppmseventh,projapacompall)
    
    projaptpmbrsum = comppmseventh.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmseventh.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmseventh.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmseventh.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmseventh.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmseventh.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compsevnth.html', {'projseventhzip':projseventhzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})
    
def apaccompcompeith(request):    
    comppmeighth = BudgetedAP.objects.filter(month=8).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projeighthzip = zip(comppmeighth,projapacompall)
    
    projaptpmbrsum = comppmeighth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmeighth.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmeighth.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmeighth.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmeighth.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmeighth.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compeith.html', {'projeighthzip':projeighthzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})
    
def apaccompcompninth(request):
    comppmnineth = BudgetedAP.objects.filter(month=9).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projninethzip = zip(comppmnineth,projapacompall)
    
    projaptpmbrsum = comppmnineth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmnineth.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmnineth.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmnineth.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmnineth.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmnineth.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compninth.html', {'projninethzip':projninethzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})
    
def apaccompcomptenth(request):
    comppmtenth = BudgetedAP.objects.filter(month=10).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projtenthzip = zip(comppmtenth,projapacompall)
    
    projaptpmbrsum = comppmtenth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmtenth.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmtenth.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmtenth.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmtenth.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmtenth.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_comptenth.html', {'projtenthzip':projtenthzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})

def apaccompcompelvnth(request):    
    comppmelvnth = BudgetedAP.objects.filter(month=11).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projeleventhzip = zip(comppmelvnth,projapacompall)
    
    projaptpmbrsum = comppmelvnth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmelvnth.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmelvnth.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmelvnth.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmelvnth.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmelvnth.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
    
    return render(request, 'rasmApp/apaccomp_compelvnth.html', {'projeleventhzip':projeleventhzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})

def apaccompcomplast(request): 
    comppmlast = BudgetedAP.objects.filter(month=12).values('erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')
    
    projapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget_id')

    projyrzip = zip(comppmlast,projapacompall)
    
    projaptpmbrsum = comppmlast.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    projacomptpmbrsum = comppmlast.aggregate(projacomptpmbrsum=Sum('acomptotalpmonthbr'))['projacomptpmbrsum']
    projaptpmkmsum = comppmlast.aggregate(projaptpmkmsum=Sum('aptotalpmonthkm'))['projaptpmkmsum']
    projacomptpmkmsum = comppmlast.aggregate(projacomptpmkmsum=Sum('acomptotalpmonthkm'))['projacomptpmkmsum']
    projfincomptpmsum = comppmlast.aggregate(projfincomptpmsum=Sum('fincomppmonth'))['projfincomptpmsum']
    projphycomptpmsum = comppmlast.aggregate(projphycomptpmsum=Sum('phycomppmonth'))['projphycomptpmsum']
    projaptbrsum = projapacompall.aggregate(projaptbrsum=Sum('aptotalbr'))['projaptbrsum']
    projacomptbrsum = projapacompall.aggregate(projacomptbrsum=Sum('acomptotalbr'))['projacomptbrsum']
    projaptkmsum = projapacompall.aggregate(projaptkmsum=Sum('aptotalkm'))['projaptkmsum']
    projacomptkmsum = projapacompall.aggregate(projacomptkmsum=Sum('acomptotalkm'))['projacomptkmsum']
    projfincompsum = projapacompall.aggregate(projfincompsum=Sum('fincomp'))['projfincompsum']
    projphycompsum = projapacompall.aggregate(projphycompsum=Sum('phycomp'))['projphycompsum']
        
    return render(request, 'rasmApp/apaccomp_complast.html', {'projyrzip':projyrzip, 'projaptpmbrsum':projaptpmbrsum, 'projacomptpmbrsum':projacomptpmbrsum, 'projaptpmkmsum':projaptpmkmsum, 'projacomptpmkmsum':projacomptpmkmsum, 'projfincomptpmsum':projfincomptpmsum, 'projphycomptpmsum':projphycomptpmsum, 'projaptbrsum':projaptbrsum, 'projacomptbrsum':projacomptbrsum, 'projaptkmsum':projaptkmsum, 'projacomptkmsum':projacomptkmsum, 'projfincompsum':projfincompsum, 'projphycompsum':projphycompsum})

def district_compare_firstmonth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmfirst = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmfirst = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmfirst = BudgetedAP.objects.filter(month=1).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(month=1).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')

    disfirstzip = zip(discomppmfirst,disapacompall)
    
    disaptpmbrsum = discomppmfirst.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmfirst.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmfirst.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmfirst.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmfirst.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmfirst.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compfirstm.html', {'disfirstzip':disfirstzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_second(request):    
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmsecond = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmsecond = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmsecond = BudgetedAP.objects.filter(Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    
    dissecondzip = zip(discomppmsecond,disapacompall)
    
    disaptpmbrsum = discomppmsecond.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmsecond.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmsecond.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmsecond.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmsecond.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmsecond.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compsecond.html', {'dissecondzip':dissecondzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_third(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmthird = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmthird = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmthird = BudgetedAP.objects.filter(month=3).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')

    disthirdzip = zip(discomppmthird,disapacompall)
    
    disaptpmbrsum = discomppmthird.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmthird.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmthird.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmthird.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmthird.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmthird.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compthird.html', {'disthirdzip':disthirdzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_fourth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmfourth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmfourth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmfourth = BudgetedAP.objects.filter(month=4).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    disfourthzip = zip(discomppmfourth,disapacompall)
    
    disaptpmbrsum = discomppmfourth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmfourth.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmfourth.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmfourth.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmfourth.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmfourth.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compfourth.html', {'disfourthzip':disfourthzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_fifth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmfifth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmfifth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmfifth = BudgetedAP.objects.filter(month=5).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    
    disfifthzip = zip(discomppmfifth,disapacompall)
    
    disaptpmbrsum = discomppmfifth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmfifth.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmfifth.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmfifth.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmfifth.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmfifth.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compfifth.html', {'disfifthzip':disfifthzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_sixth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmsixth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmsixth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmsixth = BudgetedAP.objects.filter(month=6).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    dissixthzip = zip(discomppmsixth,disapacompall)
    
    disaptpmbrsum = discomppmsixth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmsixth.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmsixth.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmsixth.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmsixth.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmsixth.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compsixth.html', {'dissixthzip':dissixthzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_seventh(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmseventh = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmseventh = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmseventh = BudgetedAP.objects.filter(month=7).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    disseventhzip = zip(discomppmseventh,disapacompall)
    
    disaptpmbrsum = discomppmseventh.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmseventh.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmseventh.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmseventh.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmseventh.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmseventh.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compseventh.html', {'disseventhzip':disseventhzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_eighth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmeighth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmeighth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmeighth = BudgetedAP.objects.filter(month=8).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    diseighthzip = zip(discomppmeighth,disapacompall)
    
    disaptpmbrsum = discomppmeighth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmeighth.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmeighth.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmeighth.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmeighth.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmeighth.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compeighth.html', {'diseighthzip':diseighthzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_nineth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmnineth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmnineth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmnineth = BudgetedAP.objects.filter(month=9).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    disninethzip = zip(discomppmnineth,disapacompall)
    
    disaptpmbrsum = discomppmnineth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmnineth.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmnineth.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmnineth.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmnineth.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmnineth.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
            
    return render(request, 'rasmApp/district_apaccomp_compnineth.html', {'disninethzip':disninethzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_tenth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmtenth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmtenth = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmtenth = BudgetedAP.objects.filter(month=10).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    distenthzip = zip(discomppmtenth,disapacompall)
    
    disaptpmbrsum = discomppmtenth.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmtenth.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmtenth.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmtenth.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmtenth.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmtenth.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
        
    return render(request, 'rasmApp/district_apaccomp_comptenth.html', {'distenthzip':distenthzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_elvm(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmelvm = BudgetedAP.objects.filter(month=11).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    diselvmzip = zip(discomppmelvm,disapacompall)
    
    disaptpmbrsum = discomppmelvm.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmelvm.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmelvm.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmelvm.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmelvm.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmelvm.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
    
    return render(request, 'rasmApp/district_apaccomp_compelvnth.html', {'diselvmzip':diselvmzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def district_compare_yr(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        discomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        discomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        discomppmyr = BudgetedAP.objects.filter(month=12).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')

    disyrzip = zip(discomppmyr,disapacompall)
    
    disaptpmbrsum = discomppmyr.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = discomppmyr.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = discomppmyr.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = discomppmyr.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = discomppmyr.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = discomppmyr.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
        
    return render(request, 'rasmApp/district_apaccomp_compyr.html', {'disyrzip':disyrzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum, 'searchfin':searchfin})

def ownf_district_comp_first(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmfirst = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=1)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmfirst = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=1)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmfirst = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=1)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    ownfdisfirstmzip = zip(ownfdiscomppmfirst,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmfirst.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmfirst.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmfirst.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmfirst.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmfirst.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmfirst.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_firstm.html', {'ownfdisfirstmzip':ownfdisfirstmzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_second(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmtwo = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmtwo = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmtwo = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=2)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
          
    ownfdistwomzip = zip(ownfdiscomppmtwo,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmtwo.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmtwo.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmtwo.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmtwo.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmtwo.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmtwo.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_twom.html', {'ownfdistwomzip':ownfdistwomzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_third(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmthree = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmthree = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmthree = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=3)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    ownfdisthreemzip = zip(ownfdiscomppmthree,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmthree.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmthree.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmthree.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmthree.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmthree.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmthree.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_threem.html', {'ownfdisthreemzip':ownfdisthreemzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_fourth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmfour = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmfour = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmfour = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=4)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    ownfdisfourmzip = zip(ownfdiscomppmfour,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmfour.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmfour.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmfour.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmfour.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmfour.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmfour.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_fourm.html', {'ownfdisfourmzip':ownfdisfourmzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_fifth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmfive = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmfive = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmfive = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=5)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    
    ownfdisfivemzip = zip(ownfdiscomppmfive,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmfive.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmfive.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmfive.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmfive.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmfive.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmfive.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_fivem.html', {'ownfdisfivemzip':ownfdisfivemzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_sixth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmsix = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmsix = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmsix = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=6)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    ownfdissixmzip = zip(ownfdiscomppmsix,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmsix.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmsix.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmsix.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmsix.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmsix.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmsix.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_sixm.html', {'ownfdissevenmzip':ownfdissixmzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_seventh(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmseven = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmseven = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmseven = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=7)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    ownfdissevenmzip = zip(ownfdiscomppmseven,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmseven.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmseven.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmseven.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmseven.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmseven.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmseven.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_sevenm.html', {'ownfdissevenmzip':ownfdissevenmzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_eighth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmeight = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmeight = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmeight = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=8)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    ownfdiseightmzip = zip(ownfdiscomppmeight,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmeight.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmeight.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmeight.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmeight.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmeight.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmeight.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_eightm.html', {'ownfdiseightmzip':ownfdiseightmzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_nineth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmnine = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmnine = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmnine = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=9)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'), acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    ownfdisninemzip = zip(ownfdiscomppmnine,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmnine.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmnine.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmnine.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmnine.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmnine.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmnine.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownf_dist_apacompcomp_ninem.html', {'ownfdisninemzip':ownfdisninemzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp_tenth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmten = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmten = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmten = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=10)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        
    ownfdistenmzip = zip(ownfdiscomppmten,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmten.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmten.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmten.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmten.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmten.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmten.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
        
    return render(request, 'rasmApp/ownf_dist_apacompcomp_tenm.html', {'ownfdistenmzip':ownfdistenmzip, 'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_comp(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    
    ownfdiselvmzip = zip(ownfdiscomppmelvm,disapacompall)
    
    ownfaptpmbrsum = ownfdiscomppmelvm.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscomppmelvm.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscomppmelvm.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscomppmelvm.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscomppmelvm.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscomppmelvm.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
        
    return render(request, 'rasmApp/ownforce_district_apacompcomp.html', {'ownfdiselvmzip':ownfdiselvmzip, 'disapacompall':disapacompall,  'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def ownf_district_compyr(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        ownfdiscompyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        ownfdiscompyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        ownfdiscompyr = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'),Q(month=12)).values('erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bcontractor','erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    ownfdisyrzip = zip(ownfdiscompyr,disapacompall)
    
    ownfaptpmbrsum = ownfdiscompyr.aggregate(ownfaptpmbrsum=Sum('aptotalpmonthbr'))['ownfaptpmbrsum']
    ownfacomptpmbrsum = ownfdiscompyr.aggregate(ownfacomptpmbrsum=Sum('acomptotalpmonthbr'))['ownfacomptpmbrsum']
    ownfaptpmkmsum = ownfdiscompyr.aggregate(ownfaptpmkmsum=Sum('aptotalpmonthkm'))['ownfaptpmkmsum']
    ownfacomptpmkmsum = ownfdiscompyr.aggregate(ownfacomptpmkmsum=Sum('acomptotalpmonthkm'))['ownfacomptpmkmsum']
    ownf_fincomptpmsum = ownfdiscompyr.aggregate(ownf_fincomptpmsum=Sum('fincomppmonth'))['ownf_fincomptpmsum']
    ownf_phycomptpmsum = ownfdiscompyr.aggregate(ownf_phycomptpmsum=Sum('phycomppmonth'))['ownf_phycomptpmsum']
    ownfaptbrsum = disapacompall.aggregate(ownfaptbrsum=Sum('aptotalbr'))['ownfaptbrsum']
    ownfacomptbrsum = disapacompall.aggregate(ownfacomptbrsum=Sum('acomptotalbr'))['ownfacomptbrsum']
    ownfaptkmsum = disapacompall.aggregate(ownfaptkmsum=Sum('aptotalkm'))['ownfaptkmsum']
    ownfacomptkmsum = disapacompall.aggregate(ownfacomptkmsum=Sum('acomptotalkm'))['ownfacomptkmsum']
    ownf_fincompsum = disapacompall.aggregate(ownf_fincompsum=Sum('fincomp'))['ownf_fincompsum']
    ownf_phycompsum = disapacompall.aggregate(ownf_phycompsum=Sum('phycomp'))['ownf_phycompsum']
    
    return render(request, 'rasmApp/ownforce_district_apacompcompyr.html', {'ownfdisyrzip':ownfdisyrzip, 'disapacompall':disapacompall,  'ownfaptbrsum':ownfaptbrsum, 'ownfacomptbrsum':ownfacomptbrsum, 'ownfaptkmsum':ownfaptkmsum, 'ownfacomptkmsum':ownfacomptkmsum, 'ownf_fincompsum':ownf_fincompsum, 'ownf_phycompsum':ownf_phycompsum, 'ownfaptpmbrsum':ownfaptpmbrsum, 'ownfacomptpmbrsum':ownfacomptpmbrsum, 'ownfaptpmkmsum':ownfaptpmkmsum, 'ownfacomptpmkmsum':ownfacomptpmkmsum, 'ownf_fincomptpmsum':ownf_fincomptpmsum, 'ownf_phycomptpmsum':ownf_phycomptpmsum, 'searchfin':searchfin})

def contractor_comp(request):    
    ownfalldata = ERABudget.objects.filter(Q(bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(bcontractor__icontains='የመንግስት ተቋራጭ')|Q(bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')).values('bcontractor').annotate(
        total_asphalt=Sum('basphalt'),
        total_gravel=Sum('bgravel'),
        tsum=Sum('basphalt') + Sum('bgravel'),
        group_count=Count('id')
    )
    ownfallasphsum = ownfalldata.aggregate(ownfallasphsum=Sum('total_asphalt'))['ownfallasphsum']
    ownfallgrvsum = ownfalldata.aggregate(ownfallgrvsum=Sum('total_gravel'))['ownfallgrvsum']
    ownfalltsum = ownfalldata.aggregate(ownfalltsum=Sum('tsum'))['ownfalltsum']
    
    return render(request, 'rasmApp/contractor_apacompcomp.html', {
        'ownfalldata':ownfalldata,
        'ownfallasphsum':ownfallasphsum,
        'ownfallgrvsum':ownfallgrvsum,
        'ownfalltsum':ownfalltsum,
        })

def contractor_apacompcomp_one(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmonem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=1)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bcontractor')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bcontractor')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmonem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=1)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bcontractor')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bcontractor')
    else:
        contractorcomppmonem = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=1)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bcontractor')
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bcontractor')
        
    contractoronemzip = zip(contractorcomppmonem,disapacompall)
    
    contraptpmbrsum = contractorcomppmonem.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmonem.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmonem.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmonem.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmonem.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmonem.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_one.html', {'contractoronemzip':contractoronemzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_two(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmtwom = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=2)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmtwom = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=2)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmtwom = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=2)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        
    contractortwomzip = zip(contractorcomppmtwom,disapacompall)
    
    contraptpmbrsum = contractorcomppmtwom.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmtwom.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmtwom.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmtwom.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmtwom.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmtwom.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_two.html', {'contractortwomzip':contractortwomzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_three(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmthreem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=3)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmthreem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=3)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmthreem = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=3)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        
    contractorthreemzip = zip(contractorcomppmthreem,disapacompall)
    
    contraptpmbrsum = contractorcomppmthreem.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmthreem.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmthreem.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmthreem.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmthreem.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmthreem.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_three.html', {'contractorthreemzip':contractorthreemzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_four(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmfourm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=4)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmfourm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=4)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmfourm = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=4)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
            
    contractorfourmzip = zip(contractorcomppmfourm,disapacompall)
    
    contraptpmbrsum = contractorcomppmfourm.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmfourm.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmfourm.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmfourm.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmfourm.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmfourm.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_four.html', {'contractorfourmzip':contractorfourmzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_five(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmfivem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=5)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmfivem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=5)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmfivem = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=5)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
            
    contractorfivemzip = zip(contractorcomppmfivem,disapacompall)
    
    contraptpmbrsum = contractorcomppmfivem.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmfivem.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmfivem.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmfivem.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmfivem.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmfivem.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_five.html', {'contractorfivemzip':contractorfivemzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_six(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmsixm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=6)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmsixm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=6)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmsixm = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=6)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        
    contractorsixmzip = zip(contractorcomppmsixm,disapacompall)
    
    contraptpmbrsum = contractorcomppmsixm.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmsixm.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmsixm.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmsixm.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmsixm.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmsixm.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_six.html', {'contractorsixmzip':contractorsixmzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_seven(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmsevenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=7)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmsevenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=7)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmsevenm = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=7)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    
    contractorsevenmzip = zip(contractorcomppmsevenm,disapacompall)
    
    contraptpmbrsum = contractorcomppmsevenm.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmsevenm.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmsevenm.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmsevenm.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmsevenm.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmsevenm.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_seven.html', {'contractorsevenmzip':contractorsevenmzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_eight(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmeightm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=8)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmeightm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=8)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmeightm = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=8)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        
    contractoreightmzip = zip(contractorcomppmeightm,disapacompall)
    
    contraptpmbrsum = contractorcomppmeightm.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmeightm.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmeightm.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmeightm.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmeightm.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmeightm.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_eight.html', {'contractoreightmzip':contractoreightmzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_nine(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmninem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=9)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmninem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=9)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmninem = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=9)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        
    contractorninemzip = zip(contractorcomppmninem,disapacompall)
    
    contraptpmbrsum = contractorcomppmninem.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmninem.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmninem.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmninem.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmninem.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmninem.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_nine.html', {'contractorninemzip':contractorninemzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_ten(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmtenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=10)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmtenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=10)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmtenm = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=10)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        
    contractortenmzip = zip(contractorcomppmtenm,disapacompall)
    
    contraptpmbrsum = contractorcomppmtenm.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmtenm.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmtenm.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmtenm.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmtenm.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmtenm.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_ten.html', {'contractortenmzip':contractortenmzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_eleven(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=11)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=11)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmelvm = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=11)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    
    contractorelvmzip = zip(contractorcomppmelvm,disapacompall)
    
    contraptpmbrsum = contractorcomppmelvm.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmelvm.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmelvm.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmelvm.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmelvm.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmelvm.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_eleven.html', {'contractorelvmzip':contractorelvmzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def contractor_apacompcomp_yr(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=12)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=12)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), (Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    else:
        contractorcomppmyr = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')),Q(month=12)).values('erabudget__bcontractor').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
        disapacompall = BudgetedAP.objects.filter((Q(erabudget__bcontractor__icontains='የራስ ሀይል ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ሥራ ተቋራጭ')|Q(erabudget__bcontractor__icontains='የመንግስት ተቋራጭ')|Q(erabudget__bcontractor__icontains='የግል ወይም የመንግስት ተቋራጭ (በግዢ ሂደት ላይ)')), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bcontractor').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/contractor_apacompcomp_yr.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})


def allbyproject_first(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=1)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=1)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=1).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectfirst.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_second(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=2)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=2)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=2).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectsecond.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_third(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=3)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=3)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=3).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectthird.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_fourth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=4)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=4)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=4).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectfourth.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_fifth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=5)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=5)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=5).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectfifth.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_sixth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=6)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=6)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=6).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectsixth.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_seventh(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=7)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=7)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=7).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectseventh.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_eighth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=8)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=8)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=8).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojecteighth.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_nineth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=9)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=9)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=9).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojectnineth.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_tenth(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=10)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=10)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=10).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojecttenth.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_eleventh(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=11)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=11)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=11).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyprojecteleventh.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})

def allbyproject_yr(request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'),Q(month=12)).values('erabudget__bdistrict__districtname','erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    elif searchfin == 'ካፒታል በጀት':
        contractorcomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'),Q(month=12)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
    else:
        contractorcomppmyr = BudgetedAP.objects.filter(month=12).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bdistrict__districtname', 'erabudget__bworktype__maintenancetype', 'erabudget__bcontractor', 'erabudget__bprojectname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bdistrict__id')
            
    contractoryrzip = zip(contractorcomppmyr,disapacompall)
    
    contraptpmbrsum = contractorcomppmyr.aggregate(contraptpmbrsum=Sum('aptotalpmonthbr'))['contraptpmbrsum']
    contracomptpmbrsum = contractorcomppmyr.aggregate(contracomptpmbrsum=Sum('acomptotalpmonthbr'))['contracomptpmbrsum']
    contraptpmkmsum = contractorcomppmyr.aggregate(contraptpmkmsum=Sum('aptotalpmonthkm'))['contraptpmkmsum']
    contracomptpmkmsum = contractorcomppmyr.aggregate(contracomptpmkmsum=Sum('acomptotalpmonthkm'))['contracomptpmkmsum']
    contr_fincomptpmsum = contractorcomppmyr.aggregate(contr_fincomptpmsum=Sum('fincomppmonth'))['contr_fincomptpmsum']
    contr_phycomptpmsum = contractorcomppmyr.aggregate(contr_phycomptpmsum=Sum('phycomppmonth'))['contr_phycomptpmsum']
    contraptbrsum = disapacompall.aggregate(contraptbrsum=Sum('aptotalbr'))['contraptbrsum']
    contracomptbrsum = disapacompall.aggregate(contracomptbrsum=Sum('acomptotalbr'))['contracomptbrsum']
    contraptkmsum = disapacompall.aggregate(contraptkmsum=Sum('aptotalkm'))['contraptkmsum']
    contracomptkmsum = disapacompall.aggregate(contracomptkmsum=Sum('acomptotalkm'))['contracomptkmsum']
    contr_fincompsum = disapacompall.aggregate(contr_fincompsum=Sum('fincomp'))['contr_fincompsum']
    contr_phycompsum = disapacompall.aggregate(contr_phycompsum=Sum('phycomp'))['contr_phycompsum']
        
    return render(request, 'rasmApp/allbyproject_yr.html', {'contractoryrzip':contractoryrzip, 'disapacompall':disapacompall,  'contraptbrsum':contraptbrsum, 'contracomptbrsum':contracomptbrsum, 'contraptkmsum':contraptkmsum, 'contracomptkmsum':contracomptkmsum, 'contr_fincompsum':contr_fincompsum, 'contr_phycompsum':contr_phycompsum, 'contraptpmbrsum':contraptpmbrsum, 'contracomptpmbrsum':contracomptpmbrsum, 'contraptpmkmsum':contraptpmkmsum, 'contracomptpmkmsum':contracomptpmkmsum, 'contr_fincomptpmsum':contr_fincomptpmsum, 'contr_phycomptpmsum':contr_phycomptpmsum, 'searchfin':searchfin})


def intervention_summary_firstm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmfirstm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmfirstm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmfirstm = BudgetedAP.objects.filter(month=1).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(month=1).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionfirstmzip = zip(interventioncomppmfirstm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmfirstm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmfirstm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmfirstm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmfirstm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmfirstm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmfirstm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_first.html', {'interventionfirstmzip':interventionfirstmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_secondm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmsecondm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=2)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmsecondm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=2)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmsecondm = BudgetedAP.objects.filter(month=2).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionsecondmzip = zip(interventioncomppmsecondm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmsecondm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmsecondm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmsecondm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmsecondm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmsecondm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmsecondm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_second.html', {'interventionsecondmzip':interventionsecondmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_thirdm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmthreem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=3)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype__maintenancetype').order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmthreem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=3)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype__maintenancetype').order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmthreem = BudgetedAP.objects.filter(month=3).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype__maintenancetype').order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionthreemzip = zip(interventioncomppmthreem,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmthreem.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmthreem.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmthreem.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmthreem.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmthreem.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmthreem.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_three.html', {'interventionthreemzip':interventionthreemzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_fourthm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmfourm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=4)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmfourm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=4)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmfourm = BudgetedAP.objects.filter(month=4).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionfourmzip = zip(interventioncomppmfourm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmfourm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmfourm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmfourm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmfourm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmfourm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmfourm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_four.html', {'interventionfourmzip':interventionfourmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_fifthm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmfivem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=5)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmfivem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=5)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmfivem = BudgetedAP.objects.filter(month=5).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionfivemzip = zip(interventioncomppmfivem,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmfivem.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmfivem.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmfivem.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmfivem.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmfivem.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmfivem.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_five.html', {'interventionfivemzip':interventionfivemzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_sixthm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmsixm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=6)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmsixm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=6)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmsixm = BudgetedAP.objects.filter(month=6).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionsixmzip = zip(interventioncomppmsixm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmsixm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmsixm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmsixm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmsixm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmsixm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmsixm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_six.html', {'interventionsixmzip':interventionsixmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_seventhm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmsevenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=7)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmsevenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=7)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmsevenm = BudgetedAP.objects.filter(month=7).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionsevenmzip = zip(interventioncomppmsevenm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmsevenm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmsevenm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmsevenm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmsevenm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmsevenm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmsevenm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_seven.html', {'interventionsevenmzip':interventionsevenmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_eighthm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmeightm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=8)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmeightm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=8)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmeightm = BudgetedAP.objects.filter(month=8).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventioneightmzip = zip(interventioncomppmeightm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmeightm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmeightm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmeightm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmeightm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmeightm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmeightm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_eight.html', {'interventioneightmzip':interventioneightmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_ninthm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmninem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=9)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmninem = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=9)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmninem = BudgetedAP.objects.filter(month=9).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionninemzip = zip(interventioncomppmninem,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmninem.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmninem.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmninem.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmninem.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmninem.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmninem.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_nine.html', {'interventionninemzip':interventionninemzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_tenthm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmtenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=10)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmtenm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=10)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmtenm = BudgetedAP.objects.filter(month=10).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        
    interventiontenmzip = zip(interventioncomppmtenm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmtenm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmtenm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmtenm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmtenm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmtenm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmtenm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_ten.html', {'interventiontenmzip':interventiontenmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_eleventhm (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=11)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmelvm = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=11)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmelvm = BudgetedAP.objects.filter(month=11).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionelvmzip = zip(interventioncomppmelvm,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmelvm.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmelvm.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmelvm.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmelvm.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmelvm.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmelvm.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_eleven.html', {'interventionelvmzip':interventionelvmzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def intervention_summary_yr (request):
    searchfin = request.GET.get('fin')
    if searchfin == 'መንገድ ፈንድ':   
        interventioncomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=12)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='መንገድ ፈንድ'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'),acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    elif searchfin == 'ካፒታል በጀት':
        interventioncomppmyr = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=12)).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(erabudget__bfinancer__financerName='ካፒታል በጀት'), Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'),acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
    else:
        interventioncomppmyr = BudgetedAP.objects.filter(month=12).values('erabudget__bworktype__maintenancetype').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
        disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bworktype__maintenancetype').annotate(aptotalbr=Sum('bapinBr'),acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('erabudget__bworktype_id')
            
    interventionyrzip = zip(interventioncomppmyr,disapacompall)
    
    intervenaptpmbrsum = interventioncomppmyr.aggregate(intervenaptpmbrsum=Sum('aptotalpmonthbr'))['intervenaptpmbrsum']
    intervenacomptpmbrsum = interventioncomppmyr.aggregate(intervenacomptpmbrsum=Sum('acomptotalpmonthbr'))['intervenacomptpmbrsum']
    intervenaptpmkmsum = interventioncomppmyr.aggregate(intervenaptpmkmsum=Sum('aptotalpmonthkm'))['intervenaptpmkmsum']
    intervenacomptpmkmsum = interventioncomppmyr.aggregate(intervenacomptpmkmsum=Sum('acomptotalpmonthkm'))['intervenacomptpmkmsum']
    interven_fincomptpmsum = interventioncomppmyr.aggregate(interven_fincomptpmsum=Sum('fincomppmonth'))['interven_fincomptpmsum']
    interven_phycomptpmsum = interventioncomppmyr.aggregate(interven_phycomptpmsum=Sum('phycomppmonth'))['interven_phycomptpmsum']
    intervenaptbrsum = disapacompall.aggregate(intervenaptbrsum=Sum('aptotalbr'))['intervenaptbrsum']
    intervenacomptbrsum = disapacompall.aggregate(intervenacomptbrsum=Sum('acomptotalbr'))['intervenacomptbrsum']
    intervenaptkmsum = disapacompall.aggregate(intervenaptkmsum=Sum('aptotalkm'))['intervenaptkmsum']
    intervenacomptkmsum = disapacompall.aggregate(intervenacomptkmsum=Sum('acomptotalkm'))['intervenacomptkmsum']
    interven_fincompsum = disapacompall.aggregate(interven_fincompsum=Sum('fincomp'))['interven_fincompsum']
    interven_phycompsum = disapacompall.aggregate(interven_phycompsum=Sum('phycomp'))['interven_phycompsum']
        
    return render(request, 'rasmApp/intervention_apacompcomp_yr.html', {'interventionyrzip':interventionyrzip, 'disapacompall':disapacompall,  'intervenaptbrsum':intervenaptbrsum, 'intervenacomptbrsum':intervenacomptbrsum, 'intervenaptkmsum':intervenaptkmsum, 'intervenacomptkmsum':intervenacomptkmsum, 'interven_fincompsum':interven_fincompsum, 'interven_phycompsum':interven_phycompsum, 'intervenaptpmbrsum':intervenaptpmbrsum, 'intervenacomptpmbrsum':intervenacomptpmbrsum, 'intervenaptpmkmsum':intervenaptpmkmsum, 'intervenacomptpmkmsum':intervenacomptpmkmsum, 'interven_fincomptpmsum':interven_fincomptpmsum, 'interven_phycomptpmsum':interven_phycomptpmsum, 'searchfin':searchfin})

def apaccomp_compare(request):
    acompcomp = Accomplishment.objects.filter(bapmonth__icontains='ግንቦት').values('erabudget__bdistrict__districtname').annotate(tap_len_m = Sum('budgetedap__bapinKm'), tacomp_len_m = Sum('actionInKm'), complen=(F('actionInKm')/F('budgetedap__bapinKm'))*100, phycompkm=(Sum('actionInKm')/Sum('budgetedap__bapinKm'))*100).order_by('erabudget__bdistrict')[:100]
    
    apaccompall = BudgetedAP.objects.all()
    apacompall = apaccompall.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname').annotate(totapkm=Sum('bapinKm'), totacomkm=Sum('accomplishment__actionInKm'),fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100).order_by('id')[:300]

    ziplast = zip(acompcomp,apacompall)
    #l = dict(BudgetedAP.objects.order_by('erabudget__bdistrict__districtname').values('erabudget__bdistrict__districtname','month').annotate(totapkm=Sum('bapinKm'))) #(ERABudget.objects.all().values('bdistrict__districtname','budgetedap__month'))
    #l = l[1]
    
    d = apaccompall.values('erabudget__bdistrict__districtname','month').annotate(totapbr=Sum('bapinBr'),totapkm=Sum('bapinKm'),mcount = Count('month'))
    #d = d.filter(month=1)
    #dpv = pivot(d, 'erabudget__bdistrict__districtname', 'month', 'totapkm', include_total=True)
    
    df = pd.DataFrame(d)
    dpv = df.pivot_table(index='erabudget__bdistrict__districtname', columns='month', values=['totapbr','totapkm'], aggfunc='sum')
    dpv.to_excel('MyPD22.xlsx','Pivot_Data',startrow=2)
    dpv = dpv.reset_index()
    h = dpv.to_html('rasmApp/sample2.html')
    
    #print(h)
    #return render(request,'rasmApp/annualbudget.html', {'pt':pt})
    
    ID = [1,2]
    name = ['Jim','Jane']
    age = [35,25]
    employees=zip(ID, name, age)
    
    employees2 = [
        {'ID':1,'name':'Jim','age':35},
        {'ID':2,'name':'Jane','age':25},
    ]
    
    return render(request, 'rasmApp/apaccompcompare.html', {'acompcomp':acompcomp,'apacompall':apacompall,'ziplast':ziplast, 'acompcomp':acompcomp, 'employees':employees, 'employees2':employees2, 'd':d, 'dpv':dpv, 'h':h})

def apaccomp_per_district(request):    
    return render(request, 'rasmApp/sample.html')

def rambranch_summary(request):
    branchsummary = ERABudget.objects.all().values('bdistrict__districtname').annotate(total_asphalt=Sum('basphalt'),total_gravel=Sum('bgravel'),total_sum=Sum('basphalt')+Sum('bgravel')).order_by('bdistrict')
    
    tasphalt_sum = branchsummary.aggregate(tasphalt_sum=Sum('total_asphalt'))['tasphalt_sum']
    tgravel_sum = branchsummary.aggregate(tgravel_sum=Sum('total_gravel'))['tgravel_sum']
    tsum = branchsummary.aggregate(tsum=Sum('total_sum'))['tsum']
    
    return render(request, 'rasmApp/branch_summary.html', {'branchsummary':branchsummary, 'tasphalt_sum':tasphalt_sum, 'tgravel_sum':tgravel_sum, 'tsum':tsum})

def ownfbranch_summary(request):
    ownfbranchsummary = ERABudget.objects.filter(bcontractor__icontains='የራስ ሀይል ተቋራጭ').values('bdistrict__districtname', 'bcontractor').annotate(total_asphalt=Sum('basphalt'),total_gravel=Sum('bgravel'),total_sum=Sum('basphalt')+Sum('bgravel')).order_by('bdistrict')
    
    tasphalt_sum = ownfbranchsummary.aggregate(tasphalt_sum=Sum('total_asphalt'))['tasphalt_sum']
    tgravel_sum = ownfbranchsummary.aggregate(tgravel_sum=Sum('total_gravel'))['tgravel_sum']
    tsum = ownfbranchsummary.aggregate(tsum=Sum('total_sum'))['tsum']
    
    return render(request, 'rasmApp/ownfbranch_summary.html', {'ownfbranchsummary':ownfbranchsummary, 'tasphalt_sum':tasphalt_sum, 'tgravel_sum':tgravel_sum, 'tsum':tsum})

def intervention_summary(request):
    interventionsummary = BudgetedAP.objects.exclude(Q(erabudget__bworktype__maintenancetype='የካሳ ክፍያ')| Q(erabudget__bworktype__maintenancetype='ኤርጎኖሚክስ')| Q(erabudget__bworktype__maintenancetype='የመንገድ ደህንነት ስራ')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ ስራዎች')| Q(erabudget__bworktype__maintenancetype='የማማከር አገልግሎት')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ የማዘመን ስራዎች')| Q(erabudget__bworktype__maintenancetype='ድልድይ መልሶ ግንባታ')| Q(erabudget__bworktype__maintenancetype='ድልድይ/ፉካ ጥገና ስራ')).values('erabudget__bworktype__maintenancetype').annotate(total_asphalt=Sum('erabudget__basphalt')/12,total_gravel=Sum('erabudget__bgravel')/12,total_sum=Sum('erabudget__basphalt')/12 + Sum('erabudget__bgravel')/12)
    
    tasphalt_sum = interventionsummary.aggregate(tasphalt_sum=Sum('total_asphalt'))['tasphalt_sum']
    tgravel_sum = interventionsummary.aggregate(tgravel_sum=Sum('total_gravel'))['tgravel_sum']
    tsum = interventionsummary.aggregate(tsum=Sum('total_sum'))['tsum']
    
    return render(request, 'rasmApp/intervention_summary.html', {'interventionsummary':interventionsummary, 'tasphalt_sum':tasphalt_sum, 'tgravel_sum':tgravel_sum, 'tsum':tsum})

def all_by_project_summary(request):
    allbyprojsummary = BudgetedAP.objects.exclude(Q(erabudget__bworktype__maintenancetype='የካሳ ክፍያ')| Q(erabudget__bworktype__maintenancetype='ኤርጎኖሚክስ')| Q(erabudget__bworktype__maintenancetype='የመንገድ ደህንነት ስራ')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ ስራዎች')| Q(erabudget__bworktype__maintenancetype='የማማከር አገልግሎት')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ የማዘመን ስራዎች')| Q(erabudget__bworktype__maintenancetype='ድልድይ መልሶ ግንባታ')| Q(erabudget__bworktype__maintenancetype='ድልድይ/ፉካ ጥገና ስራ')).values('erabudget__bworktype__maintenancetype','erabudget__bprojectname').annotate(total_asphalt=Sum('erabudget__basphalt')/12,total_gravel=Sum('erabudget__bgravel')/12,total_sum=Sum('erabudget__basphalt')/12 + Sum('erabudget__bgravel')/12)
    
    tasphalt_sum = allbyprojsummary.aggregate(tasphalt_sum=Sum('total_asphalt'))['tasphalt_sum']
    tgravel_sum = allbyprojsummary.aggregate(tgravel_sum=Sum('total_gravel'))['tgravel_sum']
    tsum = allbyprojsummary.aggregate(tsum=Sum('total_sum'))['tsum']
    
    return render(request, 'rasmApp/all_byprojsummary.html', {'allbyprojsummary':allbyprojsummary, 'tasphalt_sum':tasphalt_sum, 'tgravel_sum':tgravel_sum, 'tsum':tsum})

def exportxl(request):
    erabudget_resource = ERABudgetResource()
    dataset = erabudget_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="budget.csv"'
    return response

def bexport(request):
    budgetexp = ERABudget.objects.all()
    data2 = budgetexp.values()
    data2 = pd.DataFrame(data2)
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=budgets.xlsx'

    def style_specific_cell(x):
        color = 'background-color: yellow'
        return [color if x.name == 'bprojectname' else '' for _ in x]

    data2.style.apply(style_specific_cell, axis=1).to_excel(response, index=False, engine='openpyxl')

    return response
    
def intervention_summary_export(request):
    interventionsummary = BudgetedAP.objects.exclude(Q(erabudget__bworktype__maintenancetype='የካሳ ክፍያ')| Q(erabudget__bworktype__maintenancetype='ኤርጎኖሚክስ')| Q(erabudget__bworktype__maintenancetype='የመንገድ ደህንነት ስራ')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ ስራዎች')| Q(erabudget__bworktype__maintenancetype='የማማከር አገልግሎት')| Q(erabudget__bworktype__maintenancetype='የሚዛን ጣቢያ የማዘመን ስራዎች')| Q(erabudget__bworktype__maintenancetype='ድልድይ መልሶ ግንባታ')| Q(erabudget__bworktype__maintenancetype='ድልድይ/ፉካ ጥገና ስራ')).values('erabudget__bworktype__maintenancetype').annotate(total_asphalt=Sum('erabudget__basphalt')/12,total_gravel=Sum('erabudget__bgravel')/12,total_sum=Sum('erabudget__basphalt')/12 + Sum('erabudget__bgravel')/12)
    
    tasphalt_sum = interventionsummary.aggregate(tasphalt_sum=Sum('total_asphalt'))['tasphalt_sum']
    tgravel_sum = interventionsummary.aggregate(tgravel_sum=Sum('total_gravel'))['tgravel_sum']
    tsum = interventionsummary.aggregate(tsum=Sum('total_sum'))['tsum']

    data2 = pd.DataFrame(interventionsummary)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=intervention_summary.xlsx'

    def style_specific_cell(x):
        color = 'background-color: yellow'
        return [color if x.name == 'bprojectname' else '' for _ in x]

    data2.style.apply(style_specific_cell, axis=1).to_excel(response, index=False, engine='openpyxl')


    return response

@login_required(login_url='login')    
def apaccompcomparison(request):
    return render(request, 'rasmApp/apwithaccomp_comparison.html')

@login_required(login_url='login')
def disapaccompcomparison(request):
    return render(request, 'rasmApp/disapwithaccomp_comparison.html')

@login_required(login_url='login')
def ownfdisapaccompcomparison(request):
    return render(request, 'rasmApp/owndisapwithaccomp_comparison.html')

@login_required(login_url='login')
def contractor_comparison(request):
    return render(request, 'rasmApp/contractor_apacmop_comparison.html')

@login_required(login_url='login')
def intervention_comparison(request):
    return render(request, 'rasmApp/intervention_apacmop_comparison.html')


# Added Views

@login_required(login_url='login')
def quarterly_branchoffice(request):
    return render(request, 'rasmApp/quarterly_branchoffice.html')

@login_required(login_url='login')
def quarterly_byfinance(request):
    return render(request, 'rasmApp/quarterly_byfinance.html')

@login_required(login_url='login')
def quarterly_byproject(request):
    return render(request, 'rasmApp/quarterly_byproject.html')

@login_required(login_url='login')
def quarterly_contractor(request):
    return render(request, 'rasmApp/quarterly_contractor.html')

@login_required(login_url='login')
def quarterly_intervention(request):
    return render(request, 'rasmApp/quarterly_intervention.html')

@login_required(login_url='login')
def quarterly_ownbranch(request):
    return render(request, 'rasmApp/quarterly_ownbranch.html')

@login_required(login_url='login')
def annual_branchoffice(request):
    return render(request, 'rasmApp/annual_branchoffice.html')

@login_required(login_url='login')
def annual_byfinancer(request):
    return render(request, 'rasmApp/annual_byfinancer.html')


@login_required(login_url='login')
def annual_byproject(request):
    return render(request, 'rasmApp/annual_byproject.html')

@login_required(login_url='login')
def annual_contractor(request):
    return render(request, 'rasmApp/annual_contractor.html')

@login_required(login_url='login')
def annual_intervention(request):
    return render(request, 'rasmApp/annual_intervention.html')

@login_required(login_url='login')
def annual_ownforce(request):
    return render(request, 'rasmApp/annual_ownforce.html')

def about(request):
    return render(request, 'rasmApp/about.html')

# Ends here

def branchchart(request):
    return render(request, 'rasmApp/branchchart.html')

def roadl_branch_chart(request):
    labels = []
    data = []
    data2 = []

    queryset = ERABudget.objects.values('bdistrict__districtname').annotate(total_asphalt=Sum('basphalt'), total_gravel=Sum('bgravel')).order_by('bdistrict')
    
    for entry in queryset:
        labels.append(entry['bdistrict__districtname'])
        data.append(entry['total_asphalt'])
        data2.append(entry['total_gravel'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data2': data2,
    })

def apacompchartelvm(request):
    return render(request, 'rasmApp/apacompchart_elvm.html')

def apacomp_elvm_chart(request):
    labels = []
    data = []
    data2 = []

    queryset = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)).values('erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'))

    
    for entry in queryset:
        labels.append(entry['erabudget__bdistrict__districtname'])
        data.append(entry['aptotalbr'])
        data2.append(entry['acomptotalbr'])
    
    return JsonResponse(data={
        'labels': labels,
        'data': data,
        'data2': data2,
    })

def financer_compare_yr(request):    
    compbyfinyr = BudgetedAP.objects.filter(month=12).values('erabudget__bfinancer__financerName', 'erabudget__bdistrict__districtname').annotate(aptotalpmonthbr = Sum('bapinBr'), acomptotalpmonthbr = Sum('accomplishment__actionInBr'), aptotalpmonthkm = Sum('bapinKm'), acomptotalpmonthkm = Sum('accomplishment__actionInKm'), fincomppmonth=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomppmonth=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)
    
    disapacompall = BudgetedAP.objects.filter(Q(month=1)|Q(month=2)|Q(month=3)|Q(month=4)|Q(month=5)|Q(month=6)|Q(month=7)|Q(month=8)|Q(month=9)|Q(month=10)|Q(month=11)|Q(month=12)).values('erabudget__bfinancer__financerName', 'erabudget__bdistrict__districtname').annotate(aptotalbr=Sum('bapinBr'), acomptotalbr=Sum('accomplishment__actionInBr'), aptotalkm=Sum('bapinKm'),acomptotalkm=Sum('accomplishment__actionInKm'), fincomp=(Sum('accomplishment__actionInBr')/Sum('bapinBr'))*100, phycomp=(Sum('accomplishment__actionInKm')/Sum('bapinKm'))*100)

    financeryrzip = zip(compbyfinyr,disapacompall)
    
    disaptpmbrsum = compbyfinyr.aggregate(disaptpmbrsum=Sum('aptotalpmonthbr'))['disaptpmbrsum']
    disacomptpmbrsum = compbyfinyr.aggregate(disacomptpmbrsum=Sum('acomptotalpmonthbr'))['disacomptpmbrsum']
    disaptpmkmsum = compbyfinyr.aggregate(disaptpmkmsum=Sum('aptotalpmonthkm'))['disaptpmkmsum']
    disacomptpmkmsum = compbyfinyr.aggregate(disacomptpmkmsum=Sum('acomptotalpmonthkm'))['disacomptpmkmsum']
    disfincomptpmsum = compbyfinyr.aggregate(disfincomptpmsum=Sum('fincomppmonth'))['disfincomptpmsum']
    disphycomptpmsum = compbyfinyr.aggregate(disphycomptpmsum=Sum('phycomppmonth'))['disphycomptpmsum']
    disaptbrsum = disapacompall.aggregate(disaptbrsum=Sum('aptotalbr'))['disaptbrsum']
    disacomptbrsum = disapacompall.aggregate(disacomptbrsum=Sum('acomptotalbr'))['disacomptbrsum']
    disaptkmsum = disapacompall.aggregate(disaptkmsum=Sum('aptotalkm'))['disaptkmsum']
    disacomptkmsum = disapacompall.aggregate(disacomptkmsum=Sum('acomptotalkm'))['disacomptkmsum']
    disfincompsum = disapacompall.aggregate(disfincompsum=Sum('fincomp'))['disfincompsum']
    disphycompsum = disapacompall.aggregate(disphycompsum=Sum('phycomp'))['disphycompsum']
        
    return render(request, 'rasmApp/financer_apaccomp_compyr.html', {'financeryrzip':financeryrzip, 'disaptpmbrsum':disaptpmbrsum, 'disacomptpmbrsum':disacomptpmbrsum, 'disaptpmkmsum':disaptpmkmsum, 'disacomptpmkmsum':disacomptpmkmsum, 'disfincomptpmsum':disfincomptpmsum, 'disphycomptpmsum':disphycomptpmsum, 'disaptbrsum':disaptbrsum, 'disacomptbrsum':disacomptbrsum, 'disaptkmsum':disaptkmsum, 'disacomptkmsum':disacomptkmsum, 'disfincompsum':disfincompsum, 'disphycompsum':disphycompsum})




def road_segment_list(request):
    context = {}
    numbers = range(0, 12)  # Create a range from 0 to 11 (excluding 12)
    roadsegments = RoadSegment.objects.all()
    roadsegext = RoadSegmentExt.objects.all()
        
    context={'roadsegments':roadsegments, 'roadsegext':roadsegext, 'numbers': numbers}
    return render(request, 'rasmApp/road_segments.html', context)


def road_segment_detail(request, pk):
    roadsegments = RoadSegment.objects.get(id=pk)
    RoadSegmentExtFormSet = inlineformset_factory(RoadSegment, RoadSegmentExt, fields=('inspector','fromlen','tolen', 'roadsegment'),extra=3)
    formset = RoadSegmentExtFormSet(queryset=RoadSegmentExt.objects.all(), instance=roadsegments)    
            
    if request.method == 'POST':
        formset = RoadSegmentExtFormSet(request.POST, instance=roadsegments)
        if formset.is_valid():
            formset.save()
    
    context = {'formset':formset,'roadsegments':roadsegments}
    return render(request, 'rasmApp/roadsegmentdetail.html', context)

def road_segment_ext(request):
    context = {}
    #roadsegments = RoadSegment.objects.get(id=pk)
    roadsegmentext = RoadSegmentExt.objects.all()
    
    context = {'roadsegmentext':roadsegmentext}

    return render(request, 'rasmApp/road_segment_exts.html', context)



def roadsegext(request):
    roadseg = RoadSegmentExt.objects.all()
    return render(request, 'rasmApp/roadsegext.html', {'roadseg':roadseg})


def create_condition_survey(request, pk):
    RoadConditionSurveyFormSet = inlineformset_factory(RoadSegmentExt, RoadConditionSurvey, fields=('roadsegext','problem','severity', 'extent', 'activity', 'qty'))
    roadc = RoadSegmentExt.objects.get(id=pk)

    formset = RoadConditionSurveyFormSet(queryset=RoadConditionSurvey.objects.all(), instance=roadc)    
            
    if request.method == 'POST':
        formset = RoadConditionSurveyFormSet(request.POST, instance=roadc)
        if formset.is_valid():
            formset.save()
    context = {'formset':formset,'roadc':roadc}

    return render(request, 'rasmApp/condition_survey_form.html', context)



#def create_condition_survey(request):
#    context = {}
#    return render(request, 'rasmApp/roadconditionsurvey.html', context)


def coditionlst(request):
    roadseg = RoadSegment.objects.all()
    conditionserveyl = RoadConditionSurvey.objects.all()
    
    return render(request, 'rasmApp/road_condition_survey_list.html', {'roadseg': roadseg, 'conditionserveyl':conditionserveyl})

def boq(request, pk):
    rid = pk #request.GET.get('d')
    condsummary = RoadConditionSurvey.objects.exclude(activity=None).values('roadsegext__roadsegment__district__districtname', 'roadsegext__roadsegment_id', 'roadsegext__roadsegment__roadname', 'activity__activitycode', 'activity__activity', 'activity__unit', 'activity__urate').annotate(qty_total=Sum('qty'), amt_total=F('qty_total')*F('activity__urate'))

    condsummary = condsummary.filter(roadsegext__roadsegment_id = rid)
    rs = RoadSegment.objects.get(id = rid)
    context = {'condsummary': condsummary, 'rid':rid, 'rs':rs}
    
    return render(request, 'rasmApp/bill_of_qty.html', context)

def condition_summary(request):
    roadseg = RoadSegmentExt.objects.all()
    condsummary = RoadConditionSurvey.objects.exclude(activity=None).values('roadsegext__roadsegment__district__districtname', 'roadsegext__roadsegment__sectionname__sectionname', 'roadsegext__roadsegment__roadname', 'activity__activitycode', 'activity__activity', 'activity__unit', 'activity__urate').annotate(qty_total=Sum('qty'), amt_total=F('qty_total')*F('activity__urate'))

    context = {'roadseg':roadseg, 'condsummary': condsummary}
    
    return render(request, 'rasmApp/roadconditionsummary.html', context)

def road_condition_detail(request, pk):
    roadsegext = RoadSegmentExt.objects.get(id=pk)
    roadcond = roadsegext.roadconditionsurvey_set.all()

    context = {'roadsegext':roadsegext, 'roadcond':roadcond}

    return render(request, 'rasmApp/road_condition_detail.html', context)






def create_conditionsurvey(request):
    context = {}
    return render(request, 'rasmApp/roadconditionsurvey.html', context)#{'form': form})
