#!/usr/bin/python2.7

import argparse, urllib2, re
from crawler import Crawler

parser = argparse.ArgumentParser(description='Crawl through all links on the page and scan deep for a given level of depth')
parser.add_argument("-u", "--url", required=True, help="The Base URL")
parser.add_argument("-d", "--depth", required=True, type=int, dest="depth", help="Search Depth", default=3)
parser.add_argument("strings", nargs='*', help="Strings to search for")
args = parser.parse_args()

regexes = [re.compile(string) for string in args.strings]

for hit in Crawler.crawl([args.url], args.depth, regexes):
	print(('%s matches %s (%d hits)' % ("->".join(hit[0]), hit[1], hit[2])))
