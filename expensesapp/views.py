from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from userpreferences.models import UserPreference
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
import json, datetime, csv, xlwt

from django.template.loader import render_to_string
# from weasyprint import HTML
import tempfile, os
from django.db.models import Sum





def search_expenses(request):
    if request.method== 'POST':
        search_str = json.loads(request.body).get('searchText')

        expenses=Expense.objects.filter(
            amount__istartswith=search_str, owner= request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner = request.user) | Expense.objects.filter(
            description__istartswith=search_str, owner = request.user) | Expense.objects.filter(
            category__istartswith=search_str, owner = request.user)
        data = expenses.values()
        return JsonResponse(list(data), safe=False)





@login_required(login_url='/authentication/login/')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page( page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except ObjectDoesNotExist:
        currency = 'Select a Currency'
        UserPreference.objects.create(user=request.user, currency=currency)
    # if UserPreference.objects.get(user=request.user).currency.DoesNotExist:
    #     currency = 'USD'
    #     UserPreference.objects.create(user=request.user, currency=currency)
    # else:
    #     currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expensesapp/index.html', context)

@login_required
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':

        return render(request, 'expensesapp/add_expense.html', context)

    if request.method =='POST':
        amount=request.POST['amount']
        description=request.POST['description']
        date=request.POST['expense_date']
        category=request.POST['category']


        if not amount:
            messages.error(request, 'Amount is required.')
            return render(request, 'expensesapp/add_expense.html', context)

        if not description:
            messages.error(request, 'description is required.')
            return render(request, 'expensesapp/add_expense.html', context)

        if not date:
            messages.error(request, 'Date is required.')
            return render(request, 'expensesapp/add_expense.html', context)

        Expense.objects.create(amount=amount, date=date,owner=request.user,
                               category=category, description=description)

        messages.success(request, 'Expense saved successfully.')
        return redirect('expenses')

@login_required
def add_expense_category(request):
    if request.method == 'GET':
        return render(request, 'expensesapp/add_expense_category.html')

    if request.method =='POST':
        newcategory = request.POST['category'].upper()

        if not Category.objects.filter(name=newcategory).exists():
            Category.objects.create(name=newcategory)
            messages.success(request, 'New category '+ str(newcategory) +' added.')
        else:
            messages.warning(request, 'Category '+ str(newcategory) +' already exists.')

        return redirect('add-expenses-category')

@login_required
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()


    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method =='GET':
        return render(request,'expensesapp/edit_expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required.')
            return render(request, 'expensesapp/edit_expense.html', context)

        if not description:
            messages.error(request, 'description is required.')
            return render(request, 'expensesapp/edit_expense.html', context)

        if not date:
            messages.error(request, 'Date is required.')
            return render(request, 'expensesapp/edit_expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.save()

        messages.success(request, 'Expenses Updated Successfully')
        return redirect('expenses')


def delete_expense(request, id):
    expense= Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense Removed.')
    return redirect('expenses')


def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days = 30*6)
    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    finalrep = {}

    def get_category(expense):
        return expense.category

    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount=0
        filtered_by_category = expenses.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount

    for x in expenses:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)

    return JsonResponse({'expense_category_data': finalrep}, safe = False)

def expense_stats_view(request):
    return  render(request, 'expensesapp/expense-stats.html')


def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename=Expenses - '+ str(datetime.datetime.now())+'.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Description', 'Category', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.description, expense.category, expense.date])

    return response

def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Expenses - '+ str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Expenses')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Amount', 'Description', 'Category', 'Date']
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    rows = Expense.objects.filter(owner = request.user).values_list('amount', 'description', 'category', 'date')
    for row in rows:
        row_num+=1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def export_pdf(request):


    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; attachment; filename=Expenses'+ str(datetime.datetime.now())+'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    expenses = Expense.objects.filter(owner=request.user)
    sum=expenses.aggregate(Sum('amount'))
    html_string = render_to_string('expensesapp/pdf-output.html', {'expenses': expenses, 'total': sum['amount__sum']})
    # html = HTML(string=html_string)
    result = html.write_pdf()
    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output.seek(0)
        response.write(output.read())

    return response
