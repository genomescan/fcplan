from django.contrib import admin
# Register your models here.
from .models import Document, Contact

admin.site.register(Document)
admin.site.register(Contact)
