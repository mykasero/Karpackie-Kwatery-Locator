from django.shortcuts import render, redirect, get_object_or_404
from .models import AppartmentsModel,AppartmentsPhotosModel, HomepageCounters
from .forms import AppartmentForm, CountersForm, ContactForm
import googlemaps, requests, json
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
import datetime as dt
from django.urls import reverse
from django.core.paginator import Paginator
import environ
from django.utils.translation import gettext_lazy as _

env = environ.Env()
environ.Env.read_env()

"""
    Function for checking if the currents session user has staff priviledge
"""
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url = login_url)

"""
    Landing Page view
"""
def home(request):
    """
        If there's data in the counters view, 
        get the latest data and display it in the counters on the landing page,
        if there's none do a safe fail and display 1 in every counter
    """
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
"""
    Appartments view 
"""
def appartments(request, appartment_pk):
    """
        Get the specific appartment by appartment id, 
        display the view with the appartments information,
        based on the location information call the gmaps geocode API to get the latitude and longitude
        which will be used in the map API
    """
    current_appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)
    
    # remove trailing whitespace and newlines, split the text by ";" char
    appartments_extra_desc = current_appartment.extra_desc.strip("\r\n").split(';')
    
    if appartments_extra_desc[-1] == '':
        appartments_extra_desc = appartments_extra_desc[:-1]
    
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_BACK)
    try:
        print(f"test adres - {current_appartment.address}, {current_appartment.city}")
        geocode_result = gmaps.geocode(current_appartment.address+", "+current_appartment.city)
        print("TEST RESULT - ", geocode_result)
        if geocode_result:
            location = geocode_result[0]['geometry']['location']
            lat, lng = location['lat'], location['lng']
        else:
            # default coordinates if the geocoding goes wrong
            lat, lng = 50.041069, 21.999145

        
    except Exception as e:
        # default coordinates if the geocoding goes wrong
        lat, lng = 50.041069, 21.999145
        print(f"geocode_result failed 2 - - {e}")
    
    context = {
        'appartment' : current_appartment,
        'str_city' : current_appartment.address + ', ' + current_appartment.city,
        'extra_desc' : appartments_extra_desc,
        'map_lat' : lat,
        'map_lng' : lng,
        'google_maps' : settings.GOOGLE_MAPS_FRONT,
    }
    
    return render(request,"core/appartments.html", {'context':context})

"""
    Gallery view
"""
def gallery(request):
    """
        Get all the images of every appartment,
        split them into first image and all images, first image will be used as the image for the miniature,
        redistribute them into addresses that their appartments belong to,
        create a paginator that has 9 items per page
    """
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
            'id' : image.id,
        })
    
    gallery_items = []
    
    for address, data in address_groups.items():
        gallery_items.append({
            'title' : address,
            'first_image' : data['first_image'],
            'all_images' : data['all_images'],
        })
    
    paginator = Paginator(gallery_items, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'gallery_items': gallery_items,
        'page_obj' : page_obj,
        'paginated_items' : page_obj.object_list,
    }
    
    return render(request,"core/gallery.html", context)

"""
    Remove image view, available only for staff
"""
@staff_required(login_url="/login/")
def remove_image(request, image_id):
    image = get_object_or_404(AppartmentsPhotosModel, id=image_id)
    image.delete()
    
    return redirect('gallery')

