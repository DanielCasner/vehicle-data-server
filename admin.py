from djapps.torque.models import *
from django.contrib import admin

class SampleAdmin(admin.ModelAdmin):
    model = Sample
    list_display = ('time', 'mpg', 'throttle', 'speed')

admin.site.register(Sample, SampleAdmin)
