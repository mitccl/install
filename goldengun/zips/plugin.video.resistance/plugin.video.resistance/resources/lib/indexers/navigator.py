# -*- coding: utf-8 -*-

'''
    resistance Add-on
    Copyright (C) 2020 lockdown_machine
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import os,sys,urlparse,xbmcaddon,xbmc,urllib2,xbmcgui

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
		ADDON_ID      = xbmcaddon.Addon().getAddonInfo('id')
		HOMEPATH      = xbmc.translatePath('special://home/')
		ADDONSPATH    = os.path.join(HOMEPATH, 'addons')
		THISADDONPATH = os.path.join(ADDONSPATH, ADDON_ID)
		#NEWSFILE      = 'https://pastebin.com/'
		LOCALNEWS     = os.path.join(THISADDONPATH, 'whatsnew.txt')
	
		def root(self):
			self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
			self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Top Movies', 'playlistNavigator', 'top.png', 'DefaultMovies.png')
			self.addDirectoryItem('Playlists', 'customNavigator', 'play.png', 'DefaultMovies.png')
			#self.addDirectoryItem('IPTV Channels', 'iptvNavigator', 'iptv.png', 'fanart.png')
			self.addDirectoryItem('Swift Streams', 'swiftNavigator', 'swift.png', 'fanart.png')
			self.addDirectoryItem('SportPlugins', 'sportplugins', 'sports.png', 'fanart.png')
			self.addDirectoryItem('Extended Info', 'extinfo', 'ext.png', 'DefaultTVShows.png')
			self.addDirectoryItem('TMDB', 'tmdbNavigator', 'tmdb1.png', 'DefaultMovies.png')
			if not control.setting('lists.widget') == '0':
				self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
				self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')
				self.addDirectoryItem('Scraper Settings', 'openscrapersSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
				self.addDirectoryItem('Resolve Url Settings', 'ruSettings', 'ru.png', 'DefaultFolder.png')
				self.addDirectoryItem('Metalgear Settings', 'metSettings', 'ext.png', 'DefaultFolder.png')
				self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')

			self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')
			downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
			if downloads == True:
				self.addDirectoryItem(32009, 'downloadNavigator', 'business.png', 'DefaultFolder.png')
				
				#self.addDirectoryItem('', 'newsNavigator', 'tools.png', 'DefaultAddonProgram.png')
 			self.endDirectory()

#######################################################################

		def news(self):
				message=self.open_news_url(self.NEWSFILE)
				r = open(self.LOCALNEWS)
				compfile = r.read()       
				if len(message)>1:
						if compfile == message:pass
						else:
								text_file = open(self.LOCALNEWS, "w")
								text_file.write(message)
								text_file.close()
								compfile = message
				self.showText('[B][COLOR springgreen]Latest Updates and Information[/COLOR][/B]', compfile)
		
		def open_news_url(self, url):
				req = urllib2.Request(url)
				req.add_header('User-Agent', 'klopp')
				response = urllib2.urlopen(req)
				link=response.read()
				response.close()
				print link
				return link

		def news_local(self):
			r = open(self.LOCALNEWS)
			compfile = r.read()
			self.showText('[B]Updates and Information[/B]', compfile)

		def showText(self, heading, text):
			id = 10147
			xbmc.executebuiltin('ActivateWindow(%d)' % id)
			xbmc.sleep(500)
			win = xbmcgui.Window(id)
			retry = 50
			while (retry > 0):
				try:
					xbmc.sleep(10)
					retry -= 1
					win.getControl(1).setLabel(heading)
					win.getControl(5).setText(text)
					quit()
					return
				except: pass
#######################################################################


		def movies(self, lite=False):
			self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
			self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')
			self.addDirectoryItem('Actor', 'moviePersons', 'actor.png', 'DefaultMovies.png')
			self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
			self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultMovies.png')
			self.addDirectoryItem('Box Office', 'movies&url=boxoffice', 'boxoffice2.png', 'DefaultMovies.png')
			self.addDirectoryItem('IMDB Public Lists', 'imdbLists', 'imdb.png', 'DefaultMovies.png')
			self.addDirectoryItem('1Click Movie', 'oneclick', 'oneclick.png', 'DefaultMovies.png')
			self.addDirectoryItem('IMDB Top 100', 'movies&url=top3', 'imdb.png', 'DefaultMovies.png')
			self.addDirectoryItem('IMDB Top 250', 'movies&url=top2', 'imdb.png', 'DefaultMovies.png')
			self.addDirectoryItem('IMDB Top 1000', 'movies&url=top4', 'imdb.png', 'DefaultMovies.png')
			self.addDirectoryItem('IMDB Best Director Winning', 'movies&url=bestd', 'imdb.png', 'DefaultMovies.png')
			self.addDirectoryItem('National Film Board Preserved ', 'movies&url=nfb', 'nfb.png', 'DefaultMovies.png')
			self.addDirectoryItem('Fox', 'movies&url=fox', 'fox.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Paramount', 'movies&url=para', 'para.png', 'DefaultTVShows.png')
			self.addDirectoryItem('MGM', 'movies&url=pmgm', 'mgm.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Disney', 'movies&url=disney1', 'dis.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Universal', 'movies&url=uni', 'uni.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Sony', 'movies&url=sony', 'sony.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Warner Bros', 'movies&url=warb', 'warb.png', 'DefaultTVShows.png')
			self.addDirectoryItem('IMDB Prime Video', 'movies&url=primev', 'imdb.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic', 'movies&url=classmov', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic Horror', 'movies&url=classhor', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic Fantasy', 'movies&url=classfant', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic Western', 'movies&url=classwest', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic Animation', 'movies&url=classani', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic War', 'movies&url=classwar', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic Sci-fi', 'movies&url=classsci', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Eighties', 'movies&url=eighties', 'Eighties.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Nineties', 'movies&url=nineties', 'Nineties.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Noughties', 'movies&url=noughties', 'Noughties.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Twenty Tens', 'movies&url=twentyten', 'TwentyTens.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Twenty Twenties', 'movies&url=twentytwo', 'twentytwenties.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
			self.addDirectoryItem('Actor Search', 'moviePerson', 'actorsearch.png', 'DefaultMovies.png')
			self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

		
			self.endDirectory()


		def mymovies(self, lite=False):
			self.accountCheck()

			if traktCredentials == True and imdbCredentials == True:
				self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
				self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))
				self.addDirectoryItem(32034, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)

			elif traktCredentials == True:
				self.addDirectoryItem(32032, 'movies&url=traktcollection', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktcollection'))
				self.addDirectoryItem(32033, 'movies&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png', queue=True, context=(32551, 'moviesToLibrary&url=traktwatchlist'))

			elif imdbCredentials == True:
				self.addDirectoryItem(32032, 'movies&url=imdbwatchlist', 'imdb.png', 'DefaultMovies.png', queue=True)
				self.addDirectoryItem(32033, 'movies&url=imdbwatchlist2', 'imdb.png', 'DefaultMovies.png', queue=True)

			if traktCredentials == True:
				self.addDirectoryItem(32035, 'movies&url=traktfeatured', 'trakt.png', 'DefaultMovies.png', queue=True)

			elif imdbCredentials == True:
				self.addDirectoryItem(32035, 'movies&url=featured', 'imdb.png', 'DefaultMovies.png', queue=True)

			if traktIndicators == True:
				self.addDirectoryItem(32036, 'movies&url=trakthistory', 'trakt.png', 'DefaultMovies.png', queue=True)

				self.addDirectoryItem(32039, 'movieUserlists', 'mymovies.png', 'DefaultMovies.png')
				self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
				self.addDirectoryItem('Actor Search', 'moviePerson', 'actorsearch.png', 'DefaultMovies.png')
				self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

				self.endDirectory()


		def tvshows(self, lite=False):
			self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
			self.addDirectoryItem('IMDB Prime Video', 'tvshows&url=usprime', 'imdb.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Documentaries', 'tvshows&url=docsa', 'documentaries.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Mystery', 'tvshows&url=myst', 'myst.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Sci-Fi', 'tvshows&url=scifi1', 'scifi.png', 'DefaultTVShows.png')
			self.addDirectoryItem('User Rating 7 to 10', 'tvshows&url=userr', 'rated.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Mini-Series', 'tvshows&url=mini', 'mini.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Classic', 'tvshows&url=classtv', 'classic.png', 'DefaultTVShows.png')
			self.addDirectoryItem('PG-PG13', 'tvshows&url=pg', 'pg.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Sci-Fi Animation', 'tvshows&url=scian', 'scifi.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Global Animation', 'tvshows&url=ani1', 'glob.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Reality TV', 'tvshows&url=rtv', 'real.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Walt Disney', 'tvshows&url=waltd', 'dis.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Dream Works', 'tvshows&url=dreamw', 'dream.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Sony', 'tvshows&url=sony3', 'sony.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Warner Bros', 'tvshows&url=warnerbro1', 'warb.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Universal', 'tvshows&url=uni1', 'uni.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Fox', 'tvshows&url=fox11', 'fox.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Paramount', 'tvshows&url=para4', 'para.png', 'DefaultTVShows.png')
			self.addDirectoryItem('MGM', 'tvshows&url=mgm5', 'mgm.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')
			self.addDirectoryItem('Actor Search', 'tvPerson', 'actorsearch.png', 'DefaultTVShows.png')
			self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

			self.endDirectory()


		def mytvshows(self, lite=False):
			self.accountCheck()

			if traktCredentials == True and imdbCredentials == True:
				self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
				self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))
				self.addDirectoryItem(32034, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')

			elif traktCredentials == True:
				self.addDirectoryItem(32032, 'tvshows&url=traktcollection', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktcollection'))
				self.addDirectoryItem(32033, 'tvshows&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png', context=(32551, 'tvshowsToLibrary&url=traktwatchlist'))

			elif imdbCredentials == True:
				self.addDirectoryItem(32032, 'tvshows&url=imdbwatchlist', 'imdb.png', 'DefaultTVShows.png')
				self.addDirectoryItem(32033, 'tvshows&url=imdbwatchlist2', 'imdb.png', 'DefaultTVShows.png')

			if traktCredentials == True:
				self.addDirectoryItem(32035, 'tvshows&url=traktfeatured', 'trakt.png', 'DefaultTVShows.png')

			elif imdbCredentials == True:
				self.addDirectoryItem(32035, 'tvshows&url=trending', 'imdb.png', 'DefaultMovies.png', queue=True)

			if traktIndicators == True:
				self.addDirectoryItem(32036, 'calendar&url=trakthistory', 'trakt.png', 'DefaultTVShows.png', queue=True)
				self.addDirectoryItem(32037, 'calendar&url=progress', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
				self.addDirectoryItem(32038, 'calendar&url=mycalendar', 'trakt.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)
				self.addDirectoryItem(32040, 'tvUserlists', 'mytvshows.png', 'DefaultTVShows.png')

			if traktCredentials == True:
				self.addDirectoryItem(32041, 'episodeUserlists', 'mytvshows.png', 'DefaultTVShows.png')
				self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
				self.addDirectoryItem('Actor Search', 'tvPerson', 'actorsearch.png', 'DefaultTVShows.png')
				self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

				self.endDirectory()

		def tmdb(self, lite=False):
			self.addDirectoryItem('TMDB Movies', 'TMDBMovies', 'movies.png', 'DefaultMovies.png')
			self.addDirectoryItem('TMDB TV Shows', 'TMDBShows', 'tvshows.png', 'DefaultTVShows.png')
		
			self.endDirectory()
	
		def TMDBMovies(self):

			self.addDirectoryItem('Trending', 'movies&url=trending', 'trending.png', 'playlist.png')
			self.addDirectoryItem('Popular', 'movies&url=popular', 'popular.png', 'playlist.png')
			self.addDirectoryItem('Anticipated', 'movies&url=anticipated', 'anticipated.png', 'playlist.png')
			self.addDirectoryItem('Box Office', 'movies&url=boxoffice2', 'boxoffice2.png', 'playlist.png')
			self.addDirectoryItem('Movie Mosts', 'movieMosts', 'mosts.png', 'playlist.png')
			self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')
			self.endDirectory()	

		def movieMosts(self):		

			self.addDirectoryItem('Most Played This Week', 'movies&url=played1', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Played This Month', 'movies&url=played2', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Played This Year', 'movies&url=played3', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Played All Time', 'movies&url=played4', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected This Week', 'movies&url=collected1', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected This Month', 'movies&url=collected2', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected This Year', 'movies&url=collected3', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected All Time', 'movies&url=collected4', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched This Week', 'movies&url=watched1', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched This Month', 'movies&url=watched2', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched This Year', 'movies&url=watched3', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched All Time', 'movies&url=watched4', 'mosts.png', 'playlist.png')


			self.endDirectory()	

		def TMDBShows(self):		

			self.addDirectoryItem('Trending', 'tvshows&url=trending', 'trending.png', 'playlist.png')
			self.addDirectoryItem('Popular', 'tvshows&url=popular', 'popular.png', 'playlist.png')
			self.addDirectoryItem('Anticipated', 'tvshows&url=anticipated', 'anticipated.png', 'playlist.png')
			self.addDirectoryItem('Show Premieres', 'tvshows&url=premieres', 'premieres.png', 'playlist.png')
			self.addDirectoryItem('TV Show Mosts', 'showMosts', 'mosts.png', 'playlist.png')
			self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')


			self.endDirectory()	

		def showMosts(self):		

			self.addDirectoryItem('Most Played This Week', 'tvshows&url=played1', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Played This Month', 'tvshows&url=played2', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Played This Year', 'tvshows&url=played3', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Played All Time', 'tvshows&url=played4', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected This Week', 'tvshows&url=collected1', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected This Month', 'tvshows&url=collected2', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected This Year', 'tvshows&url=collected3', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Collected All Time', 'tvshows&url=collected4', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched This Week', 'tvshows&url=watched1', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched This Month', 'tvshows&url=watched2', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched This Year', 'tvshows&url=watched3', 'mosts.png', 'playlist.png')
			self.addDirectoryItem('Most Watched All Time', 'tvshows&url=watched4', 'mosts.png', 'playlist.png')


			self.endDirectory()			
		
		def custom(self, lite=False):		

			self.addDirectoryItem('Anime', 'movies&url=anime', 'anime.png', 'playlist.png')
			self.addDirectoryItem('Avant Garde', 'movies&url=avant', 'avant.png', 'playlist.png')
			self.addDirectoryItem('Based On A True Story', 'movies&url=true', 'true.png', 'playlist.png')
			self.addDirectoryItem('Biker', 'movies&url=biker', 'biker.png', 'playlist.png')
			self.addDirectoryItem('B Movies', 'movies&url=bmovie', 'bmovie.png', 'playlist.png')
			self.addDirectoryItem('Breaking The Fourth Wall', 'movies&url=breaking', 'breaking.png', 'playlist.png')
			self.addDirectoryItem('Business', 'movies&url=business', 'business.png', 'playlist.png')
			self.addDirectoryItem('Capers', 'movies&url=caper', 'caper.png', 'playlist.png')
			self.addDirectoryItem('Car Chases', 'movies&url=car', 'chase.png', 'playlist.png')
			self.addDirectoryItem('Character Study', 'movies&url=char', 'character.png', 'playlist.png')
			self.addDirectoryItem('Chick Flix', 'movies&url=chick', 'chick.png', 'playlist.png')
			self.addDirectoryItem('Coming to Age', 'movies&url=coming', 'coming.png', 'playlist.png')
			self.addDirectoryItem('Competition', 'movies&url=competition', 'comps.png', 'playlist.png')
			self.addDirectoryItem('Cult', 'movies&url=cult', 'cult.png', 'playlist.png')
			self.addDirectoryItem('Cyberpunk', 'movies&url=cyber', 'cyber.png', 'playlist.png')
			self.addDirectoryItem('Drug Addiction', 'movies&url=drugs', 'drug.png', 'playlist.png')
			self.addDirectoryItem('Dystopia', 'movies&url=dystopia', 'dystopia.png', 'playlist.png')
			self.addDirectoryItem('Epic', 'movies&url=epic', 'epic.png', 'playlist.png')
			self.addDirectoryItem('Espionage', 'movies&url=espionage', 'espionage.png', 'playlist.png')
			self.addDirectoryItem('Experimental', 'movies&url=expiremental', 'experimental.png', 'playlist.png')
			self.addDirectoryItem('Existential', 'movies&url=Existential', 'exis.png', 'playlist.png')
			self.addDirectoryItem('Fairy Tale', 'movies&url=fairytale', 'fairytale.png', 'playlist.png')
			self.addDirectoryItem('Farce', 'movies&url=farce', 'farce.png', 'playlist.png')
			self.addDirectoryItem('Femme Fatale', 'movies&url=femme', 'femme.png', 'playlist.png')
			self.addDirectoryItem('Futuristic', 'movies&url=futuristic', 'futuristic.png', 'playlist.png')
			self.addDirectoryItem('Heist', 'movies&url=heist', 'heist.png', 'playlist.png')
			self.addDirectoryItem('High School', 'movies&url=highschool', 'highschool.png', 'playlist.png')
			self.addDirectoryItem('Horror Movie Remakes', 'movies&url=remakes', 'horror.png', 'playlist.png')
			self.addDirectoryItem('James Bond', 'movies&url=bond', 'bond.png', 'playlist.png')
			self.addDirectoryItem('Kidnapping', 'movies&url=kidnapped', 'kidnapped.png', 'playlist.png')
			self.addDirectoryItem('Kung Fu', 'movies&url=kungfu', 'kungfu.png', 'playlist.png')
			self.addDirectoryItem('Monster', 'movies&url=monster', 'monster.png', 'playlist.png')
			self.addDirectoryItem('Movie Box Sets', 'movies&url=box', 'boxsets.png', 'playlist.png')
			self.addDirectoryItem('Movie Loners', 'movies&url=loners', 'loner.png', 'playlist.png')
			self.addDirectoryItem('Movies & Racism', 'movies&url=racist', 'race.png', 'playlist.png')
			self.addDirectoryItem('Neo Noir', 'movies&url=neo', 'neo.png', 'playlist.png')
			self.addDirectoryItem('Parenthood', 'movies&url=parenthood', 'parenthood.png', 'playlist.png')
			self.addDirectoryItem('Parody', 'movies&url=parody', 'parody.png', 'playlist.png')
			self.addDirectoryItem('Post Apocalypse', 'movies&url=apocalypse', 'apocalypse.png', 'playlist.png')
			self.addDirectoryItem('Private Eye', 'movies&url=private', 'dick.png', 'playlist.png')
			self.addDirectoryItem('Remakes', 'movies&url=remake', 'remake.png', 'playlist.png')
			self.addDirectoryItem('Road Movies', 'movies&url=road', 'road.png', 'playlist.png')
			self.addDirectoryItem('Robots', 'movies&url=robot', 'robot.png', 'playlist.png')
			self.addDirectoryItem('Satire', 'movies&url=satire', 'satire.png', 'playlist.png')
			self.addDirectoryItem('Schizophrenia', 'movies&url=schiz', 'schiz.png', 'playlist.png')
			self.addDirectoryItem('Serial Killers', 'movies&url=serial', 'serial.png', 'playlist.png')
			self.addDirectoryItem('Slasher', 'movies&url=slasher', 'slasher.png', 'playlist.png')
			self.addDirectoryItem('Sleeper Hits', 'movies&url=sleeper', 'sleeper.png', 'playlist.png')
			self.addDirectoryItem('Spiritual', 'movies&url=spiritual', 'spiritual.png', 'playlist.png')
			self.addDirectoryItem('Spoofs', 'movies&url=spoof', 'spoof.png', 'playlist.png')
			self.addDirectoryItem('Star Wars', 'movies&url=star', 'starwars.png', 'playlist.png')
			self.addDirectoryItem('Steampunk', 'movies&url=steampunk', 'steampunk.png', 'playlist.png')
			self.addDirectoryItem('Superheros', 'movies&url=superhero', 'superhero.png', 'playlist.png')
			self.addDirectoryItem('Supernatural', 'movies&url=supernatural', 'supernatural.png', 'playlist.png')
			self.addDirectoryItem('Tech Noir', 'movies&url=tech', 'tech.png', 'playlist.png')
			self.addDirectoryItem('Time Travel', 'movies&url=time', 'time.png', 'playlist.png')
			self.addDirectoryItem('Vampires', 'movies&url=vampire', 'vampire.png', 'playlist.png')
			self.addDirectoryItem('Virtual Reality', 'movies&url=vr', 'vr.png', 'playlist.png')
			self.addDirectoryItem('Wilhelm Scream', 'movies&url=wilhelm', 'wilhelm.png', 'playlist.png')
			self.addDirectoryItem('Zombies', 'movies&url=zombie', 'zombie.png', 'playlist.png')
			self.addDirectoryItem('New Years', 'movies&url=newyear', 'newyear.png', 'season.png')
			self.addDirectoryItem('Easter', 'movies&url=easter', 'easter.png', 'season.png')
			self.addDirectoryItem('Halloween', 'movies&url=halloween', 'halloween.png', 'season.png')
			self.addDirectoryItem('Thanksgiving', 'movies&url=thanx', 'thanksgiving.png', 'season.png')
			self.addDirectoryItem('Christmas', 'movies&url=xmass', 'christmas.png', 'season.png')
			self.addDirectoryItem('DC', 'movies&url=dc', 'dc.png', 'playlist.png')
			self.addDirectoryItem('Disney and Pixar', 'movies&url=disney', 'disney.png', 'playlist.png')
			self.addDirectoryItem('Marvel Universe', 'movies&url=marvel', 'marvel.png', 'playlist.png')

			self.endDirectory()		


		def playlist(self, lite=False):		
			self.addDirectoryItem('I Love The 80s', 'movies&url=eighties', 'Eighties.png', 'playlist.png')
			self.addDirectoryItem('IMDB Top 1000', 'movies&url=thousand', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Top Gangster Movies', 'movies&url=gangster', 'gangster.png', 'playlist.png')
			self.addDirectoryItem('Top Action Movies 60-99', 'movies&url=action2', 'action.png', 'playlist.png')
			self.addDirectoryItem('Greatest Horror Films of All Time', 'movies&url=horror2', 'horror.png', 'playlist.png')
			self.addDirectoryItem('Greatest Sci-Fi Films of All Time', 'movies&url=scifi', 'scifi.png', 'playlist.png')
			self.addDirectoryItem('Greatest Westerns of All Time', 'movies&url=western', 'western.png', 'playlist.png')
			self.addDirectoryItem('Top Cop Movies', 'movies&url=cop', 'cop.png', 'playlist.png')
			self.addDirectoryItem('Greatest War Movies', 'movies&url=war', 'war.png', 'playlist.png')
			self.addDirectoryItem('Great Movies Directed By Women', 'movies&url=women', 'women.png', 'playlist.png')
			self.addDirectoryItem('Greatest Political Movies', 'movies&url=political', 'political.png', 'playlist.png')
			self.addDirectoryItem('The Most Romantic Movies', 'movies&url=romance', 'romance.png', 'playlist.png')

			self.endDirectory()		
	

		def imdbLists(self):		

			self.addDirectoryItem('Greatest Movies: 2000-2017', 'movies&url=imdb1', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Horror Movie Series', 'movies&url=imdb2', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Horror Of The Skull Posters', 'movies&url=imdb3', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Top Satirical Movies', 'movies&url=imdb4', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Greatest Science Fiction', 'movies&url=imdb5', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Famous and Infamous Movie Couples', 'movies&url=imdb6', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Top Private Eye Movies', 'movies&url=imdb7', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Sleeper Hit Movies', 'movies&url=imdb8', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Cult Horror Movies', 'movies&url=imdb9', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Heist Caper Movies', 'movies&url=imdb10', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Artificial Intelligence', 'movies&url=imdb11', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Stephen King Movies and Adaptations', 'movies&url=imdb12', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Alien Invasion', 'movies&url=imdb13', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Contract Killers', 'movies&url=imdb14', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Heroic Bloodshed', 'movies&url=imdb15', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Conspiracy', 'movies&url=imdb16', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Top Kung Fu', 'movies&url=imdb17', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Movies Based In One Room', 'movies&url=imdb18', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Movies For Intelligent People', 'movies&url=imdb19', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Inspirational Movies', 'movies&url=imdb20', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Tech Geeks', 'movies&url=imdb21', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Movie Clones', 'movies&url=imdb22', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Obscure Underrated Movies', 'movies&url=imdb23', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Smut and Trash', 'movies&url=imdb24', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Revenge', 'movies&url=imdb25', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Motivational', 'movies&url=imdb26', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Disaster & Apocalyptic', 'movies&url=imdb27', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Music or Musical Movies', 'movies&url=imdb28', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Mental, Physical Illness and Disability Movies', 'movies&url=imdb29', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Best Twist Ending Movies', 'movies&url=imdb30', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Heists, Cons, Scams & Robbers', 'movies&url=imdb31', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Road Trip & Travel', 'movies&url=imdb32', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Spy - CIA - MI5 - MI6 - KGB', 'movies&url=imdb33', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Prison & Escape', 'movies&url=imdb34', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Courtroom', 'movies&url=imdb35', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Father - Son', 'movies&url=imdb36', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Based on a True Story', 'movies&url=imdb37', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Man Vs. Nature', 'movies&url=imdb38', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Gangster', 'movies&url=imdb39', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Teenage', 'movies&url=imdb40', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Old Age', 'movies&url=imdb41', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Serial Killers', 'movies&url=imdb42', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Addiction', 'movies&url=imdb43', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Time Travel', 'movies&url=imdb44', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Puff Puff Pass', 'movies&url=imdb45', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Artists , Painters , Writers', 'movies&url=imdb46', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Love', 'movies&url=imdb47', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Winter Is Here', 'movies&url=imdb48', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Suicide', 'movies&url=imdb49', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Alchoholic', 'movies&url=imdb50', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Video Games', 'movies&url=imdb51', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Shocking Movie Scenes', 'movies&url=imdb52', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Biographical', 'movies&url=imdb53', 'imdb.png', 'playlist.png')
			self.addDirectoryItem('Movies to Teach You a Thing or Two', 'movies&url=imdb54', 'imdb.png', 'playlist.png')


			self.endDirectory()	

		def iptv(self):
			self.addDirectoryItem('AllTV', 'alltv', 'networks.png', 'fanart.png')
			self.addDirectoryItem('CinemaTV', 'cinematv', 'networks.png', 'fanart.png')
			self.addDirectoryItem('FaithTV', 'faithtv', 'networks.png', '')
			self.addDirectoryItem('LodgeTV', 'lodgetv', 'networks.png', '')
			self.addDirectoryItem('MyTV',  'mytv',  'networks.png',  'DefaultTVShows.png')
			self.addDirectoryItem('RadioTV', 'radiotv', 'networks.png', '')
			self.endDirectory()

		def oneclickmovies(self):
			self.addDirectoryItem('1 Click', '1click', 'debrid.png', 'debrid.png')  
			self.addDirectoryItem('1080p Movies', '1kmovies', '1k.png', 'DefaultMovies.png')
			self.addDirectoryItem('Dolby Digital Movies', 'dtsmovies', 'dts.png', 'debrid.png')  
			self.addDirectoryItem('4k Movies', '4kmovies', '4k.png', 'DefaultMovies.png')
			self.addDirectoryItem('4K RD', 'vipclick', '4krd.png', 'DefaultMovies.png')
			self.addDirectoryItem('4k Hero', 'nlmovie', '4khero.png', 'debrid.png')  
			self.addDirectoryItem('More 1 Click', 'nltvshow', 'oneclick.png', 'debrid.png')  
			self.addDirectoryItem('kids', 'kids', 'kidscorner.png', 'kidscorner.png')  
			self.endDirectory()
		
		def tools(self):
			self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32361, 'authTrakt', 'tools.png', 'DefaultAddonProgram.png')

			self.endDirectory()

		def library(self):
			self.addDirectoryItem(32557, 'openSettings&query=4.0', 'tools.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32558, 'updateLibrary&query=tool', 'library_update.png', 'DefaultAddonProgram.png')
			self.addDirectoryItem(32559, control.setting('library.movie'), 'movies.png', 'DefaultMovies.png', isAction=False)
			self.addDirectoryItem(32560, control.setting('library.tv'), 'tvshows.png', 'DefaultTVShows.png', isAction=False)

			if trakt.getTraktCredentialsInfo():
				self.addDirectoryItem(32561, 'moviesToLibrary&url=traktcollection', 'trakt.png', 'DefaultMovies.png')
				self.addDirectoryItem(32562, 'moviesToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultMovies.png')
				self.addDirectoryItem(32563, 'tvshowsToLibrary&url=traktcollection', 'trakt.png', 'DefaultTVShows.png')
				self.addDirectoryItem(32564, 'tvshowsToLibrary&url=traktwatchlist', 'trakt.png', 'DefaultTVShows.png')

				self.endDirectory()

		def downloads(self):
			movie_downloads = control.setting('movie.download.path')
			tv_downloads = control.setting('tv.download.path')

			if len(control.listDir(movie_downloads)[0]) > 0:
				self.addDirectoryItem(32001, movie_downloads, 'movies.png', 'DefaultMovies.png', isAction=False)
			if len(control.listDir(tv_downloads)[0]) > 0:
				self.addDirectoryItem(32002, tv_downloads, 'tvshows.png', 'DefaultTVShows.png', isAction=False)

			self.endDirectory()


		def search(self):
			self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
			self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')
			self.addDirectoryItem('Actor Search', 'moviePerson', 'actorsearch.png', 'DefaultMovies.png')
			self.addDirectoryItem('TV Actor Search', 'tvPerson', 'actorsearch.png', 'DefaultTVShows.png')

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


