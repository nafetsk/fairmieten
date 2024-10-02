"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from .hello import urls as hello_urls
import fairmieten.views
import fairmieten.form_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", include(hello_urls)),
    path("aggregation/", fairmieten.views.aggregation),
    path("aggregation/get_chart/", fairmieten.views.get_chart),
    path("aggregation/data/<uuid:id>/", fairmieten.views.get_data),
    path('vorgang/neu/', fairmieten.form_views.vorgang_erstellen, name='vorgang_erstellen'),
]
