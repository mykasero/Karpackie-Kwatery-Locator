from django.shortcuts import render, redirect, get_object_or_404
from .models import AppartmentsModel,AppartmentsPhotosModel, HomepageCounters
from .forms import AppartmentForm, CountersForm
import googlemaps
from django.conf import settings
from django.http import JsonResponse
from django.core.paginator import Paginator
# Create your views here.

def home(request):
    if HomepageCounters.objects.all():
        counters_data = HomepageCounters.objects.order_by('-id').values()[0]
        context = {
            'stats' : {
                'appartments_number':counters_data['appartments_amount'],
                'locations_number':counters_data['locations_amount'],
                'clients_number':counters_data['clients_amount']}
        }
    else:
        context = {
            'stats' : {
                'appartments_number':1,
                'locations_number':1,
                'clients_number':1}
        }
    return render(request,"core/home.html", {'context':context})

def appartments(request, appartment_pk):
    current_appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)
    
    appartments_extra_desc = current_appartment.extra_desc.strip("\r\n").split(';')
    if appartments_extra_desc[-1] == '':
        appartments_extra_desc = appartments_extra_desc[:-1]
    
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
    
    context = {
        'appartment' : current_appartment,
        'str_city' : current_appartment.address + ', ' + current_appartment.city,
        'extra_desc' : appartments_extra_desc,
        'map_lat' : lat,
        'map_lng' : lng,
        'google_maps' : settings.GOOGLE_MAPS_FRONT,
    }
    
    return render(request,"core/appartments.html", {'context':context})

def gallery(request):
    images = AppartmentsPhotosModel.objects.select_related('appartment').all()
    
    address_groups = {}
    for image in images:

        address = image.appartment.address + ", " + image.appartment.city
        if address not in address_groups:
            address_groups[address] = {
                'first_image' : image,
                'all_images' : [],
            }
        address_groups[address]['all_images'].append({
            'url' : image.image.url,
            'title' : address,
        })
    
    gallery_items = []
    
    for address, data in address_groups.items():
        gallery_items.append({
            'title' : address,
            'first_image' : data['first_image'],
            'all_images' : data['all_images'],
        })
    
    context = {
        'gallery_items': gallery_items
    }
    
    return render(request,"core/gallery.html", context)

def contact(request):
    return render(request,"core/contact.html")

def admin_page(request):        
    return render(request,"core/admin_page.html")

def add_appartment(request):
    if request.method=='POST':
        form_appartments = AppartmentForm(request.POST, request.FILES)
        uploaded_files = request.FILES.getlist('images')
        
        if form_appartments.is_valid():
            instance = form_appartments.save(commit=False)
            instance.uploaded_by = request.user
            instance.save()
            
            for image in uploaded_files:
                AppartmentsPhotosModel.objects.create(appartment=instance, image=image)

            return render(request, "core/home.html")
        else:
            print(f"Form errors: {form_appartments.errors}")
            
    else:
        form_appartments = AppartmentForm()
        print(f"test - {form_appartments}")
        
    return render(request,"core/add_appartment.html", {'form':form_appartments})

def update_counters(request):
    if request.method=='POST':
        form_counters = CountersForm(request.POST)

        if form_counters.is_valid():
            # removing the previous data as it won't be needed any longer to save db memory
            HomepageCounters.objects.all().delete()
            form_counters.save()

            return render(request, "core/admin_page.html")
        else:
            print(f"Form errors: {form_counters.errors}")
            
    else:
        form_counters = CountersForm()
        
    return render(request,"core/update_counters.html", {'form':form_counters})