from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
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
	search = forms.CharField(max_length=100)
	depth = forms.IntegerField()

def form(request):
	if request.method == 'POST':
		form = CrawlForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			return HttpResponseRedirect(('/crawl?url=%s&search=%s&depth=%s' % (data['url'], data['search'], data['depth'])))
	else:
		form = CrawlForm()
	return render_to_response('crawl_form.html', {'form': form }, context_instance=RequestContext(request)) 

def crawl(request):
	rget = request.GET
	search = rget.get('search')
	url = rget.get('url')
	depth = rget.get('depth')

	if (search == None or url == None or depth == None):
		return HttpResponseBadRequest("Need to specify search term, url and depth")

	regexes = [re.compile(string) for string in search.split()]
	return render_to_response('crawl_results.html', {'results' : Crawler.crawl([url], int(depth), regexes), 'url': url, 'depth': depth, 'search': search})
