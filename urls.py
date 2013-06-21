from django.conf.urls.defaults import *

urlpatterns = patterns('',
    ('^$', 'pydc.torque.views.home'),
    ('^upload$', 'pydc.torque.views.upload'),
    ('^mpg_vs_kph.js$', 'pydc.torque.views.mpg_vs_kph'),
    ('^car_data.js$', 'pydc.torque.views.car_data'),
)
