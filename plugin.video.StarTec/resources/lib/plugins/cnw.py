"""

    Copyright (C) 2018 MuadDib

    ----------------------------------------------------------------------------
    "THE BEER-WARE LICENSE" (Revision 42):
    @tantrumdev wrote this file.  As long as you retain this notice you
    can do whatever you want with this stuff. If we meet some day, and you think
    this stuff is worth it, you can buy him a beer in return. - Muad'Dib
    ----------------------------------------------------------------------------

    Changelog:
        2018.6.29:
            - Added caching to primary menus (Cache time is 3 hours)


"""

import __builtin__
import base64,time
import json,re,requests,os,traceback,urlparse
import koding
import xbmc,xbmcaddon,xbmcgui
from koding import route
from resources.lib.plugin import Plugin
from resources.lib.util import dom_parser
from resources.lib.util.context import get_context_items
from resources.lib.util.xml import JenItem, JenList, display_list
from unidecode import unidecode

CACHE_TIME = 10800  # change to wanted cache time in seconds

addon_fanart = xbmcaddon.Addon().getAddonInfo('fanart')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
next_icon = os.path.join(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')), 'resources', 'media', 'next.png')

User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'

class CNW(Plugin):
    name = "cnw"

    def process_item(self, item_xml):
        if "<cnw>" in item_xml:
            item = JenItem(item_xml)
            if "http" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "PlayCNW",
                    'url': item.get("cnw", ""),
                    'folder': False,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "category/" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Cat",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "recent" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Cat",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "popular" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Cat",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "pornstar" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_ShowStarVids",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            elif "search" in item.get("cnw", ""):
                result_item = {
                    'label': item["title"],
                    'icon': item.get("thumbnail", addon_icon),
                    'fanart': item.get("fanart", addon_fanart),
                    'mode': "CNW_Stars",
                    'url': item.get("cnw", ""),
                    'folder': True,
                    'imdb': "0",
                    'content': "files",
                    'season': "0",
                    'episode': "0",
                    'info': {},
                    'year': "0",
                    'context': get_context_items(item),
                    "summary": item.get("summary", None)
                }
            result_item['fanart_small'] = result_item["fanart"]
            return result_item


@route(mode='CNW_Cat', args=["url"])
def category_cnw(url):
    url = url.replace('category/', '')
    url = urlparse.urljoin('http://www.celebsnudeworld.com/', url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            headers = {'User_Agent':User_Agent}
            html = requests.get(url,headers=headers).content
            
            cat_divs = dom_parser.parseDOM(html, 'ul', attrs={'class':'videos'})[0]
            vid_entries = dom_parser.parseDOM(cat_divs, 'li')
            for vid_section in vid_entries:
                thumbnail = urlparse.urljoin('http://www.celebsnudeworld.com/', re.compile('src="(.+?)"',re.DOTALL).findall(str(vid_section))[0])
                vid_page_url, title = re.compile('href="(.+?)"\stitle="(.+?)"',re.DOTALL).findall(str(vid_section))[0]
                vid_page_url = urlparse.urljoin('http://www.celebsnudeworld.com/', vid_page_url)
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <meta>"\
                       "        <summary>%s</summary>"\
                       "    </meta>"\
                       "    <cnw>%s</cnw>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,title,vid_page_url,thumbnail)

            try:
                try:
                    next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[1]
                except:
                    next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[0]
                next_page = next_page.replace('/', '', 1)
                xml += "<dir>"\
                       "    <title>Next Page</title>"\
                       "    <meta>"\
                       "        <summary>Click here for more porn bitches!</summary>"\
                       "    </meta>"\
                       "    <cnw>category/%s</cnw>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</dir>" % (next_page,next_icon)
            except:
                pass
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='CNW_ShowStarVids', args=["url"])
def pornstar_vids_cnw(url):
    url = url.replace('category/', '')
    url = urlparse.urljoin('http://www.celebsnudeworld.com/', url)

    xml = fetch_from_db(url)
    if not xml:
        xml = ""
        try:
            xml += "<dir>"\
                   "    <title>Celebs Nude World Home</title>"\
                   "    <meta>"\
                   "        <summary>Go back to the CNW main menu</summary>"\
                   "    </meta>"\
                   "    <link>file://adult/cnw/main.xml</link>"\
                   "</dir>"

            headers = {'User_Agent':User_Agent}
            html = requests.get(url,headers=headers).content
            
            cat_divs = dom_parser.parseDOM(html, 'ul', attrs={'class':'videos'})[0]
            vid_entries = dom_parser.parseDOM(cat_divs, 'li')
            for vid_section in vid_entries:
                thumbnail = urlparse.urljoin('http://www.celebsnudeworld.com/', re.compile('src="(.+?)"',re.DOTALL).findall(str(vid_section))[0])
                vid_page_url, title = re.compile('href="(.+?)"\stitle="(.+?)"',re.DOTALL).findall(str(vid_section))[0]
                vid_page_url = urlparse.urljoin('http://www.celebsnudeworld.com/', vid_page_url)
                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <meta>"\
                       "        <summary>%s</summary>"\
                       "    </meta>"\
                       "    <cnw>%s</cnw>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,title,vid_page_url,thumbnail)

            try:
                try:
                    next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[1]
                except:
                    next_page = dom_parser.parseDOM(html, 'a', attrs={'class':'prevnext'}, ret='href')[0]
                next_page = next_page.replace('/', '', 1)
                xml += "<dir>"\
                       "    <title>Next Page</title>"\
                       "    <meta>"\
                       "        <summary>Click here for more porn bitches!</summary>"\
                       "    </meta>"\
                       "    <cnw>category/%s</cnw>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</dir>" % (next_page,next_icon)
            except:
                pass
        except:
            pass

    jenlist = JenList(xml)
    display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='CNW_Stars', args=["url"])
