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
from django.contrib.auth import views as auth_views
from django.urls import path, include
import fairmieten.views
import fairmieten.form_views
import aggregation.urls

urlpatterns = [
    path("admin/", admin.site.urls),

    path('', fairmieten.views.home, name='home'),

    path("aggregation/", include(aggregation.urls)),

	path('vorgang/neu/', fairmieten.form_views.vorgang_erstellen, {'type_nr': 1}, name='vorgang_erstellen'),
    path('vorgang/neu/<int:type_nr>/', fairmieten.form_views.vorgang_erstellen, name='vorgang_erstellen'),
    path('vorgang/edit/<uuid:vorgang_id>/', fairmieten.form_views.vorgang_bearbeiten, {'type_nr': 1}, name='vorgang_bearbeiten'),
    path('vorgang/edit/<uuid:vorgang_id>/<int:type_nr>/', fairmieten.form_views.vorgang_bearbeiten, name='vorgang_bearbeiten'),
    path('vorgang/delete/<uuid:vorgang_id>/', fairmieten.views.delete_vorgang, name='delete_vorgang'),
    path('vorgang/save/<int:form_nr>/', fairmieten.form_views.save_form, name='save_form'),
    path('vorgang/save/<int:form_nr>/<int:vorgang_id>|None/', fairmieten.form_views.save_form, name='save_form'),
    
    path('vorgang/beratung/', fairmieten.form_views.create_beratung, name='create_beratung'),
    path('vorgang/allgemein/', fairmieten.form_views.create_vorgang, name='create_vorgang'),
    path('vorgang/person', fairmieten.form_views.create_person, name='create_person'),
    path('vorgang/diskriminierung', fairmieten.form_views.create_diskriminierung, name='create_diskriminierung'),
    path('vorgang/verursacher', fairmieten.form_views.create_verursacher, name='create_verursacher'),
    path('vorgang/intervention', fairmieten.form_views.create_intervention, name='create_intervention'),
    path('vorgang/loesungsansaetze', fairmieten.form_views.create_loesungsansaetze, name='create_loesungsansaetze'),
    path('vorgang/ergebnis', fairmieten.form_views.create_ergebnis, name='create_ergebnis'),

    path('vorgang/detail/<uuid:vorgang_id>/', fairmieten.views.vorgang_detail, name='vorgang_detail'),
    path('vorgang/liste/', fairmieten.views.vorgang_liste, name='vorgang_liste'),
    path('vorgang/meine_liste/', fairmieten.views.vorgang_meine_liste, name='vorgang_meine_liste'),
    path('htmx/such_feld/', fairmieten.views.such_feld, name='such_feld'),
    
    path('login/', fairmieten.views.login_view, name='login'),
    path('logout/', fairmieten.views.logout_view, name='logout'),

    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
         ), 
         name='password_reset'),
    
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
         ), 
         name='password_reset_done'),
    
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
         ), 
         name='password_reset_confirm'),
    
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(), 
         name='password_reset_complete'),
]   
