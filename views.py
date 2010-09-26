from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from django.db.models import Avg, Max
from djapps.torque.models import *
from datetime import *
from decimal import Decimal

def home(request):
    return render_to_response('danielcasner/base.html', {'title': 'Torque', 'string_content':'Nothing to see here yet'})
    return HttpResponse('Nothing to see here yet.')


def car_data(request):
    def fmt_mpg_vs_speed(querry):
        return [[int(mpg), speed] for mpg, speed in querry.values_list('mpg', 'speed')]

    jsvars = []
    
    today = Sample.objects.latest('time').time.date()
    jsvars.append('var today="' + today.isoformat() + '"')

    throttle_cutoff = Decimal('1.0')

    todays_samples = Sample.objects.filter(time__gte=today)
    jsvars.append('var todays_mpg_vs_kph_accel=' + repr(fmt_mpg_vs_speed(todays_samples.filter(throttle__gt =throttle_cutoff))))
    jsvars.append('var todays_mpg_vs_kph_coast=' + repr(fmt_mpg_vs_speed(todays_samples.filter(throttle__lte=throttle_cutoff))))

    old_samples = Sample.objects.filter(time__lt=today)
    old_len = 5000
    jsvars.append('var old_mpg_vs_kph_accel=' + repr(fmt_mpg_vs_speed(old_samples.filter(throttle__gt =throttle_cutoff).order_by('?')[:old_len])))
    jsvars.append('var old_mpg_vs_kph_coast=' + repr(fmt_mpg_vs_speed(old_samples.filter(throttle__lte=throttle_cutoff).order_by('?')[:old_len])))

    two_months_ago = today - timedelta(61,0,0)
    oneday = timedelta(1,0,0)
    history = []
    hi = 0
    qday = today
    while qday > two_months_ago:
        samples = Sample.objects.filter(time__gte=qday, time__lt=qday+oneday).values('vehicle_id').annotate(mpg_avg=Avg('mpg'), temp_max=Max('engine_temp')).filter(vehicle_id=0)
        if len(samples):
            ag = samples[0]
            history.append([hi, ag['mpg_avg'], ag['temp_max']])
        hi -= 1
        qday -= oneday

    jsvars.append('var trend_data=' + repr(history))
        
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
