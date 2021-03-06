# -*- coding: utf-8 -*-
"""
    default.py --- totally Addon entry point
    Copyright (C) 2017, totally

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
"""
import __builtin__

# CONFIGURATION VARIABLES
# -----------------------
# change these to suit your addons
import base64
import __builtin__
root_xml_url = base64.b64decode(b"aHR0cDovL3N1cHJlbWFjeS5vcmcudWsvVGh1bmRlclN0cnVjay90b3RhbGx5L3RvdGFsbHkueG1s")
__builtin__.tvdb_api_key = base64.b64decode(b"RTc0NzREMEY2MjlFNDhGQw==")
__builtin__.tmdb_api_key = base64.b64decode(b"YzU3N2RlMDc3OGYyYmEzMzg0NmVjNTAwMzMzMmRiYjY=")
__builtin__.trakt_client_id = base64.b64decode(b"ZGIzMGUwZTQxYzUzMDM4YjRkZDY1YjJhZDdjMDNlZjBiMmUyODZjYzQ1YjEzZGI3ZGM1ZjQ0OTZhYmI5Mjk1Yw==")
__builtin__.trakt_client_secret = base64.b64decode(b"OTE3YzA1NDU2ZmY0M2I2OTI3OTk4ZjUyY2Q3NTE5ZTFkNWY2MGFjZWJhMDNlOGVlMDgxZTFmYWEyMzI0Y2Y1NQ==")
__builtin__.search_db_location = ""  # location of search db

import os
import sys

import koding
import koding.router as router
import resources.lib.search
import resources.lib.sources
import resources.lib.testings
import resources.lib.util.info
import xbmc
import xbmcaddon
import xbmcplugin
from koding import route
from resources.lib.util.xml import totallyList, display_list
import resources.lib.util.views
from resources.lib.plugins import *
from language import get_string as _
from resources.lib.plugin import run_hook


addon_id = xbmcaddon.Addon().getAddonInfo('id')
addon_name = xbmcaddon.Addon().getAddonInfo('name')
home_folder = xbmc.translatePath('special://home/')
addon_folder = os.path.join(home_folder, 'addons')
art_path = os.path.join(addon_folder, addon_id)
content_type = "files"


@route("main")
def root():
    """root menu of the addon"""
    if not get_list(root_xml_url):
        koding.Add_Dir(
            name=_("Message"),
            url=_("Sorry, server is down"),
            mode="message",
            folder=True,
            icon=xbmcaddon.Addon().getAddonInfo("icon"),
            fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
            content_type="")
        koding.Add_Dir(
            name=_("Search"),
            url="",
            mode="Search",
            folder=True,
            icon=xbmcaddon.Addon().getAddonInfo("icon"),
            fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
            content_type="")
        koding.Add_Dir(
            name=_("Testings"),
            url='{"file_name":"testings.xml"}',
            mode="Testings",
            folder=True,
            icon=xbmcaddon.Addon().getAddonInfo("icon"),
            fanart=xbmcaddon.Addon().getAddonInfo("fanart"),
            content_type="")


@route(mode='get_list_uncached', args=["url"])
def get_list_uncached(url):
    """display totally list uncached"""
    global content_type
    totally_list = totallyList(url, cached=False)
    if not totally_list:
        koding.dolog(_("returned empty for ") + url)
    items = totally_list.get_list()
    content = totally_list.get_content_type()
    if items == []:
        return False
    if content:
        content_type = content
    display_list(items, content_type)
    return True


@route(mode="get_list", args=["url"])
def get_list(url):
    """display totally list"""
    global content_type
    totally_list = totallyList(url)
    if not totally_list:
        koding.dolog(_("returned empty for ") + url)
    items = totally_list.get_list()
    content = totally_list.get_content_type()
    if items == []:
        return False
    if content:
        content_type = content
    display_list(items, content_type)
    return True


@route(mode="all_episodes", args=["url"])
def all_episodes(url):
    global content_type
    import pickle
    import xbmcgui
    season_urls = pickle.loads(url)
    result_items = []
    dialog = xbmcgui.DialogProgress()
    dialog.create(addon_name, _("Loading items"))
    num_urls = len(season_urls)
    for index, season_url in enumerate(season_urls):
        if dialog.iscanceled():
            break
        percent = ((index + 1) * 100) / num_urls
        dialog.update(percent, _("processing lists"), _("%s of %s") % (
            index + 1,
            num_urls))

        totally_list = totallyList(season_url)
        result_items.extend(totally_list.get_list(skip_dialog=True))
    content_type = "episodes"
    display_list(result_items, "episodes")


@route(mode="Settings")
def settings():
    xbmcaddon.Addon().openSettings()


@route(mode="ScraperSettings")
def scraper_settings():
    xbmcaddon.Addon('script.module.universalscrapers').openSettings()


@route(mode="ResolverSettings")
def resolver_settings():
    xbmcaddon.Addon('script.module.resolveurl').openSettings()


@route(mode="ClearTraktAccount")
def clear_trakt_account():
    import xbmcgui
    if xbmcgui.Dialog().yesno(addon_name, "{0} Trakt {1}. {2}".format(_("Delete"), _("Settings").lower(), _("Are you sure?"))):
        xbmcaddon.Addon().setSetting("TRAKT_EXPIRES_AT", "")
        xbmcaddon.Addon().setSetting("TRAKT_ACCESS_TOKEN", "")
        xbmcaddon.Addon().setSetting("TRAKT_REFRESH_TOKEN", "")


@route(mode="message", args=["url"])
def show_message(message):
    import xbmcgui
    if len(message) > 80:
        koding.Text_Box(addon_name, message)
    else:
        xbmcgui.Dialog().ok(addon_name, message)


@route('clearCache')
def clear_cache():
    import xbmcgui
    dialog = xbmcgui.Dialog()
    if dialog.yesno(addon_name, _("Clear Metadata?")):
        koding.Remove_Table("meta")
        koding.Remove_Table("episode_meta")
    if dialog.yesno(addon_name, _("Clear Scraper Cache?")):
        import universalscrapers
        universalscrapers.clear_cache()
    if dialog.yesno(addon_name, _("Clear GIF Cache?")):
        dest_folder = os.path.join(
            xbmc.translatePath(xbmcaddon.Addon().getSetting("cache_folder")),
            "artcache")
        koding.Delete_Folders(dest_folder)
    xbmc.log("running hook:", xbmc.LOGNOTICE)
    run_hook("clear_cache")


def get_addon_url(mode, url=""):
    import urllib
    result = sys.argv[0] + "?mode=%s" % mode

    if url:
        result += "&url=%s" % urllib.quote_plus(url)
    return result


def first_run_wizard():
    result = run_hook("first_run_wizard")
    if result:
        return


# koding.User_Info()
if xbmcaddon.Addon().getSetting("first_run") == "true":
    first_run_wizard()

foldername = xbmc.getInfoLabel("Container.FolderName")
if foldername in ["", "plugin.program.super.favourites"]:
    __builtin__.totally_WIDGET = True
else:
    __builtin__.totally_WIDGET = False

xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_NONE)
xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)

router.Run()

xbmcplugin.endOfDirectory(int(sys.argv[1]), cacheToDisc=False)
try:
    content_type = __builtin__.content_type
except:
    pass
if not xbmcaddon.Addon().getSetting("first_run") == "true":
    if content_type == "files":
        content_type = "other"
    resources.lib.util.views.set_list_view_mode(content_type)
