from django.contrib import admin
# Register your models here.
from .models import StagedSample
from .models import CombinationRestriction
admin.site.register(StagedSample)
admin.site.register(CombinationRestriction)