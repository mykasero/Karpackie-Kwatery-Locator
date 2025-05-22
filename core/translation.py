from modeltranslation.translator import register, TranslationOptions
from .models import AppartmentsModel

@register(AppartmentsModel)
class AppartmentTranslationOptions(TranslationOptions):
    fields = ('extra_desc',)
    
print('translation.py loaded')