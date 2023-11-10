from django.contrib import admin

from .models import ExampleLip, ExampleNose, Photo

admin.site.register(Photo)
admin.site.register(ExampleLip)
admin.site.register(ExampleNose)
