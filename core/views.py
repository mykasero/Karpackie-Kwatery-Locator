from django.shortcuts import render
from core.models import TestModel
# Create your views here.

def home(request):
    context = TestModel.objects.all().values()
    
    return render(request,"core/home.html", {'context':context})

def apartments(request):
    return render(request,"core/apartments.html")

def gallery(request):
    return render(request,"core/gallery.html")

def contact(request):
    return render(request,"core/contact.html")

def admin_page(request):
    return render(request,"core/admin_page.html")