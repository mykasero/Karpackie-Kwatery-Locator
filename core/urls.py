from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("kwatery/<int:appartment_pk>/", views.appartments, name="appartments"),
    path("galeria/", views.gallery, name="gallery"),
    path("kontakt/", views.contact, name="contact"),
    path("administracja/", views.admin_page, name="admin_page"),
    path("administracja/dodaj_lokal/", views.add_appartment, name="add_appartment"),
    path("administracja/liczniki/", views.update_counters, name="update_counters"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("rejestracja/", views.register, name="register"),
]
