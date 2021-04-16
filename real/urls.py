from django.urls import path

from . import views

app_name = 'real'

urlpatterns = [
    path('', views.index, name='index'),
    path('rest/', views.barcode_list),
]