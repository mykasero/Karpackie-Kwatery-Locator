from .models import AppartmentsModel
from django.core.cache import cache
from datetime import date
'''
    return a dict of dicts like this:
    {
        'city':city_name1:{
            'appartment_id':1,'address':address1,'appartment_id':3,'address':address3
            },
        'city:city_name2{
            'appartment_id':2,'address':address2,}  
        },
        ...etc
    }
    so each appartment will be pointed via id to the correct template and later the data for the template can be generated
    
    the navbar should look like
    >city_name1
        >address1 pointing to appartment 1
        >address3 pointing to appartment 3
    >city_name2
        >address2 pointing to appartment 2
    ...etc
    
'''
def cities_context(request):
    # appartments = cache.get('appartments')
    # if not appartments:
    all_apps = AppartmentsModel.objects.all().values('pk','id','city','address')
    all_cities = [appartment['city'] for appartment in AppartmentsModel.objects.all().values('city').distinct()]
        # cache.set('appartments', all_apps, timeout=60*60) # Cache for 1hour
        
    return {
        'cities_list' : all_cities,
        'appartments' : all_apps,
    }
    
def current_year_context(request):
    current_year = date.today().year
    
    return {
        'current_year' : current_year,
    }