import urllib2
from BeautifulSoup import BeautifulSoup 

class Crawler:
	@classmethod
	def crawl(cls, urls, depth, regexes, urls_seen=set([])):
		if (depth == 0):
			return
	
		this_url = urls[-1]
	
		try:
			html = urllib2.urlopen(this_url).read()
	
			for regex in regexes:
				matches = regex.findall(html)
				if (matches):
					yield (urls, regex.pattern, len(matches))
	
			soup = BeautifulSoup(html)
			links = [tag['href'] for tag in soup.findAll('a', href=True)]
	
			#Fix local links, and filter invalid links
			filtered_links = [cls.filter_link(link) for link in links]
			fixed_links = [cls.fix_link(this_url, link) for link in filtered_links if link]
	
			for link in fixed_links:
				if link not in urls_seen:
					urls_seen.add(link)	
					cls.crawl(urls + [link], depth - 1, regexes, urls_seen)
					
		except (RuntimeError, urllib2.URLError):
			print('Error processing URL: %s' % this_url)
			return
	
	@classmethod
	def fix_link(cls, base_url, link):
		if link.startswith('http'):
			return link
		else:
			return base_url + '/' + link	
	
	@classmethod
	def filter_link(cls, link):
		if link.startswith('mailto'):
			return None
		else:
			return link

