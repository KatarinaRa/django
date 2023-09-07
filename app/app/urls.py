"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from app1 import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('predmeti/', views.predmeti, name='predmeti'),
    path('login/', views.logIn, name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('add_predmet/', views.add_predmet, name='add_predmet'),
    path('delete_predmet/<int:predmet_id>', views.delete_predmet, name='delete_predmet'),
    path('delete_predmetconf/<int:predmet_id>', views.delete_predmetconf, name='delete_predmetconf'),
    path('edit_predmet/<int:predmet_id>', views.edit_predmet),
    path('studenti/', views.get_students, name='studenti'),
    path('add_students/', views.add_students, name='add_students'),
    path('edit_students/<int:student_id>', views.edit_students),
    path('profesors/', views.get_profesors, name='profesors'),
    path('add_profesors/', views.add_profesors, name='add_profesors'),
    path('edit_profesors/<int:profesor_id>', views.edit_profesors),
    path('predmeti_profesor/', views.predmeti_po_profesoru, name='predmet_profesor'),
    path('upisni_list/', views.upisni_list, name='upisni_list'),
    path('upisni_list/<int:student_id>', views.upisni_list_admin, name='upisni_list'),
    path('studenti_predmet/<int:predmet_id>', views.studenti_po_predmetu),
    path('edit_status/<int:upis_id>', views.edit_status, name='edit_status'),
    path('filtriranje/', views.filtriranje, name='filtriranje'),
    path('filtriranje1/', views.filtriranje1, name='filtriranje1'),
    path('prikaz_predmeta/', views.prikazi_predmete, name='prikazi_predmete'),
    
    
    
]
