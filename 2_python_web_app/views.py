from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django import forms

class CrawlForm(forms.Form):
	url = forms.CharField()
	search_text = forms.CharField(max_length=100)
	depth = forms.IntegerField()

def home(request):
	if request.method == 'POST':
		form = CrawlForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect('/results/')
	else:
		form = CrawlForm()

	return render_to_response('index.html',{'form': form }, context_instance=RequestContext(request)) 
