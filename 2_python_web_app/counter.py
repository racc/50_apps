import re, urllib2, itertools, collections
from BeautifulSoup import BeautifulSoup 

class Counter:
	@classmethod
	def count(cls, url):
		try:
			req = urllib2.Request(url)
			resp = urllib2.urlopen(req)
			headers = resp.info()
			if (headers.getmaintype() != 'text'):
				return None
			
			html = resp.read()
			soup = BeautifulSoup(html)
			texts = soup.findAll(text=True)
			visible_texts = filter(cls.visible, texts)
			transformed_texts = map(cls.transform, visible_texts)
			reduced_texts = reduce(lambda x, y: x + " " + y, transformed_texts) 
			words = re.split('\s+', reduced_texts)
			counted = sorted(collections.Counter(words).items(), key=lambda x: -x[1])
			return counted

		except (RuntimeError, urllib2.URLError, IOError):
			print('Error processing URL: %s' % this_url)
			return None

	@classmethod
	def visible(cls, element):
		if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
			return False
	 	elif re.match('.*<!--.*-->.*', element, re.DOTALL):
			return False
		return True

	@classmethod
	def transform(cls, element):
		return re.sub('\W+', ' ', element).lower()

