from django.contrib import admin
from .models import AppartmentsModel, AppartmentsPhotosModel, HomepageCounters

@admin.register(AppartmentsModel)
class AppartmentsModelAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display=('id','name','address', 'description', 'extra_desc','uploaded_on','updated_on','uploaded_by',)
    
@admin.register(AppartmentsPhotosModel)
class AppartmentsPhotosModelAdmin(admin.ModelAdmin):
    list_display=('id','image',)
    
@admin.register(HomepageCounters)
class HomepageCountersModelAdmin(admin.ModelAdmin):
    list_display=('id',)