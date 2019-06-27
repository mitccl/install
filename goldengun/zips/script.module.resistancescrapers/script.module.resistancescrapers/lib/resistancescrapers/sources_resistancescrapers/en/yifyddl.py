import re
import urllib
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['yifyddl.movie']
		self.base_link = 'https://yifyddl.movie/movie/'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			query = '%s-%s' % (title, year)
			url = self.base_link % query
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			
			# 720p
			try:
				r = client.request(url)
				match = re.compile('<a href="http://guard\.link/(.+?)">\n.+?720p').findall(r)
				for url in match:
					url = 'http://guard.link/' + url
					r = client.request(url)
					#import xbmcgui
					#xbmcgui.Dialog().textviewer(url, r)
					
					# Nitroflare
					match = re.compile('http://nitroflare\.com/(.+?)\n').findall(r)
					for url in match:
						host = 'nitroflare.com'
						url = 'http://' + host + '/' + url
						sources.append({
							'source': host,
							'quality': 'HD',
							'language': 'en',
							'url': url,
							'direct': False,
							'debridonly': True
						})
					
					# Openload
					match = re.compile('https://openload\.co/(.+?)\n').findall(r)
					for url in match:
						host = 'openload.co'
						url = 'https://' + host + '/' + url
						sources.append({
							'source': host,
							'quality': 'HD',
							'language': 'en',
							'url': url,
							'direct': False,
							'debridonly': False
						})
			except:
				return
				
			# 1080p
			try:
				r = client.request(url)
				match = re.compile('<a href="http://guard\.link/(.+?)">\n.+?1080p').findall(r)
				for url in match:
					url = 'http://guard.link/' + url
					r = client.request(url)
					#import xbmcgui
					#xbmcgui.Dialog().textviewer(url, r)
					
					# Nitroflare
					match = re.compile('http://nitroflare\.com/(.+?)\n').findall(r)
					for url in match:
						host = 'nitroflare.com'
						url = 'http://' + host + '/' + url
						sources.append({
							'source': host,
							'quality': '1080p',
							'language': 'en',
							'url': url,
							'direct': False,
							'debridonly': True
						})
					
					# Openload
					match = re.compile('https://openload\.co/(.+?)\n').findall(r)
					for url in match:
						host = 'openload.co'
						url = 'https://' + host + '/' + url
						sources.append({
							'source': host,
							'quality': '1080p',
							'language': 'en',
							'url': url,
							'direct': False,
							'debridonly': False
						})
			except:
				return
			
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url

