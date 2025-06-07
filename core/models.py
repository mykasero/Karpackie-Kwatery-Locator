from django.db import models
from django.conf import settings
from django.utils import timezone


# Model responsible for storing the appartments
class AppartmentsModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column="Appartment name")
    address = models.CharField(db_column="Appartment address")
    city = models.CharField(db_column="City")
    description = models.TextField(db_column="Appartment description", default='', blank=True)
    extra_desc = models.TextField(db_column="Additional description", default='')
    uploaded_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
 
# SubModel for storing the photos of specific model connected to it by FK
class AppartmentsPhotosModel(models.Model):
    appartment = models.ForeignKey(AppartmentsModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='appartments_images/')

# Simple model for storing the current counters data that is displayed on the landing page    
class HomepageCounters(models.Model):
    id = models.AutoField(primary_key=True)
    appartments_amount = models.IntegerField(db_column="Appartments Amount", default=0)
    locations_amount = models.IntegerField(db_column="Locations Amount", default=0)
    clients_amount = models.IntegerField(db_column="Clients Amount", default=0)
    
    