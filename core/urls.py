from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("kwatery/<int:appartment_pk>/", views.appartments, name="appartments"),
    path("galeria/", views.gallery, name="gallery"),
    path("kontakt/", views.contact, name="contact"),
    path("administracja/", views.admin_page, name="admin_page"),
]
