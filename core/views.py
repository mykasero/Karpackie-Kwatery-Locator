from django.shortcuts import render, redirect, get_object_or_404
from .models import TestModel,AppartmentsModel,AppartmentsPhotosModel
from .forms import AppartmentForm

# Create your views here.

def home(request):
    context = {
        'context': TestModel.objects.all().values(),
        'stats' : {'appartments_number':250,'locations_number':13,'clients_number':500}
    }
    print(context)
    return render(request,"core/home.html", {'context':context})

def appartments(request, appartment_pk):
    current_appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)
    
    appartments_extra_desc = current_appartment.extra_desc.split(';')
    print(appartments_extra_desc)
    # print("extra_desc test = ", appartments_extra_desc)
    
    context = {
        'appartment' : current_appartment,
        'extra_desc' : appartments_extra_desc,
        'images' : AppartmentsPhotosModel.objects.all().values(),
    }
    
    # print("kwatery data - ", context['appartments'])
    # print("zdjecia data - ", context['images'])
    return render(request,"core/appartments.html", {'context':context})

def gallery(request):
    return render(request,"core/gallery.html")

def contact(request):
    return render(request,"core/contact.html")

def admin_page(request):
    if request.method=='POST':
        form = AppartmentForm(request.POST, request.FILES)
        uploaded_files = request.FILES.getlist('images')
        
        if form.is_valid():
            instance = form.save(commit=False)
            instance.uploaded_by = request.user
            instance.save()

            for image in uploaded_files:
                AppartmentsPhotosModel.objects.create(appartment=instance, image=image)
            
            return redirect('apartments')

        else:
            print(f"Form errors: {form.errors}")
    else:
        
        form = AppartmentForm()
        
    return render(request,"core/admin_page.html", {'form':form})