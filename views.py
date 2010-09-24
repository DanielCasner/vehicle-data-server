from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from django.db.models import Avg, Max
from djapps.torque.models import *
from datetime import datetime
from decimal import Decimal

def home(request):
    return render_to_response('danielcasner/base.html', {'title': 'Torque', 'string_content':'Nothing to see here yet'})
    return HttpResponse('Nothing to see here yet.')


def car_data(request):
    def fmt_mpg_vs_speed(querry):
        return [[int(s['mpg']), s['speed']] for s in querry.values('mpg', 'speed')]

    jsvars = []
    
    today = Sample.objects.order_by('time').reverse()[0].time.date()
    jsvars.append('var today="' + today.isoformat() + '"')

    throttle_cutoff = Decimal('1.0')

    todays_samples = Sample.objects.filter(time__gte=today)
    jsvars.append('var todays_mpg_vs_kph_accel=' + repr(fmt_mpg_vs_speed(todays_samples.filter(throttle__gt =throttle_cutoff))))
    jsvars.append('var todays_mpg_vs_kph_coast=' + repr(fmt_mpg_vs_speed(todays_samples.filter(throttle__lte=throttle_cutoff))))

    old_samples = Sample.objects.filter(time__lt=today)
    old_len = 10000
    jsvars.append('var old_mpg_vs_kph_accel=' + repr(fmt_mpg_vs_speed(old_samples.filter(throttle__gt =throttle_cutoff)[:old_len])))
    jsvars.append('var old_mpg_vs_kph_coast=' + repr(fmt_mpg_vs_speed(old_samples.filter(throttle__lte=throttle_cutoff)[:old_len])))

    #two_months_ago = today - timedelta(60,0,0)
    #last_two_months = Sample.objects.filter(time__gte=two_months_ago)
    #two_months_mpg = last_two_months.values('time').annotate(mpg_avg=Avg('mpg'))
    
    jsvars.append('')
    return HttpResponse(';\n'.join(jsvars))


def mpg_vs_kph(request):
    def fmt_array(querry):
        return [[int(s['mpg']), s['speed']] for s in querry.values('mpg', 'speed')]
    return HttpResponse('var mpg_vs_kph = %s;\n' % (repr(fmt_array(Sample.objects)),))

def upload(request):
    try:
        time = datetime.fromtimestamp(float(request.GET['time'])/1000.0)
        lat  = request.GET.get('kff1006')
        if lat: lat = Decimal(lat)
        lon  = request.GET.get('kff1005')
        if lon: lon = Decimal(lon)
        #altitude = ???
        mpg  = Decimal(request.GET.get('kff1201', '0.0'))
        throttle = Decimal(request.GET['k11'])
        speed = Decimal(request.GET['kd'])
        rpm = request.GET.get('kc')
        if rpm: rpm = Decimal(rpm)
        etmp = request.GET.get('k5')
        if etmp: etmp = Decimal(etmp)
        vid = 0 # Where could I get this?
    except Exception, inst:
        errlog = file('/home/www-data/djapps/torque/upload_errors.log', 'a')
        errlog.write('Sample error:\n\t%s\n\t%s\n\n' % (inst, repr(request.GET)))
        errlog.close()
    else:
        try:
            Sample.objects.create(time=time,
                                  latitude=lat,
                                  longitude=lon,
                                  mpg=mpg,
                                  throttle=throttle,
                                  speed=speed,
                                  rpm=rpm,
                                  engine_temp=etmp,
                                  vehicle_id=vid)
        except Exception, inst:
            errlog = file('/home/www-data/djapps/torque/insert_errors.log', 'a')
            errlog.write(str(inst) + '\n\n')
            errlog.close()
    return HttpResponse('OK!')
