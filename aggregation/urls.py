from django.urls import path
from . import views

urlpatterns = [
    path("", views.aggregation, name='aggregation'),
    path("get_chart/", views.get_chart, name='get_chart'),
]