"""
    Admin main page view, available only for staff
"""
@staff_required(login_url="/login/")
def admin_page(request):    
    date_from = (dt.date.today()-dt.timedelta(days=30)).isoformat()  
    graphql_query = f"""
    query {{
      viewer {{
        zones(filter: {{zoneTag: "{settings.CLOUDFLARE_ZONE_ID}"}}) {{
          httpRequests1dGroups(limit: 30, filter: {{date_gt: "{date_from}"}}) {{
            dimensions {{
              date
            }}
            sum {{
              requests
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        "https://api.cloudflare.com/client/v4/graphql",
        headers={
            "Authorization" : f"Bearer {settings.CLOUDFLARE_ZONE_TOKEN}",
            "Content-type" : "application/json",
        },
        json={"query": graphql_query}
    )
    
    data = response.json()
    data_failed = False
    print(f"TEST DATA \ \ \n {data}")
    if not data.get("success", True) or data["data"] == None:
        print("here")
        data_failed = True
        return render(
            request,
            "core/admin_page.html",
            {
                "data_fail" : data_failed,
                "data" : data,
            }
        )
    else:
        print("here2")
        zone_data = data["data"]["viewer"]["zones"][0]
        dates_30 = sum([request["sum"]["requests"] for request in zone_data["httpRequests1dGroups"]])
        dates_7 = sum([request["sum"]["requests"] for request in zone_data["httpRequests1dGroups"][-7:]])
        dates_1 = zone_data["httpRequests1dGroups"][-1]["sum"]["requests"]
        return render(
            request,
            "core/admin_page.html",
            {
                "data_fail" : data_failed,
                "requests_per_timeframe" : [dates_30,dates_7,dates_1],
            }            
        )
    

"""
    Admin add appartment view, available only for staff
"""
@staff_required(login_url="/login/")
def add_appartment(request):
    """
        Render form, if request.method is POST - get the uploaded info and images
        save the information, loop over the images and save them to the current
        appartments instance
    """
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
        
    return render(request,"core/add_appartment.html", {'form':form_appartments})

"""
    Admin edit appartment view, available only for staff
"""
@staff_required(login_url="/login/")
def edit_appartment(request, appartment_pk):
    """
        Works similar to the add appartment view
    """
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
"""
    Admin remove appartment confirmation view, available only for staff
"""
@staff_required(login_url="/login/")
def remove_appartment_conf(request, appartment_pk):
    appartment = get_object_or_404(AppartmentsModel, pk=appartment_pk)
    return render(request, "core/remove_appartment_conf.html", {'appartment':appartment})

"""
    Admin remove appartment view, available only for staff
"""
@staff_required(login_url="/login/")
def remove_appartment(request, appartment_pk):
    """
        Get the specific appartment, if request.method is post, delete the appartment and send 204 response
    """
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

"""
    Admin update counter view, available only for staff
"""
@staff_required(login_url="/login/")
def update_counters(request):
    """
        Render countersform, if request.method is POST - remove previous data and save the current one
    """ 
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

"""
    Login view for staff
"""
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
                messages.warning(request, _("Aby wyświetlić żądaną strone, musisz być zalogowany."))
                
            form = LoginForm()
            return render(request, "core/login.html", {'form':form})

"""
    Logout view
"""  
def logout(request):
    auth_logout(request)
    messages.info(request, _("Wylogowano pomyślnie"))
    return redirect("/")

"""
    Register view
"""
def register(request):
    """
        Render register form, if request.method is POST and data is valid, register new user
        and add him to the admin permissions group
    """
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            group = Group.objects.get(name="admin")
            user.groups.add(group)
            messages.info(request, _("Pomyślnie zarejestrowano jako admin."))
            return redirect('administracja/')

        else:
            return render(request,"core/register.html", {'form':form})
    else:
        form = RegisterForm()
        return render(request,"core/register.html", {'form':form})

"""
    Contact view
"""    
def contact(request):
    """
        Render contact form, if request.method is POST - Send the email with brevo API 
        to the business mailbox
    """ 
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email_address = form.cleaned_data['email']
            name = form.cleaned_data['name']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            send_to = env("EMAIL_SEND_TO")
            subject = f"Zapytanie z formularza kontaktowego od {name}"
            email_body = f"""
            Imie: {name}
            Adres mailowy: {email_address}
            Nr. telefonu: {phone_number}
            
            Wiadomość: {message}
            """
            send_mail(
                subject,
                email_body,
                settings.DEFAULT_FROM_EMAIL,
                [send_to],
            )
            
            messages.success(request, _("Pomyślnie wysłano zgłoszenie."))
            return render(request,"core/home.html")
        else:
            form = ContactForm(request.POST)
            return render(request,"core/contact.html", {'form':form})
    else:
        
        form = ContactForm()
        
    return render(request,"core/contact.html", {'form':form})
    