from modeltranslation.translator import register, TranslationOptions
from .models import AppartmentsModel

# Additional form field in the appartments for adding an English translation of the appartments description
@register(AppartmentsModel)
class AppartmentTranslationOptions(TranslationOptions):
    fields = ('extra_desc',)
    
