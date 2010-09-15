from django.conf.urls.defaults import *
from djappssl.finance.models import Account

urlpatterns = patterns('',
    ('^$', 'djapps.torque.views.home'),
    ('^upload$', 'djapps.torque.views.upload'),
)
