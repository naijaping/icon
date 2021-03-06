# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# TheGroove360 - XBMC Plugin
# Canale cinemastreaming
# ------------------------------------------------------------

import re
import urlparse

from core import httptools
from core import scrapertools
from core import servertools
from core.item import Item
from core.tmdb import infoSod
from lib.unshortenit import unshorten_only
from platformcode import logger

__channel__ = "cinemastreaming"

host = "https://cinemastreaming.info"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("[thegroove360.cinemastreaming] mainlist")

    # Main options
    itemlist = [Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]Film[/COLOR]",
                     url="%s/film/" % host,
                     extra="movie",
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Categorie[/COLOR]",
                     url=host,
                     extra="movie",
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="paesi",
                     title="[COLOR azure]Paesi[/COLOR]",
                     url=host,
                     extra="movie",
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca Film...[/COLOR]",
                     extra="movie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search"),
                Item(channel=__channel__,
                     action="peliculas_tv",
                     title="[COLOR azure]SerieTV[/COLOR]",
                     url="%s/serie-tv/" % host,
                     extra="movie",
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="search",
                     title="[COLOR yellow]Cerca Serie...[/COLOR]",
                     url=host,
                     extra="serie",
                     thumbnail="http://dc467.4shared.com/img/fEbJqOum/s7/13feaf0c8c0/Search")]

    return itemlist


def peliculas(item):
    logger.info("[thegroove360.cinemastreaming] peliculas")
    itemlist = []

    # Carica la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti
    patron = '<article id.*\s.*<a href="(.*?)".*\s.*\s.*src="(.*?)".*\s.*\s.*?Title">(.*?)<'
    matches = re.compile(patron, re.IGNORECASE).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 contentType="movie",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,
                 plot=scrapedplot,
                 extra=item.extra,
                 viewmode="movie_with_plot"), tipo='movie'))

    next_page = scrapertools.find_single_match(data,'<a class="next page-numbers" href="(.*?)">')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist


def peliculas_tv(item):
    logger.info("[thegroove360.cinemastreaming] peliculas")
    itemlist = []

    # Carica la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti
    patron = 'class="TPost C">.*\s.*?<a href="(.*?)">.*\s.*\s.*\s.*?src="(.*?)".*\s.*\s.*\s.*?<h3 class="Title">(.*?)<'
    matches = re.compile(patron, re.IGNORECASE).findall(data)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedplot = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="episodios",
                 contentType="episode",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail,

                 plot=scrapedplot,
                 extra=item.extra,
                 viewmode="movie_with_plot"), tipo='tv'))

    next_page = scrapertools.find_single_match(data,'<a class="next page-numbers" href="(.*?)">')

    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas_tv",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url=next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))

    return itemlist

def episodios(item):
    logger.info("Stefano.cinemastreaming peliculas_tv")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data
    bloque = scrapertools.get_match(data, '<main>(.*?)</main>')

    # Estrae i contenuti 
    patron = '<td class="MvTbTtl"><a href="([^"]+)">(.*?)<'
    matches = re.compile(patron, re.DOTALL).findall(bloque)

    for scrapedurl, scraped2 in matches:
        scrapedplot = ""
        scrapedthumbnail = ""
        scrapedtitle = scrapedurl
        scrapedtitle = scrapedtitle.replace(host, "")
        scrapedtitle = scrapedtitle.replace("episode", "")
        scrapedtitle = scrapedtitle.replace("/", "").title()
        scrapedtitle = scrapedtitle + " " + scraped2

        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 title=scrapedtitle,
                 fulltitle=scrapedtitle,
                 url=scrapedurl,
                 thumbnail=scrapedthumbnail), tipo="tv"))

    return itemlist

def categorie(item):
    logger.info("[thegroove360.cinemastreaming] categorie")
    itemlist = []

    # Carica la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti
    bloque = scrapertools.get_match(data, 'Categorie</a><ul class="sub-menu">(.*?)</ul>')
    patronvideos = '<li id="menu-item-.*?category.*?<a href="([^"]+)">([^"]+)</a></li>'
    matches = re.compile(patronvideos, re.DOTALL).finditer(bloque)

    for match in matches:
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        scrapedtitle = urlparse.urljoin(item.url, match.group(2))
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=match.group(2),
                 url=match.group(1),
                 thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png",
                 folder=True))

    return itemlist


def paesi(item):
    logger.info("[thegroove360.cinemastreaming] paesi")
    itemlist = []

    if item.url == "":
        item.url = host

    # Carica la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    # Estrae i contenuti
    patronvideos = '<li id="menu-item-.*?country.*?<a href="([^"]+)">([^"]+)</a></li>'
    matches = re.compile(patronvideos, re.DOTALL).finditer(data)

    for match in matches:
        scrapedurl = urlparse.urljoin(item.url, match.group(1))
        scrapedtitle = urlparse.urljoin(item.url, match.group(2))
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title=match.group(2),
                 url=match.group(1),
                 thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png",
                 folder=True))

    return itemlist


def listserie(item):
    # da implementare
    return None


def findvideos(item):
    logger.info("[thegroove360.cinemastreaming] findvideos")

    # Carica la pagina
    data = httptools.downloadpage(item.url, headers=headers).data

    urls = set()
    if 'trdownload' in data:
        data = data.replace("&#038;", "&")
        for url in scrapertools.find_multiple_matches(data,
                                                      r'href="(https://www\.cinemastreaming\.pw/\?trdownload[^"]+?)"'):
            while True:
                loc = httptools.downloadpage(url, follow_redirects=False).headers.get("location", "")
                if not loc:
                    break
                url = loc

            url, c = unshorten_only(url, 'adfly')
            urls.add(url)

    itemlist = servertools.find_video_items(data=str(urls) + data)

    for videoitem in itemlist:
        videoitem.title = "".join([item.title, '[COLOR green][B]' + videoitem.title + '[/B][/COLOR]'])
        videoitem.fulltitle = item.fulltitle
        videoitem.show = item.show
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist

def search(item, texto):
    logger.info("[thegroove360.cinemastreaming] " + item.url + " search " + texto)
    item.url = host + "/?s=" + texto
    try:
        if item.extra == "movie":
            return peliculas(item)
        if item.extra == "serie":
            return peliculas_tv(item)
    # Continua la ricerca in caso di errore 
    except:
        import sys
        for line in sys.exc_info():
            logger.error("%s" % line)
        return []
