from rest_framework.urls import path
from core import views

urlpatterns = [
    path('accounts/', views.AccountView.as_view()),
    path('transactions/', views.TransactionView.as_view()),
    path('extracts/', views.ExtractView.as_view())
]
