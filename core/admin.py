from django.contrib import admin
from .models import TestModel, AppartmentsModel, AppartmentsPhotosModel
# Register your models here.

@admin.register(TestModel)
class TestModelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display=('id','name','test_text')
    
@admin.register(AppartmentsModel)
class AppartmentsModelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display=('id','name','address', 'description', 'extra_desc','uploaded_on','updated_on','uploaded_by',)
    
@admin.register(AppartmentsPhotosModel)
class AppartmentsPhotosModelAdmin(admin.ModelAdmin):
    list_display=('id','image',)