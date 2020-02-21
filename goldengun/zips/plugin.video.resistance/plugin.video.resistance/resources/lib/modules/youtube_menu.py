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

import sys
import re
import urllib2

from resources.lib.modules import control

syshandle = int(sys.argv[1])


class youtube_menu(object):
	def __init__(self):
		self.agent = 'VGFudHJ1bUFkZG9uQWdlbnQ='.decode('base64')
		self.key_id = 'QUl6YVN5QTU2ckhCQXlLMENsMFA0dURNXzEyc05Pd1VtQWFhczhF'.decode('base64')


	def openMenuFile(self, menuFile):
		req = urllib2.Request(menuFile)
		req.add_header('User-Agent', self.agent)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link


	def processMenuFile(self, menuFile):
		link = self.openMenuFile(menuFile).replace('\n','').replace('\r','')
		match = re.compile('name="(.+?)".+?ection="(.+?)".+?earch="(.+?)".+?ubid="(.+?)".+?laylistid="(.+?)".+?hannelid="(.+?)".+?ideoid="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
		return match


	def addMenuItem(self, name, action, subid, iconimage, fanart, description='', isFolder=True):
		u = sys.argv[0] + "?action=" + action + "&subid=" + subid
		liz = control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setInfo(type='video', infoLabels={'title': name, 'plot': description})
		liz.setProperty('Fanart_Image', fanart)
		control.addItem(handle=syshandle, url=u, listitem=liz, isFolder=isFolder)


	def addSectionItem(self, name, iconimage, fanart):
		u = sys.argv[0] + "?action=sectionItem"
		liz = control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
		liz.setProperty('Fanart_Image', fanart)
		control.addItem(handle=syshandle, url=u, listitem=liz, isFolder=False)


	def addSearchItem(self, name, search_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/kodion/search/query/?q=%s" % search_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addChannelItem(self, name, channel_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/channel/%s/" % channel_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addUserItem(self, name, channel_id, icon, fanart):
		user = channel_id
		work_url = "plugin://plugin.video.youtube/user/%s/" % user
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addPlaylistItem(self, name, playlist_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/playlist/%s/" % playlist_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=True)


	def addVideoItem(self, name, video_id, icon, fanart):
		work_url = "plugin://plugin.video.youtube/play/?video_id=%s" % video_id
		liz = control.item(name)
		liz.setInfo( type='video', infoLabels={'title': name})
		liz.setArt({'thumb': icon, 'banner': 'DefaultVideo.png', 'fanart': fanart})
		liz.setProperty('IsPlayable', 'true')
		control.addItem(handle=syshandle, url=work_url, listitem=liz, isFolder=False)

