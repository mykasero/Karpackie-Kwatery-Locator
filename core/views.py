from django.shortcuts import render
from core.models import TestModel
# Create your views here.

def home(request):
    context = TestModel.objects.all().values()
    
    return render(request,"core/home.html", {'context':context})