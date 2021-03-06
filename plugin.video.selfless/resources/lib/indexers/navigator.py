# -*- coding: utf-8 -*-
################################################################################
# |                                                                            #
# |    Selfless Live                                                           #
# |    Copyright (C) 2018 Kodi Ghost                                           #
# |                                                                            #
# |    This program is free software: you can redistribute it and/or modify    #
# |    it under the terms of the GNU General Public License as published by    #
# |    the Free Software Foundation, either version 3 of the License, or       #
# |    (at your option) any later version.                                     #
# |                                                                            #
# |    This program is distributed in the hope that it will be useful,         #
# |    but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# |    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# |    GNU General Public License for more details.                            #
# |                                                                            #
################################################################################

import os,sys,urlparse

from resources.lib.modules import control
from resources.lib.modules import trakt

sysaddon = sys.argv[0] ; syshandle = int(sys.argv[1]) ; control.moderator()

artPath = control.artPath() ; addonFanart = control.addonFanart()

imdbCredentials = False if control.setting('imdb.user') == '' else True

traktCredentials = trakt.getTraktCredentialsInfo()

traktIndicators = trakt.getTraktIndicatorsInfo()

queueMenu = control.lang(32065).encode('utf-8')

ua = control.setting('useramount')

class navigator:
    def root(self):
        self.addDirectoryItem(32001, 'movieNavigator', 'movies.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvNavigator', 'tvshows.png', 'DefaultTVShows.png')

        if not control.setting('lists.widget') == '0':
            self.addDirectoryItem(32003, 'mymovieNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32004, 'mytvNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

        if not control.setting('movie.widget') == '0':
            self.addDirectoryItem(32005, 'movieWidget', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')

        if (traktIndicators == True and not control.setting('tv.widget.alt') == '0') or (traktIndicators == False and not control.setting('tv.widget') == '0'):
            self.addDirectoryItem(32006, 'tvWidget', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png')

        self.addDirectoryItem(32007, 'channels', 'channels.png', 'DefaultMovies.png')

        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')

        downloads = True if control.setting('downloads') == 'true' and (len(control.listDir(control.setting('movie.download.path'))[0]) > 0 or len(control.listDir(control.setting('tv.download.path'))[0]) > 0) else False
        if downloads == True:
            self.addDirectoryItem(32009, 'downloadNavigator', 'downloads.png', 'DefaultFolder.png')

        self.addDirectoryItem(32010, 'searchNavigator', 'search.png', 'DefaultFolder.png')

        self.endDirectory()


    def movies(self, lite=False):
        self.addDirectoryItem( '[B][COLOR cyan]Welcome to SelfLess Movie Section[/COLOR][/B]','useramount', 'in-theaters.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem( '[B][COLOR cyan]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32022, 'movies&url=theaters', 'in-theaters.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32005, 'movies&url=featured', 'latest-movies.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32017, 'movies&url=trending', 'people-watching.png', 'DefaultRecentlyAddedMovies.png')
        self.addDirectoryItem(32018, 'movies&url=popular', 'most-popular.png', 'DefaultMovies.png')
        self.addDirectoryItem(32019, 'movies&url=views', 'most-voted.png', 'DefaultMovies.png')
        self.addDirectoryItem(32020, 'movies&url=boxoffice', 'box-office.png', 'DefaultMovies.png')
        self.addDirectoryItem( '[B][COLOR red]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem('Holiday Movies', 'holidayNavigator', 'season.jpg', 'DefaultMovies.jpg')
        self.addDirectoryItem('Selfless Playlists', 'customNavigator', 'playlist.jpg', 'DefaultMovies.jpg')
        self.addDirectoryItem(32620, 'boxsetsNavigator', 'boxsets.png', 'boxsets.png')		
        self.addDirectoryItem( '[B][COLOR white]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')		
        self.addDirectoryItem(32011, 'movieGenres', 'genres.png', 'DefaultMovies.png')
        self.addDirectoryItem(32012, 'movieYears', 'years.png', 'DefaultMovies.png')

        #self.addDirectoryItem(32014, 'movieLanguages', 'languages.png', 'DefaultMovies.png')


        self.addDirectoryItem(32021, 'movies&url=oscars', 'oscar-winners.png', 'DefaultMovies.png')
        self.addDirectoryItem( '[B][COLOR cyan]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32003, 'mymovieliteNavigator', 'mymovies.png', 'DefaultVideoPlaylists.png')
            self.addDirectoryItem(32029, 'moviePerson', 'people-search.png', 'DefaultMovies.png')			
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem( '[B][COLOR cyan]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')
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

        self.addDirectoryItem(32039, 'movieUserlists', 'userlists.png', 'DefaultMovies.png')

        if lite == False:
            self.addDirectoryItem(32031, 'movieliteNavigator', 'movies.png', 'DefaultMovies.png')
            self.addDirectoryItem(32010, 'movieSearch', 'search.png', 'DefaultMovies.png')

        self.endDirectory()



    def tvshows(self, lite=False):
        self.addDirectoryItem( '[B][COLOR cyan]Welcome to SelfLess TV Show Section[/COLOR][/B]','useramount', 'networks.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem( '[B][COLOR cyan]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32026, 'tvshows&url=premiere', 'new-tvshows.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32006, 'calendar&url=added', 'latest-episodes.png', 'DefaultRecentlyAddedEpisodes.png', queue=True)

        self.addDirectoryItem(32017, 'tvshows&url=trending', 'people-watching.png', 'DefaultRecentlyAddedEpisodes.png')
        self.addDirectoryItem(32018, 'tvshows&url=popular', 'most-popular.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32023, 'tvshows&url=rating', 'highly-rated.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32019, 'tvshows&url=views', 'most-voted.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32024, 'tvshows&url=airing', 'airing-today.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32027, 'calendars', 'calendar.png', 'DefaultRecentlyAddedEpisodes.png')
        #self.addDirectoryItem(32014, 'tvLanguages', 'languages.png', 'DefaultTVShows.png')
        self.addDirectoryItem( '[B][COLOR cyan]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32011, 'tvGenres', 'genres.png', 'DefaultTVShows.png')
        self.addDirectoryItem(32016, 'tvNetworks', 'networks.png', 'DefaultTVShows.png')

        #self.addDirectoryItem(32025, 'tvshows&url=active', 'returning-tvshows.png', 'DefaultTVShows.png')

        self.addDirectoryItem( '[B][COLOR cyan]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        if lite == False:
            if not control.setting('lists.widget') == '0':
                self.addDirectoryItem(32004, 'mytvliteNavigator', 'mytvshows.png', 'DefaultVideoPlaylists.png')

            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')
        self.addDirectoryItem( '[B][COLOR cyan]=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=[/COLOR][/B]','null', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32008, 'toolNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.endDirectory()

##Stoped
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

        self.addDirectoryItem(32040, 'tvUserlists', 'userlists.png', 'DefaultTVShows.png')

        if traktCredentials == True:
            self.addDirectoryItem(32041, 'episodeUserlists', 'userlists.png', 'DefaultTVShows.png')

        if lite == False:
            self.addDirectoryItem(32031, 'tvliteNavigator', 'tvshows.png', 'DefaultTVShows.png')
            self.addDirectoryItem(32010, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()


    def tools(self):
        #self.addDirectoryItem(32043, 'openSettings&query=0.0', 'tools.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32044, 'openSettings&query=3.1', 'tools.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32045, 'openSettings&query=1.0', 'tools.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32046, 'openSettings&query=6.0', 'tools.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32047, 'openSettings&query=2.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32556, 'libraryNavigator', 'tools.png', 'DefaultAddonProgram.png')
        #self.addDirectoryItem(32048, 'openSettings&query=5.0', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32049, 'viewsNavigator', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32050, 'clearSources', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32604, 'clearCacheSearch', 'tools.png', 'DefaultAddonProgram.png')
        self.addDirectoryItem(32052, 'clearCache', 'tools.png', 'DefaultAddonProgram.png')

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
		
    def custom(self, lite=False):
        self.addDirectoryItem('Action Hero', 'movies&url=action3', 'playlist.jpg', 'playlist.jpg')	
        self.addDirectoryItem('Anime', 'movies&url=anime', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Anti Hero', 'movies&url=action3', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Apocalypse', 'movies&url=apocalypse', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Animated', 'movies&url=animated', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Artifical Intelligence ', 'movies&url=ai', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Avant Garde', 'movies&url=avant', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Based On A True Story', 'movies&url=true', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Biker', 'movies&url=biker', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('B Movies', 'movies&url=bmovie', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Breaking The Fourth Wall', 'movies&url=breaking', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Business', 'movies&url=business', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Capers', 'movies&url=caper', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Car Chases', 'movies&url=car', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Chase Movies', 'movies&url=chase', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Chick Flix', 'movies&url=chick', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('College', 'movies&url=college', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Coming of Age', 'movies&url=coming', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Competition', 'movies&url=competition', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Conspiracy', 'movies&url=conspiracy', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Cult', 'movies&url=cult', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Cyberpunk', 'movies&url=cyber', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Dark Hero', 'movies&url=darkhero', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('DC', 'movies&url=dc', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Disney and Pixar', 'movies&url=disney', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Drug Addiction', 'movies&url=drugs', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Dystopia', 'movies&url=dystopia', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Epic', 'movies&url=epic', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Espionage', 'movies&url=espionage', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Experimental', 'movies&url=expiremental', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Existential', 'movies&url=Existential', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Fairy Tale', 'movies&url=fairytale', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Farce', 'movies&url=farce', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Femme Fatale', 'movies&url=femme', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Film Noir', 'movies&url=noir', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Futuristic', 'movies&url=futuristic', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Good vs Evil', 'movies&url=goodvbad', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Heist', 'movies&url=heist', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Heroic Bloodshed', 'movies&url=blood', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('High School', 'movies&url=highschool', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Horror Movie Remakes', 'movies&url=remakes', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Inside The Mind', 'movies&url=char', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('In your Dreams', 'movies&url=dreamworks', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('James Bond', 'movies&url=bond', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Kidnapping', 'movies&url=kidnapped', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Kung Fu', 'movies&url=kungfu', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Marvel Cinematic Universe', 'movies&url=marvel', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Monster', 'movies&url=monster', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Movie Loners', 'movies&url=loners', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Movies & Racism', 'movies&url=racist', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Neo Noir', 'movies&url=neo', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Parenthood', 'movies&url=parenthood', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Parody', 'movies&url=parody', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Post Apocalypse', 'movies&url=apocalypse', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Private Eye', 'movies&url=private', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Psychopath', 'movies&url=psychopath', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Remakes', 'movies&url=remake', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Reboots', 'movies&url=reboot', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Road Movies', 'movies&url=road', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Robots', 'movies&url=robot', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Satire', 'movies&url=satire', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Sexy Movies', 'movies&url=sexy', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('Schizophrenia', 'movies&url=schiz', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Serial Killers', 'movies&url=serial', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Slasher', 'movies&url=slasher', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Spiritual', 'movies&url=spiritual', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Spoofs', 'movies&url=spoof', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Star Wars', 'movies&url=star', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Steampunk', 'movies&url=steampunk', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Superheros', 'movies&url=superhero', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Supernatural', 'movies&url=supernatural', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Swashbuckler', 'movies&url=swashbuckler', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Tech Noir', 'movies&url=tech', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Time Travel', 'movies&url=time', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Vampires', 'movies&url=vampire', 'playlist.jpg', 'playlist.jpg')
        self.addDirectoryItem('Virtual Reality', 'movies&url=vr', 'playlist.jpg', 'playlist.jpg')		
        self.addDirectoryItem('World Cinema', 'movies&url=world', 'playlist.jpg', 'playlist.jpg')        
        self.addDirectoryItem('Wilhelm Scream', 'movies&url=wilhelm', 'playlist.jpg', 'playlist.jpg')	
        self.addDirectoryItem('Zombies', 'movies&url=zombie', 'playlist.jpg', 'playlist.jpg')
		
		
        self.endDirectory()		

    def holiday(self, lite=False):		
        self.addDirectoryItem('New Years', 'movies&url=newyear', 'season.jpg', 'season.jpg')
        self.addDirectoryItem('Easter', 'movies&url=easter', 'season.jpg', 'season.jpg')
        self.addDirectoryItem('Halloween', 'movies&url=halloween', 'season.jpg', 'season.jpg')
        self.addDirectoryItem('Thanks Giving', 'movies&url=thanx', 'season.jpg', 'season.jpg')		
        self.addDirectoryItem('Christmas', 'movies&url=xmass', 'season.jpg', 'season.jpg')

        self.endDirectory()		

    def search(self):
        self.addDirectoryItem(32001, 'movieSearch', 'search.png', 'DefaultMovies.png')
        self.addDirectoryItem(32002, 'tvSearch', 'search.png', 'DefaultTVShows.png')

        self.endDirectory()
		
    def sortby(self):
        try:
            control.idle()
            items = [ ('Popularity', 'moviemeter'),  ('Alphabetical', 'alpha'), ('IMDb Rating', 'user_rating'), ('Number of Votes', 'num_votes'), ('US Box Office by Gross', 'boxoffice_gross_us'), ('By Year', 'year'), ('By Release Date', 'release_date') ]
            select = control.selectDialog([i[0] for i in items], 'Sort Lists By')
            if select == -1: return
            items =  items[select][1]
            control.setSetting('uservar','%s' % items)
            control.refresh()
        except:
            return

    def listamount(self):
        try:
            control.idle()
            items = [ ('10', '10'),  ('20', '20'), ('30', '30'), ('40', '40'), ('50', '50'), ('60', '60'), ('70', '70'), ('80', '80'), ('90', '90'), ('100', '100') ]
            select = control.selectDialog([i[0] for i in items], 'Items per Page')
            if select == -1: return
            items =  items[select][1]
            control.setSetting('useramount','%s' % items)
            control.refresh()
        except:
            return


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

            from resources.lib.addon import views
            views.setView(content, {})
        except:
            return


    def accountCheck(self):
        if traktCredentials == False and imdbCredentials == False:
            control.idle()
            control.infoDialog(control.lang(32042).encode('utf-8'), sound=True, icon='WARNING')
            sys.exit()


    def infoCheck(self, version):
        try:
            control.infoDialog('www.tvaddons.ag', control.lang(32074).encode('utf-8'), time=5000, sound=False)
            return '1'
        except:
            return '1'


    def clearCache(self):
        control.idle()
        yes = control.yesnoDialog(control.lang(32056).encode('utf-8'), '', '')
        if not yes: return
        from resources.lib.addon import cache
        cache.cache_clear()
        control.infoDialog(control.lang(32057).encode('utf-8'), sound=True, icon='INFO')
		
    def clearCacheSearch(self):
        control.idle()
        if control.yesnoDialog(control.lang(32056).encode('utf-8'), '', ''):
            control.setSetting('tvsearch', '')
            control.setSetting('moviesearch', '')
            control.refresh()		


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


