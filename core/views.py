from django.shortcuts import render, redirect, get_object_or_404
from .models import AppartmentsModel,AppartmentsPhotosModel, HomepageCounters
from .forms import AppartmentForm, CountersForm, ContactForm
import googlemaps
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from core.forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from datetime import datetime
import json
from django.urls import reverse

def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url = login_url)

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

@staff_required(login_url="/login/")
def admin_page(request):        
    return render(request,"core/admin_page.html")

@staff_required(login_url="/login/")
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

@staff_required(login_url="/login/")
def edit_appartment(request, appartment_pk):
    appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)

    if request.method == "POST":
        form = AppartmentForm(request.POST, request.FILES, instance=appartment, initial={
            'name' : appartment.name,
            'address' : appartment.address,
            'city' : appartment.city,
            'extra_desc' : appartment.extra_desc,
        })
        uploaded_files = request.FILES.getlist('images')
        if form.is_valid():
            
            instance = form.save(commit=False)
            instance.updated_on = datetime.now()
            instance.uploaded_by = request.user
            instance.save()
            
            
            for image in uploaded_files:
                AppartmentsPhotosModel.objects.create(appartment=instance, image=image)
            
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger' : json.dumps({
                        "appartmentUpdated" : "True",
                        "showMessage" : f"Zaktualizowano apartament",
                    })
                }
            )
        else:
            return render(request, 'core/edit_appartment.html', {
                'form' : form,
                'appartment' : appartment,
            })
    else:
        form = AppartmentForm(instance=appartment, initial={
            'name' : appartment.name,
            'address' : appartment.address,
            'city' : appartment.city,
            'extra_desc' : appartment.extra_desc,
        })
        return render(request, 'core/edit_appartment.html', {
                'form' : form,
                'appartment' : appartment,
            })

@staff_required(login_url="/login/")
def remove_appartment_conf(request, appartment_pk):
    appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)
    return render(request, "core/remove_appartment_conf.html", {'appartment':appartment})

@staff_required(login_url="/login/")
def remove_appartment(request, appartment_pk):
    appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)
    if request.method == "POST":
        appartment.delete()

        return HttpResponse(
            status=204,
            headers={
                'HX-Redirect' : reverse("home"),
                'HX-Trigger' : json.dumps({
                    "appartmentDeleted" : "True",
                    "showMessage" : f"Usunięto apartament",
                })
            }
        )


@staff_required(login_url="/login/")
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


def login(request):
    if request.user.is_authenticated:          
        return render(request,"core/admin_page.html")
    
    else:
        if request.method == "POST":
            form = LoginForm()
            username = request.POST['login']
            password = request.POST['haslo']
            
            user = authenticate(request, username = username, password = password)
            if user is not None:
                auth_login(request,user)
                return render(request, "core/admin_page.html")
            
            else:
                messages.error(request,"Podano niewłaściwe dane")
                return render(request,"core/login.html", {'form':form})
        else:
            if 'next' in request.GET:
                messages.warning(request, f"Aby wyświetlić żądaną strone, musisz być zalogowany.")
                
            form = LoginForm()
            return render(request, "core/login.html", {'form':form})
        
def logout(request):
    auth_logout(request)
    messages.info(request,"Wylogowano pomyślnie")
    return redirect("/")

def register(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            group = Group.objects.get(name="admin")
            user.groups.add(group)
            messages.info(request, "Pomyślnie zarejestrowano jako admin.")
            # return render(request, "core/admin_page.html")
            return redirect('administracja/')

        else:
            return render(request,"core/register.html", {'form':form})
    else:
        form = RegisterForm()
        return render(request,"core/register.html", {'form':form})
    
    
    
def contact(request):
    form = ContactForm()
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            # send_mail(
            #     f"Wiadomość z formularza od {form.cleaned_data['name']} ({form.cleaned_data['email']})",
            #     f"{form.cleaned_data['message']}    \n Numer telefonu kontaktującego -> {form.cleaned_data['phone_number']}",
            #     form.cleaned_data['email'],
            #     ['mykasero20@gmail.com'],
            #     fail_silently=False,
            # )
            messages.success(request, "Pomyślnie wysłano wiadomość.")
            return redirect("/")
        else:
            return render(request,"core/contact.html", {'form':form})
    else:
        form = ContactForm()
        return render(request,"core/contact.html", {'form':form})
    