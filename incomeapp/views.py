from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json, datetime
from .models import UserIncome
from django.http import JsonResponse



def search_income(request):
    if request.method== 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
            amount__istartswith=search_str, owner= request.user) | UserIncome.objects.filter(
            date__istartswith=search_str, owner = request.user) | UserIncome.objects.filter(
            description__icontains=search_str, owner = request.user) | UserIncome.objects.filter(
            source__icontains=search_str, owner = request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)


@login_required(login_url='/authentication/login/')
def index(request):
    sources = Source.objects.all()
    income = UserIncome.objects.filter(owner=request.user)
    paginator = Paginator(income, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page( page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'incomeapp': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'incomeapp/index.html', context)

@login_required
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST
    }
    if request.method == 'GET':

        return render(request, 'incomeapp/add_income.html', context)

    if request.method =='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        date=request.POST['income_date']
        source=request.POST['source']


        if not amount:
            messages.error(request, 'Amount is required.')
            return render(request, 'incomeapp/add_income.html', context)

        if not description:
            messages.error(request, 'description is required.')
            return render(request, 'incomeapp/add_income.html', context)

        if not date:
            messages.error(request, 'Date is required.')
            return render(request, 'incomeapp/add_income.html', context)

        UserIncome.objects.create(amount=amount, date=date,owner=request.user,
                               source=source, description=description)

        messages.success(request, 'incomeapp saved successfully.')
        return redirect('income')

@login_required
def add_income_source(request):
    if request.method == 'GET':
        return render(request, 'incomeapp/add_income_source.html')

    if request.method == 'POST':
        newsource = request.POST['source'].upper()

        if not Source.objects.filter(name=newsource).exists():
            Source.objects.create(name=newsource)
            messages.success(request, 'New source ' + str(newsource) + ' added.')
        else:
            messages.warning(request, 'Source ' + str(newsource) + ' already exists.')

        return redirect('add-income-source')

@login_required
def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    categories = Source.objects.all()


    context = {
        'incomeapp': income,
        'values': income,
        'categories': categories
    }
    if request.method =='GET':
        return render(request, 'incomeapp/edit_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['income_date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required.')
            return render(request, 'incomeapp/edit_income.html', context)

        if not description:
            messages.error(request, 'description is required.')
            return render(request, 'incomeapp/edit_income.html', context)

        if not date:
            messages.error(request, 'Date is required.')
            return render(request, 'incomeapp/edit_income.html', context)

        income.owner = request.user
        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.save()

        messages.success(request, 'Incomes Updated Successfully')
        return redirect('income')


def delete_income(request, id):
    income= UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Record Removed.')
    return redirect('income')

def income_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days = 30*6)
    income = UserIncome.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_source(income):
        return income.source

    source_list = list(set(map(get_source, income)))

    def get_income_source_amount(source):
        amount=0
        filtered_by_source = income.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount

    for x in income:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)

    return JsonResponse({'income_category_data': finalrep}, safe = False)

def income_stats_view(request):
    return  render(request, 'incomeapp/income-stats.html')


