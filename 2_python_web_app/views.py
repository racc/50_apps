from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from crawler import Crawler
from bootstrapforms.forms import BootstrapForm, Fieldset
import re

def home(request):
	return render_to_response('index.html')
