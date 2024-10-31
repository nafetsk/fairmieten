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
import aggregation.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", include(hello_urls)),
    path("aggregation/", include(aggregation.urls)),
    path('vorgang/neu/', fairmieten.form_views.vorgang_erstellen, name='vorgang_erstellen'),
    path('vorgang/edit/<uuid:vorgang_id>/', fairmieten.form_views.vorgang_bearbeiten, name='vorgang_bearbeiten'),
    path('vorgang/allgemein/', fairmieten.form_views.create_vorgang, name='create_vorgang'),
    path('vorgang/person', fairmieten.form_views.create_person, name='create_person'),
    path('vorgang/diskriminierung', fairmieten.form_views.create_diskriminierung, name='create_diskriminierung'),
    path('vorgang/loesungsansaetze', fairmieten.form_views.create_loesungsansaetze, name='create_loesungsansaetze'),
    path('vorgang/ergebnis', fairmieten.form_views.create_ergebnis, name='create_ergebnis'),
    path('', fairmieten.views.home, name='home'),
    path('vorgang/save/<int:form_nr>/', fairmieten.form_views.save_form, name='save_form'),
    path('vorgang/save/<int:form_nr>/<int:vorgang_id>|None/', fairmieten.form_views.save_form, name='save_form'),
    path('vorgang/liste/', fairmieten.views.vorgang_liste, name='vorgang_liste'),
    path('vorgang/meine_liste/', fairmieten.views.vorgang_meine_liste, name='vorgang_meine_liste'),
    path('vorgang/detail/<uuid:vorgang_id>/', fairmieten.views.vorgang_detail, name='vorgang_detail'),
    path('login/', fairmieten.views.login_view, name='login'),
    path('logout/', fairmieten.views.logout_view, name='logout'),
]   
