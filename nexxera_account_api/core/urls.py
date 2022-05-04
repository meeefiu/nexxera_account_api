from rest_framework.urls import path
from core import views

urlpatterns = [
    path('create-account/', views.create_account),
    path('list-account/', views.list_accounts),
    path('create-transaction/', views.create_transaction),
    path('list-transactions/', views.list_extract)
]
