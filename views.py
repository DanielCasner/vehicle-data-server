from django.shortcuts import render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django import forms
from djapps.torque.models import *
import cPickle as pickle

def home(request):
    return HttpResponse('Nothing to see here yet.')

def upload(request):
    log = file('/home/www-data/djapps/torque/log.pickle', 'a')
    if request.method == 'POST':
        pickle.dump(('POST', request.POST), log, 0)
    elif request.method == 'GET':
        pickle.dump(('GET', request.GET), log, 0)
    return HttpResponse('OK!')
