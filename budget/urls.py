from django.urls import  path
from .views import IndexView, BudgetCreateView, BudgetUpdateView, BudgetDeleteView, PDFDowloadView, PricesListView, PricesUpdateView, PricesDeleteView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("budget/add/", BudgetCreateView.as_view(), name="add_budget"),
    path("budget/update/<int:pk>/", BudgetUpdateView.as_view(), name="update_budget"),
    path("budget/delete/<int:pk>/", BudgetDeleteView.as_view(), name="delete_budget"),
    path("budget/dowload/<int:pk>/", PDFDowloadView.as_view(), name="dowload_budget"),
    path("budget/prices/", PricesListView.as_view(), name="prices_list"),
    path("budget/prices/update/<int:pk>/", PricesUpdateView.as_view(), name="update_price"),
    path("budget/prices/delete/<int:pk>/", PricesDeleteView.as_view(), name="delete_price"),


]