def pornstars_cnw(url):
    xml = ""
    try:
        keyboard = xbmc.Keyboard('', 'Search for')
        keyboard.doModal()
        if keyboard.isConfirmed() != None and keyboard.isConfirmed() != "":
            search = keyboard.getText()
        else:
            return

        if search == None or search == "":
            xml += "<item>"\
                   "    <title>Search Cancelled</title>"\
                   "    <heading></heading>"\
                   "    <thumbnail>%s</thumbnail>"\
                   "</item>" % (addon_icon)
            jenlist = JenList(xml)
            display_list(jenlist.get_list(), jenlist.get_content_type())
            return

        total = 0

        try:
            search_url = 'http://www.celebsnudeworld.com/search/pornstar/?s=%s' % search.replace(' ', '+')
            html = requests.get(search_url).content
            results = dom_parser.parseDOM(html, 'div', attrs={'class':'model'})

            if len(results) == 0:
                dialog = xbmcgui.Dialog()
                dialog.ok('Search Results', 'Search Results are empty')
                return
            for star in results:
                thumbnail = urlparse.urljoin('http://www.celebsnudeworld.com/', re.compile('src="(.+?)"',re.DOTALL).findall(str(star))[0])
                vid_page_url, title = re.compile('href="(.+?)"\stitle="(.+?)"',re.DOTALL).findall(str(star))[0]

                xml += "<item>"\
                       "    <title>%s</title>"\
                       "    <meta>"\
                       "        <summary>%s</summary>"\
                       "    </meta>"\
                       "    <cnw>%s</cnw>"\
                       "    <thumbnail>%s</thumbnail>"\
                       "</item>" % (title,title,vid_page_url,thumbnail)
                total += 1
        except:
            pass
    except:
        pass

    if total > 0:
        jenlist = JenList(xml)
        display_list(jenlist.get_list(), jenlist.get_content_type())


@route(mode='PlayCNW', args=["url"])
def play_cnw(url):
    try:
        headers = {'User_Agent':User_Agent}
        vid_html = requests.get(url,headers=headers).content
        qualities = re.compile('label="(.+?)"',re.DOTALL).findall(str(vid_html))

        selected = xbmcgui.Dialog().select('Select Quality',qualities)
        if selected ==  -1:
            return        

        vid_url = re.compile('source src="(.+?)"\stype=".+?"\slabel="%s"' % (qualities[selected]),re.DOTALL).findall(str(vid_html))[0]
        xbmc.executebuiltin("PlayMedia(%s)" % vid_url)
    except:
        return


def save_to_db(item, url):
    if not item or not url:
        return False
    try:
        koding.reset_db()
        koding.Remove_From_Table(
            "cnw_com_plugin",
            {
                "url": url
            })

        koding.Add_To_Table("cnw_com_plugin",
                            {
                                "url": url,
                                "item": base64.b64encode(item),
                                "created": time.time()
                            })
    except:
        return False


def fetch_from_db(url):
    koding.reset_db()
    cnw_plugin_spec = {
        "columns": {
            "url": "TEXT",
            "item": "TEXT",
            "created": "TEXT"
        },
        "constraints": {
            "unique": "url"
        }
    }
    koding.Create_Table("cnw_com_plugin", cnw_plugin_spec)
    match = koding.Get_From_Table(
        "cnw_com_plugin", {"url": url})
    if match:
        match = match[0]
        if not match["item"]:
            return None
        created_time = match["created"]
        if created_time and float(created_time) + CACHE_TIME >= time.time():
            match_item = match["item"]
            try:
                result = base64.b64decode(match_item)
            except:
                return None
            return result
        else:
            return
    else:
        return 


def remove_non_ascii(text):
    return unidecode(text)

