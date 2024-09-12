from django.urls import path, include
from . import views

urlpatterns = [
    path("new/", views.hello_new, name="hello_new"),
    path("list/", views.hello, name="hello_list"),
    path("", views.hello, name="hello_list"),
]
