from django.urls import path
from . import views

urlpatterns = [
    path("", views.aggregation, name='aggregation'),
    path("get_chart/", views.get_chart, name='get_chart'),
    path("csv_download/", views.csv_download, name='csv_download'),
    path("codebook_download_json/", views.codebook_download_json, name='codebook_download'),
    path("codebook_download_txt/", views.codebook_download_txt, name='codebook_download'),
    path("disable_year/", views.disable_year, name='disable_year'),
]

