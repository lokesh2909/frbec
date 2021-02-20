from django.contrib import admin
from django.urls import path
from .views import get_all_points, add_transaction, spend_points

urlpatterns = [
    path('add-transaction/', add_transaction, name="new_transaction"),
    path('spend-points/', spend_points.as_view(), name="spend_points"),
    path('all-points/', get_all_points, name="all_points"),
]