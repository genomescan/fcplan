from django.contrib import admin
# Register your models here.
from .models import StagedSamples
from .models import CombinationRestrictions
admin.site.register(StagedSamples)
admin.site.register(CombinationRestrictions)