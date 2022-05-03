from rest_framework.urls import path
from core import views

urlpatterns = [
    path('create-account/', views.create_account),
    path('list-account/', views.list_accounts),
]
