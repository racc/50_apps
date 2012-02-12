import urllib2
from urlparse import urlsplit, SplitResult
from BeautifulSoup import BeautifulSoup 

class Crawler:
	@classmethod
	def crawl(cls, urls, depth, regexes, urls_seen=set([])):
		if (depth == 0):
			return

		this_url = urls[-1]
		urls_seen.add(this_url)
		parsed = urlsplit(this_url)
	
		try:
			req = urllib2.Request(this_url)
			resp = urllib2.urlopen(req)
			if (resp.info().getmaintype() != 'text'):
				return	

			html = resp.read()
			soup = BeautifulSoup(html)
			for regex in regexes:
				res = soup.findAll(text=regex)
				if (res):
					yield (urls, regex.pattern, len(res))
	
			links = [urlsplit(tag['href']) for tag in soup.findAll('a', href=True)]
	
			#Fix local links, and filter invalid links
			filtered_links = [cls.filter_link(link) for link in links]
			fixed_links = [cls.fix_link(parsed, link).geturl() for link in filtered_links if link]
	
			for link in fixed_links:
				if link not in urls_seen:
					for crawl in cls.crawl(urls + [link], depth - 1, regexes, urls_seen):
						yield crawl

		except (RuntimeError, urllib2.URLError):
			print('Error processing URL: %s' % this_url)
		return
	
	@classmethod
	def fix_link(cls, base_url, link):
		if link.scheme.startswith('http'):
			return link
		else:
			return SplitResult(scheme='http', netloc=base_url.netloc, path=link.netloc, query=link.query, fragment=link.fragment)
	
	@classmethod
	def filter_link(cls, link):
		if link.scheme == 'mailto':
			return None
		else:
			return link

