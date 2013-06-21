from django.conf.urls.defaults import *

urlpatterns = patterns('',
    ('^$', 'djapps.torque.views.home'),
    ('^upload$', 'djapps.torque.views.upload'),
    ('^mpg_vs_kph.js$', 'djapps.torque.views.mpg_vs_kph'),
    ('^car_data.js$', 'djapps.torque.views.car_data'),
)
