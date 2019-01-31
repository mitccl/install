#Triangulum
#           ________
#          _,.-Y  |  |  Y-._
#      .-~"   ||  |  |  |   "-.
#      I" ""=="|" !""! "|"[]""|     _____
#      L__  [] |..------|:   _[----I" .-{"-.
#     I___|  ..| l______|l_ [__L]_[I_/r(=}=-P
#    [L______L_[________]______j~  '-=c_]/=-^
#     \_I_j.--.\==I|I==_/.--L_]
#       [_((==)[`-----"](==)j
#          I--I"~~"""~~"I--I
#          |[]|         |[]|
#          l__j         l__j
#         |!!|         |!!|
#          |..|         |..|
#          ([])         ([])
#          ]--[         ]--[
#          [_L]         [_L]
#         /|..|\       /|..|\
#        `=}--{='     `=}--{='
#       .-^--r-^-.   .-^--r-^-.
# Resistance is futile @lock_down... 
import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt
from resources.lib.modules import cache

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')


class navigator:
	def root(self):
		self.addDirectoryItem(32001, 'movieNavigator', 'movies.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.jpg', 'DefaultTVShows.jpg')
		if not control.setting('lists.widget') == '0':
			self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.jpg', 'DefaultVideoPlaylists.jpg')
			self.addDirectoryItem(32004, 'mytvNavigator', 'myshows.jpg', 'DefaultVideoPlaylists.jpg')

		self.addDirectoryItem(32008, 'toolNavigator', 'tools.jpg', 'DefaultAddonProgram.jpg')

		downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
		if downloads == True:
			self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.jpg', 'DefaultFolder.jpg')

		self.addDirectoryItem(32010, 'searchNavigator', 'search.jpg', 'DefaultFolder.jpg')

		self.endDirectory()


	def movies(self, lite=False):
		self.addDirectoryItem('Popular', 'movies&url=popular', 'popular.jpg', 'playlist.jpg')
		self.addDirectoryItem(32011, 'movieGenres', 'genres.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem(32012, 'movieYears', 'year.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem('IMDB Top 250', 'movies&url=top2', '250.jpg', 'playlist.jpg')
		self.addDirectoryItem('Fox', 'movies&url=fox', '20.jpg', 'playlist.jpg')
		self.addDirectoryItem('Paramount', 'movies&url=para', 'para.jpg', 'playlist.jpg')
		self.addDirectoryItem('MGM', 'movies&url=pmgm', 'mgm.jpg', 'playlist.jpg')
		self.addDirectoryItem('Disney', 'movies&url=disney1', 'disney.jpg', 'playlist.jpg')
		self.addDirectoryItem('Universal', 'movies&url=uni', 'uni.jpg', 'playlist.jpg')
		self.addDirectoryItem('Sony', 'movies&url=sony', 'sony.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem('Warner Bros', 'movies&url=warb', 'warb.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem('Actor', 'moviePersons', 'actor.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem(32022, 'movies&url=theaters', 'theaters.jpg', 'DefaultRecentlyAddedMovies.jpg')
		#self.addDirectoryItem('Great Directors', 'list3Navigator', 'director.jpg', 'DefaultMovies.jpg')
		
		if lite == False:
			if not control.setting('lists.widget') == '0':
				self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.jpg', 'DefaultVideoPlaylists.jpg')

			#self.addDirectoryItem('Actor Search', 'moviePerson', 'actorsearch.jpg', 'DefaultMovies.jpg')
			self.addDirectoryItem(32010, 'movieSearch', 'search.jpg', 'DefaultMovies.jpg')

		self.endDirectory()


	def mymovies(self, lite=False):
		self.accountCheck()

		if traktCredentials == True and imdbCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.jpg', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.jpg', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
			self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.jpg', 'DefaultMovies.jpg', queue=True)

		elif traktCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.jpg', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.jpg', 'DefaultMovies.jpg', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

		elif imdbCredentials == True:
			self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.jpg', 'DefaultMovies.jpg', queue=True)
			self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.jpg', 'DefaultMovies.jpg', queue=True)

		if traktCredentials == True:
			self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.jpg', 'DefaultMovies.jpg', queue=True)

		elif imdbCredentials == True:
			self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.jpg', 'DefaultMovies.jpg', queue=True)

		if traktIndicators == True:
			self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.jpg', 'DefaultMovies.jpg', queue=True)

		self.addDirectoryItem(32039, 'movieUserlists', 'mymovies.jpg', 'DefaultMovies.jpg')

		if lite == False:
			self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.jpg', 'DefaultMovies.jpg')
			self.addDirectoryItem('Actor Search', 'moviePerson', 'actorsearch.jpg', 'DefaultMovies.jpg')
			self.addDirectoryItem(32010, 'movieSearch', 'search.jpg', 'DefaultMovies.jpg')

		self.endDirectory()


	def tvshows(self, lite=False):
		self.addDirectoryItem('Popular', 'tvshows&url=popular', 'popular.jpg', 'playlist.jpg')
		self.addDirectoryItem(32011, 'tvGenres', 'genres.jpg', 'DefaultTVShows.jpg')
		self.addDirectoryItem(32016, 'tvNetworks', 'networks.jpg', 'DefaultTVShows.jpg')
		self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new.jpg', 'DefaultTVShows.jpg')
		self.addDirectoryItem(32006, 'calendar&url=added', 'new.jpg', 'DefaultRecentlyAddedEpisodes.jpg', queue=True)

		if lite == False:
			if not control.setting('lists.widget') == '0':
				self.addDirectoryItem(32004, 'mytvliteNavigator', 'myshows.jpg', 'DefaultVideoPlaylists.jpg')

			#self.addDirectoryItem('Actor Search', 'tvPerson', 'actorsearch.jpg', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32010, 'tvSearch', 'search.jpg', 'DefaultTVShows.jpg')

		self.endDirectory()


	def mytvshows(self, lite=False):
		self.accountCheck()

		if traktCredentials == True and imdbCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.jpg', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.jpg', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
			self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.jpg', 'DefaultTVShows.jpg')

		elif traktCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.jpg', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
			self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.jpg', 'DefaultTVShows.jpg', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

		elif imdbCredentials == True:
			self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.jpg', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.jpg', 'DefaultTVShows.jpg')

		if traktCredentials == True:
			self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.jpg', 'DefaultTVShows.jpg')

		elif imdbCredentials == True:
			self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.jpg', 'DefaultMovies.jpg', queue=True)

		if traktIndicators == True:
			self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.jpg', 'DefaultTVShows.jpg', queue=True)
			self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.jpg', 'DefaultRecentlyAddedEpisodes.jpg', queue=True)
			self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.jpg', 'DefaultRecentlyAddedEpisodes.jpg', queue=True)

		self.addDirectoryItem(32040, 'tvUserlists', 'mytvshows.jpg', 'DefaultTVShows.jpg')

		if traktCredentials == True:
			self.addDirectoryItem(32041, 'episodeUserlists', 'mytvshows.jpg', 'DefaultTVShows.jpg')

		if lite == False:
			self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.jpg', 'DefaultTVShows.jpg')
			self.addDirectoryItem('Actor Search', 'tvPerson', 'actorsearch.jpg', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32010, 'tvSearch', 'search.jpg', 'DefaultTVShows.jpg')

		self.endDirectory()

	def tools(self):
		self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32556, 'libraryNavigator', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32049, 'viewsNavigator', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32050, 'clearSources', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32052, 'clearCache', 'tools.jpg', 'DefaultAddonProgram.jpg')

		self.endDirectory()

	def library(self):
		self.addDirectoryItem(32557, 'openSettings&query=4.0', 'tools.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.jpg', 'DefaultAddonProgram.jpg')
		self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.jpg', 'DefaultMovies.jpg', isAction=False)
		self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.jpg', 'DefaultTVShows.jpg', isAction=False)

		if trakt.getTraktCredentialsInfo():
			self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.jpg', 'DefaultMovies.jpg')
			self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.jpg', 'DefaultMovies.jpg')
			self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.jpg', 'DefaultTVShows.jpg')
			self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.jpg', 'DefaultTVShows.jpg')

		self.endDirectory()

	def downloads(self):
		movie_downloads = control.setting('movie.download.path')
		tv_downloads = control.setting('tv.download.path')

		if len(control.listDir(movie_downloads)[0]) > 0:
			self.addDirectoryItem(32001, movie_downloads, 'movies.jpg', 'DefaultMovies.jpg', isAction=False)
		if len(control.listDir(tv_downloads)[0]) > 0:
			self.addDirectoryItem(32002, tv_downloads, 'tvshows.jpg', 'DefaultTVShows.jpg', isAction=False)

		self.endDirectory()


	def search(self):
		self.addDirectoryItem(32001, 'movieSearch', 'search.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem(32002, 'tvSearch', 'search.jpg', 'DefaultTVShows.jpg')
		self.addDirectoryItem('Actor Search', 'moviePerson', 'actorsearch.jpg', 'DefaultMovies.jpg')
		self.addDirectoryItem('TV Actor Search', 'tvPerson', 'actorsearch.jpg', 'DefaultTVShows.jpg')

		self.endDirectory()


	def views(self):
		try:
			control.idle()

			items = [ (control.lang(32001).encode('utf-8'), 'movies'), (control.lang(32002).encode('utf-8'), 'tvshows'), (control.lang(32054).encode('utf-8'), 'seasons'), (control.lang(32038).encode('utf-8'), 'episodes') ]

			select = control.selectDialog([i[0] for i in items], control.lang(32049).encode('utf-8'))

			if select == -1: return

			content = items[select][1]

			title = control.lang(32059).encode('utf-8')
			url = '%s?action=addView&content=%s' % (sys.argv[0], content)

			poster, banner, fanart = control.addonPoster(), control.addonBanner(), control.addonFanart()

			item = control.item(label=title)
			item.setInfo(type='Video', infoLabels = {'title': title})
			item.setArt({'icon': poster, 'thumb': poster, 'poster': poster, 'banner': banner})
			item.setProperty('Fanart_Image', fanart)

			control.addItem(handle=int(sys.argv[1]), url=url, listitem=item, isFolder=False)
			control.content(int(sys.argv[1]), content)
			control.directory(int(sys.argv[1]), cacheToDisc=True)

			from resources.lib.modules import views
			views.setView(content, {})
		except:
			return


	def accountCheck(self):
		if traktCredentials == False and imdbCredentials == False:
			control.idle()
			control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
			sys.exit()




	def clearCache(self):
		control.idle()
		yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
		if not yes: return
		from resources.lib.modules import cache
		cache.cache_clear()
		control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')


	def addDirectoryItem(self, name, query, thumb, icon, context=None, queue=False, isAction=True, isFolder=True):
		try: name = control.lang(name).encode('utf-8')
		except: pass
		url = '%s?action=%s' % (sysaddon, query) if isAction == True else query
		thumb = os.path.join(artPath, thumb) if not artPath == None else icon
		cm = []
		if queue == True: cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))
		if not context == None: cm.append((control.lang(context[0]).encode('utf-8'), 'RunPlugin(%s?action=%s)' % (sysaddon, context[1])))
		item = control.item(label=name)
		item.addContextMenuItems(cm)
		item.setArt({'icon': thumb, 'thumb': thumb})
		if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)
		control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)


	def endDirectory(self):
		control.content(syshandle, 'addons')
		control.directory(syshandle, cacheToDisc=True)


