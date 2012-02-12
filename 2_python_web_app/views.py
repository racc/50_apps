from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django import forms
from crawler import Crawler
from bootstrapforms.forms import BootstrapForm, Fieldset
import re

class CrawlForm(BootstrapForm):
	url = forms.CharField()
	search_strings = forms.CharField(max_length=100)
	depth = forms.IntegerField()

def home(request):
	if request.method == 'POST':
		form = CrawlForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			regexes = [re.compile(string) for string in data['search_strings'].split()]
			results = ['%s matches %s (%d hits)' % ("->".join(hit[0]), hit[1], hit[2]) for hit in Crawler.crawl([data['url']], data['depth'], regexes)]
			return render_to_response('results.html', {'results' : results})
	else:
		form = CrawlForm()

	return render_to_response('index.html',{'form': form }, context_instance=RequestContext(request)) 
