from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("kwatery/<int:appartment_pk>/", views.appartments, name="appartments"),
    path("kwatery/<int:appartment_pk>/usun/", views.remove_appartment, name="remove_appartment"),
    path("kwatery/<int:appartment_pk>/usun_potwierdzenie/", views.remove_appartment_conf, name="remove_appartment_conf"),
    path("kwatery/<int:appartment_pk>/edytuj/", views.edit_appartment, name="edit_appartment"),
    path("galeria/", views.gallery, name="gallery"),
    path("galeria/usun_zdj/<int:image_id>/", views.remove_image, name="remove_image"),
    path("kontakt/", views.contact, name="contact"),
    path("administracja/", views.admin_page, name="admin_page"),
    path("administracja/dodaj_lokal/", views.add_appartment, name="add_appartment"),
    path("administracja/liczniki/", views.update_counters, name="update_counters"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("rejestracja/", views.register, name="register"),
]
