#!/usr/bin/python2.7

import argparse, urllib2, re
from BeautifulSoup import BeautifulSoup

def crawl(urls, depth, regexes, urls_seen=set([])):
	if (depth == 0):
		return

	this_url = urls[-1]

	try:
		html = urllib2.urlopen(this_url).read()

		for regex in regexes:
			matches = regex.findall(html)
			if (matches):
				print('%s matches %s (%d hits)' % ("->".join(urls), regex.pattern, len(matches)))

		soup = BeautifulSoup(html)
		links = [tag['href'] for tag in soup.findAll('a', href=True)]

		#Fix Local Links
		fixed_links = [fix_link(this_url, link) for link in links]

		for link in fixed_links:
			if link not in urls_seen:
				urls_seen.add(link)	

				try:
					crawl(urls + [link], depth - 1, regexes, urls_seen)
				except (RuntimeError, urllib2.URLError):
					print('Error processing URL: %s' % this_url)
				
	except (RuntimeError, urllib2.URLError):
		print('Error processing URL: %s' % this_url)

def fix_link(base_url, link):
	if link.startswith('http'):
		return link
	else:
		return base_url + '/' + link	

parser = argparse.ArgumentParser(description='Crawl through all links on the page and scan deep for a given level of depth')
parser.add_argument("-u", "--url", required=True, help="The Base URL")
parser.add_argument("-d", "--depth", required=True, type=int, dest="depth", help="Search Depth", default=3)
parser.add_argument("strings", nargs='*', help="Strings to search for")
args = parser.parse_args()

regexes = [re.compile(string) for string in args.strings]

crawl([args.url], args.depth, regexes)
