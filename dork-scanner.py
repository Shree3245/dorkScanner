import requests, re, sys, time,os, argparse
from bs4 import BeautifulSoup
from functools import partial
from multiprocessing import Pool, TimeoutError, cpu_count
from fake_useragent import UserAgent

ua = UserAgent().random

parser = argparse.ArgumentParser(description='Argument parser for dork-scanner')
parser.add_argument('-S', '--search', help='String to be searched for', default='1')
parser.add_argument('-E', '--engine', help='Search engine to be used', default='1')
parser.add_argument('-P', '--page', help='Number of pages to search in', default='1')
parser.add_argument('-Pr', '--process', help='Number of parallel processes', default='1')
results = parser.parse_args(sys.argv[1:])

class SearchEngine():
	def __init__(self, name):
		self.name = name


class Google(SearchEngine):
	def search_for(self, string, start):
		urls = []
		payload = { 'q' : string, 'start' : start }
		headers = { 'User-agent' : ua }
		req = requests.get( 'http://www.google.com/search',payload, headers = headers )
		soup = BeautifulSoup( req.text, 'html.parser' )
		h3tags = soup.findAll('cite',attrs={'class':'iUh30'})
		for h3 in h3tags:
			try:
				urls.append( h3.text )
			except:
				continue
		return urls

class Bing(SearchEngine):
	def search_for(self, string, start):
		urls = []
		payload = { 'q' : string, 'first' : start }
		headers = { 'User-agent' : ua }
		req = requests.get( 'https://www.bing.com/search',payload, headers = headers )
		soup = BeautifulSoup( req.text, 'html.parser' )
		h3tags = soup.find_all( 'li', class_='b_algo' )
		for h3 in h3tags:
			try:
				urls.append(h3.find('a').attrs['href'])
			except:
				continue
		return urls

class Baidu(SearchEngine):
	def search_for(self, string, start):
		urls = []
		payload = { 'wd' : string, 'pn' : start }
		headers = { 'User-agent' : ua }
		req = requests.get( 'http://www.baidu.com/s',payload, headers = headers)
		soup = BeautifulSoup( req.text, 'html.parser' )
		h3tags = soup.find_all( 'h3', class_='t' )
		for url in soup.find_all('h3', class_='t'):
			try:
				urlu = url.find('a').attrs['href']
				link = requests.get(urlu)
				urls.append(link.url)
			except:
				continue
		return urls



def printf(lista): 
	for i in lista:
		link = str(i)
		ch = link.replace("%3F", "?")
		ch2 = ch.replace("%3D","=")
		print( " " + ch2 )

def main():

	try:
		string = results.search
		engine = results.engine
		page   = results.page
		proc    = int( results.process  )
	except:
		print(" * * Error * * Arguments missing")
		exit(0)
	start_time = time.time()
	result = []
	pages = []

	for p in range( 0, int(page)):
		pages.append(p*10)

		p = Pool(proc) 
		print ("#"*50)
		#print "Searching for: "+str(string)+" in "+str(page)+" page(s) of "+str(engine)+" with "+str(proc)+" process(es)"
		print ("Searching for: {} in {} page(s) of {} with {} process(es)".format(str(string),str(page),str(engine),str(proc)))
		print ("#"*50)
		print ("\n")
		if engine == "google":
			search = Google(engine)
			request = partial( search.search_for, string )
			all = p.map(request, pages)

		elif engine == "bing":
			search = Bing(engine)
			request = partial( search.search_for, string )
			all = p.map(request, pages)

		elif engine == "baidu":
			search = Baidu(engine)
			request = partial( search.search_for, string )
			all = p.map(request, pages)
		else:
			search = Google(engine)
			request = partial( search.search_for, string )
			all = p.map(request, pages)

	for p in all:
		result += [ u for u in p]
		printf( set( result ) )
	print ("\n")
	print ("#"*50)
	print( " Number of urls : {}" . format( str( len( result ) ) ))
	print( " Finished in : {} s" . format( str( int( time.time() - start_time ) )))
	print ("#"*50)

if __name__ == '__main__':
	  main()
