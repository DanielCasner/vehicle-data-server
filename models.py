from django.db import models

class Sample(models.Model):
    time = models.DateTimeField(editable=False,
                                help_text='Timestamp for the sample')
    latitude = models.DecimalField(max_digits=16, decimal_places=13, null=True, blank=True, editable=False,
                                   help_text='Location, latidute of sample')
    longitude = models.DecimalField(max_digits=16, decimal_places=13, null=True, blank=True, editable=False,
                                    help_text='Location, longitude of sample')
    altitude = models.IntegerField(null=True, blank=True, editable=False,
                                   help_text='Location, altitude of sample')
    mpg = models.DecimalField(max_digits=6, decimal_places=3, editable=False, verbose_name='Miles per Gallon',
                              help_text='Reported fuel efficiency in miles/gallon.')
    throttle = models.DecimalField(max_digits=11, decimal_places=8, editable=False,
                                   help_text='Throttle %')
    rpm = models.IntegerField(blank=True, null=True, editable=False, verbose_name='engine revolutions per minute',
                              help_text='Engine speed (RPM)')
    speed = models.PositiveSmallIntegerField(blank=True, editable=False,
                                             help_text='Vehicle speed (KPH)')
    engine_temp = models.PositiveSmallIntegerField(editable=False, verbose_name='engine coolent temperature',
                                                   help_text='Engine coolent temperature (C)')
    vehicle_id = models.IntegerField(null=True, blank=True,
                                     help_text='Vehigle identifier for this record.')

    
