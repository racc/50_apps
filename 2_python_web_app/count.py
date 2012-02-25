from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from counter import Counter
from bootstrapforms.forms import BootstrapForm, Fieldset

class CountForm(BootstrapForm):
	url = forms.CharField()

def form(request):
	if request.method == 'POST':
		form = CountForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			return HttpResponseRedirect(('/count?url=%s' % (data['url'])))
	else:
		form = CountForm()
	return render_to_response('count_form.html', {'form': form }, context_instance=RequestContext(request)) 

def count(request):
	url = request.GET.get('url')	

	if (url == None):
		return HttpResponseBadRequest("Need to specify a url") 

	return render_to_response('count_results.html', {'url': url, 'results': Counter.count(url)})
