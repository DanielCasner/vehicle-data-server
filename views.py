from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from djapps.torque.models import *
from datetime import datetime
from decimal import Decimal

def home(request):
    return render_to_response('danielcasner/base.html', {'title': 'Torque', 'string_content':'Nothing to see here yet'})
    return HttpResponse('Nothing to see here yet.')

def upload(request):
    try:
        time = datetime.fromtimestamp(float(request.GET['time'])/1000.0)
        lat  = request.GET.get('kff1006')
        if lat: lat = Decimal(lat)
        lon  = request.GET.get('kff1005')
        if lon: lon = Decimal(lon)
        #altitude = ???
        mpg  = Decimal(request.GET['kff1201'])
        throttle = Decimal(request.GET['k11'])
        speed = Decimal(request.GET['kd'])
        rpm = request.GET.get('kc')
        if rpm: rpm = Decimal(rpm)
        etmp = request.GET.get('k5')
        if etmp: etmp = Decimal(etmp)
        vid = 0 # Where could I get this?
    except Exception, inst:
        errlog = file('upload_errors.log', 'a')
        errlog.write('Sample error:\n\t%s\n\t%s\n\n' % (inst, repr(request.GET)))
        errlog.close()
    else:
        Sample.objects.create(time=time,
                              latitude=lat,
                              longitude=lon,
                              mpg=mpg,
                              throttle=throttle,
                              rpm=rpm,
                              engine_temp=etmp,
                              vehicle_id=vid)
    return HttpResponse('OK!')
