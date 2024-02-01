from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('expenses/', views.index, name="expenses"),
    path('add-expense/', views.add_expense, name="add-expenses"),
    path('add-expense-category/', views.add_expense_category, name="add-expenses-category"),
    path('edit-expense/<int:id>', views.expense_edit, name="edit-expenses"),
    path('delete-expense/<int:id>', views.delete_expense, name="delete-expense"),
    path('search-expenses/', csrf_exempt(views.search_expenses), name="search-expense"),
    path('expense_category_summary', views.expense_category_summary,
         name="expense_category_summary"),
    path('expense-stats/', views.expense_stats_view, name="expense-stats"),
    path('export_csv', views.export_csv, name="export-csv"),
    path('export_excel', views.export_excel, name="export-excel"),
    path('export_pdf', views.export_pdf, name="export-pdf")
]