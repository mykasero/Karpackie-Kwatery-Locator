from django.shortcuts import render, redirect, get_object_or_404
from .models import TestModel,AppartmentsModel,AppartmentsPhotosModel
from .forms import AppartmentForm
import googlemaps
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    context = {
        'stats' : {'appartments_number':250,'locations_number':13,'clients_number':500}
    }
    return render(request,"core/home.html", {'context':context})

def appartments(request, appartment_pk):
    current_appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)
    
    appartments_extra_desc = current_appartment.extra_desc.strip("\r\n").split(';')
    if appartments_extra_desc[-1] == '':
        appartments_extra_desc = appartments_extra_desc[:-1]
    
    
    print(f"atuty: {appartments_extra_desc}")
    
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_BACK)
    try:
        geocode_result = gmaps.geocode(current_appartment.address+", "+current_appartment.city)

        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            lat, lng = location['lat'], location['lng']
        else:
            # default coordinates if the geocoding goes wrong
            lat, lng = 50.041069, 21.999145
        
    except Exception as e:
        # default coordinates if the geocoding goes wrong
        lat, lng = 50.041069, 21.999145
    
    print(f"test lat {lat} lng {lng}")
    
    context = {
        'appartment' : current_appartment,
        'extra_desc' : appartments_extra_desc,
        'images' : AppartmentsPhotosModel.objects.all().values(),
        'map_lat' : lat,
        'map_lng' : lng,
        'google_maps' : settings.GOOGLE_MAPS_FRONT,
    }
    
    return render(request,"core/appartments.html", {'context':context})

def gallery(request):
    images = AppartmentsPhotosModel.objects.all().order_by('-id').values()
    
    # paginator = Paginator(images, 20)
    # page_number = request.GET.get('page', 1)
    # page_obj = paginator.get_page(page_number)
    
    image_data=[]
    for image in images:
        print(f"TEST IMAGE -> {image}")
        appartment = get_object_or_404(AppartmentsModel, pk=image['appartment_id'])
        image_data.append({
            'id': image['id'],
            'title': appartment.address + ", " + appartment.city,
            'url': settings.MEDIA_URL+image['image'],
        })
    
    context = {
        'images':image_data,
    }
    
    return render(request,"core/gallery.html", context)

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

            return render(request, "core/home.html")
        else:
            print(f"Form errors: {form.errors}")
    
    else:
        form = AppartmentForm()
        
    return render(request,"core/admin_page.html", {'form':form})