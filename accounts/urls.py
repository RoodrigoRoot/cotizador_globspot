from django.urls import path
from .views import LoginView, logout_view, CompanyListView, CompanyCreateView, CompanyDeleteView, CompanyUpdateView, get_company_contact

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("salir/", logout_view, name="logout"),
    path("companies/", CompanyListView.as_view(), name="companies"),
    path("companies/add/", CompanyCreateView.as_view(), name="add_companies"),
    path("companies/update/<int:pk>/", CompanyUpdateView.as_view(), name="update_companies"),

    path("companies/delete/<int:pk>/", CompanyDeleteView.as_view(), name="delete_companies"),
    path("company_contact/", get_company_contact, name="get_contact_company"),

    
]
