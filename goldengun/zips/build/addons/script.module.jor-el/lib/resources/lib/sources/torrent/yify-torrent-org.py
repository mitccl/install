import xbmc
import xbmcaddon
import re
import urllib
import urlparse
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import proxy
from resources.lib.modules import cfscrape
from resources.lib.modules import torrent

class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['torrentz2.eu']
		self.base_link = 'https://www.yify-torrent.org'
		self.search_link = '/search/%s/p-1/all/all/'
		
		privateToken = xbmcaddon.Addon('plugin.video.jor-el').getSetting('private.rd.enable')
		if privateToken == 'true':
			self.token = xbmcaddon.Addon('plugin.video.jor-el').getSetting('private.rd.api')
		else:
			self.token = xbmcaddon.Addon('script.realdebrid.mod').getSetting('rd_access')

	def movie(self, imdb, title, localtitle, aliases, year):
		if xbmc.getCondVisibility('System.HasAddon(script.realdebrid.mod)'):
			try:
				title = cleantitle.geturl(title)
				title = title.replace('-','%20')
				url = title+'%20'+year
				return url
			except:
				return
			
	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			q = url

			try: # Page 1
				page = '1'
				url = self.base_link + self.search_link % q
				r = client.request(url)
				#import xbmcgui
				#xbmcgui.Dialog().textviewer(url,r)
				match = re.compile('<a class="movielink" href="(.+?)">').findall(r)
				for url in match: 
					url = 'https://www.yify-torrent.org%s' % (url)
					
					r = client.request(url)
					match = re.compile('magnet\:\?xt=urn\:btih\:(.+?)\&amp').findall(r)
					for hash in match: 
					
						# Find infohash
						url = 'https://api.real-debrid.com/rest/1.0/torrents/instantAvailability/%s?auth_token=%s' % (hash,self.token)
					
						# Check availability
						r = client.request(url)
						r = r.replace('	','').replace('\n','').replace('[','').replace(']','').replace('\/','/').replace('{','')
						r = r.replace('"rd": ',',')
						match = re.compile(',"(.+?)": "filename": "(.+?)"').findall(r)
						for id,filename in match:
							torrenturl = 'magnet:?xt=urn:btoh:%s' % hash
							quality = torrent.qualityCheck(filename)
							# Check video isn't sample
							#if quality not in filename: pass
							for check in torrent.check_filename:
								if check in filename:
									if '.mkv' in filename or '.mp4' in filename or '.flv' in filename or '.avi' in filename:
										url = 'url="%s"&filename="%s"&id="%s"' % (torrenturl,filename,id)
										sources.append({'source': 'Torrent','info': filename,'quality': quality,'language': 'en','url': url,'direct': False,'debridonly': False})
			except: return

		except Exception:
			return
		return sources

	def resolve(self, url):
		match = re.compile('url="(.+?)"&filename="(.+?)"&id="(.+?)"').findall(url)
		# Fetch magnet link
		for url,filename,id in match:
			id = id
			filename = filename.replace('[','').replace(']','').replace('(','').replace(')','')
			magnetLink = urllib.quote_plus(url)
				
			# Pass on to script.realdebrid.mod...
			import xbmc
			if id == '1': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=4&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '2': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=14&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '3': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=15&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '4': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=16&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '5': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=17&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '6': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=18&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '7': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=19&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '8': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=20&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '9': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=21&name=na&poster=na&link='+magnetLink+'&url)')
			if id == '10': xbmc.executebuiltin('RunPlugin(plugin://script.realdebrid.mod/?fanart=na&icon=na&mode=22&name=na&poster=na&link='+magnetLink+'&url)')
				
			import time
			time.sleep(3)
				
			api = 'https://api.real-debrid.com/rest/1.0/torrents?auth_token=%s' % self.token
			r = client.request(api)
			r = r.replace('	','').replace('\n','').replace('[','').replace(']','').replace('\/','/').replace('(','').replace(')','')
			match = re.compile('"filename": "'+filename+'","hash": ".+?","bytes": .+?,"host": ".+?","split": .+?,"progress": 100,"status": "downloaded","added": ".+?","links": "https://real-debrid\.com/d/(.+?)"').findall(r)
			for url in match: 
				url = 'plugin://script.realdebrid.mod/?url=https://real-debrid.com/d/%s&mode=5&name=Real-Debrid&icon=none&fanart=none&poster=none' % url
				return url
			
			