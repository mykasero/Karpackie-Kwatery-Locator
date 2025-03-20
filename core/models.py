from django.db import models
from django.conf import settings
from django.utils import timezone
# Create your models here.

class TestModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column="Test name")
    test_text = models.TextField(db_column="test text")
    
class AppartmentsModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(db_column="Appartment name")
    address = models.CharField(db_column="Appartment address")
    city = models.CharField(db_column="City")
    description = models.TextField(db_column="Appartment description")
    extra_desc = models.TextField(db_column="Additional description", default='', blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class AppartmentsPhotosModel(models.Model):
    appartment = models.ForeignKey(AppartmentsModel, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='appartments_images/')