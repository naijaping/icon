# ------------------------------------------------------------
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Stefano Thegroove 360
# Copyright 2018 https://stefanoaddon.info
#
# Distribuito sotto i termini di GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------- -----------
# Questo file fa parte di Stefano Thegroove 360.
#
# Stefano Thegroove 360 ​​è un software gratuito: puoi ridistribuirlo e / o modificarlo
# è sotto i termini della GNU General Public License come pubblicata da
# la Free Software Foundation, o la versione 3 della licenza, o
# (a tua scelta) qualsiasi versione successiva.
#
# Stefano Thegroove 360 ​​è distribuito nella speranza che possa essere utile,
# ma SENZA ALCUNA GARANZIA; senza nemmeno la garanzia implicita di
# COMMERCIABILITÀ o IDONEITÀ PER UN PARTICOLARE SCOPO. Vedere il
# GNU General Public License per maggiori dettagli.
#
# Dovresti aver ricevuto una copia della GNU General Public License
# insieme a Stefano Thegroove 360. In caso contrario, vedi <http://www.gnu.org/licenses/>.
# ------------------------------------------------- -----------
# Client for Stefano Thegroove 360
# ------------------------------------------------------------


import os
import re

import xbmc
import xbmcaddon
import xbmcgui

PLUGIN_NAME = "Stefano"

__settings__ = xbmcaddon.Addon(id="plugin.video." + PLUGIN_NAME)
__language__ = __settings__.getLocalizedString



def get_platform(full_version=False):
    """
        Devuelve la información la version de xbmc o kodi sobre el que se ejecuta el plugin

        @param full_version: indica si queremos toda la informacion o no
        @type full_version: bool
        @rtype: str o dict
        @return: Si el paramentro full_version es True se retorna un diccionario con las siguientes claves:
            'num_version': (float) numero de version en formato XX.X
            'name_version': (str) nombre clave de cada version
            'video_db': (str) nombre del archivo que contiene la base de datos de videos
            'plaform': (str) esta compuesto por "kodi-" o "xbmc-" mas el nombre de la version segun corresponda.
        Si el parametro full_version es False (por defecto) se retorna el valor de la clave 'plaform' del diccionario anterior.
        """

    ret = {}
    codename = {"10": "dharma", "11": "eden", "12": "frodo",
                "13": "gotham", "14": "helix", "15": "isengard",
                "16": "jarvis", "17": "krypton", "18": "leia"}
    code_db = {'10': 'MyVideos37.db', '11': 'MyVideos60.db', '12': 'MyVideos75.db',
               '13': 'MyVideos78.db', '14': 'MyVideos90.db', '15': 'MyVideos93.db',
               '16': 'MyVideos99.db', '17': 'MyVideos107.db', '18': 'MyVideos108.db'}

    num_version = xbmc.getInfoLabel('System.BuildVersion')
    num_version = re.match("\d+\.\d+", num_version).group(0)
    ret['name_version'] = codename.get(num_version.split('.')[0], num_version)
    ret['video_db'] = code_db.get(num_version.split('.')[0], "")
    ret['num_version'] = float (num_version)
    if ret['num_version'] < 14:
        ret['platform'] = "xbmc-" + ret['name_version']
    else:
        ret['platform'] = "kodi-" + ret['name_version']

    if full_version:
        return ret
    else:
        return ret['platform']


def is_xbmc():
    return True


def get_library_support():
    return True


def get_system_platform():
    """ fonction: pour recuperer la platform que xbmc tourne """
    platform = "unknown"
    if xbmc.getCondVisibility("system.platform.linux"):
        platform = "linux"
    elif xbmc.getCondVisibility("system.platform.xbox"):
        platform = "xbox"
    elif xbmc.getCondVisibility("system.platform.windows"):
        platform = "windows"
    elif xbmc.getCondVisibility("system.platform.osx"):
        platform = "osx"
    return platform


def get_all_settings_addon():
    # Lee el archivo settings.xml y retorna un diccionario con {id: value}
    import scrapertools

    infile = open(os.path.join(get_data_path(),"settings.xml"), "r")
    data = infile.read()
    infile.close()

    ret = {}
    matches = scrapertools.find_multiple_matches(data, '<setting id="([^"]*)" value="([^"]*)')
    settings_types = get_settings_types()

    for id, value in matches:
        ret[id] = get_setting(id)

    return ret


def open_settings():
    settings_pre = get_all_settings_addon()
    __settings__.openSettings()
    settings_post = get_all_settings_addon()

    # cb_validate_config (util para validar cambios realizados en el cuadro de dialogo)
    if settings_post.get('adult_aux_intro_password', None):
        # Hemos accedido a la seccion de Canales para adultos
        from platformcode import platformtools
        if not 'adult_password' in settings_pre:
            adult_password = set_setting('adult_password', '1111')
        else:
            adult_password = settings_pre['adult_password']


        if settings_post['adult_aux_intro_password'] == adult_password:
            # La contraseña de acceso es correcta

            # Cambio de contraseña
            if settings_post['adult_aux_new_password1']:
                if settings_post['adult_aux_new_password1'] == settings_post['adult_aux_new_password2']:
                    adult_password = set_setting('adult_password', settings_post['adult_aux_new_password1'])
                else:
                    platformtools.dialog_ok("Canale per adulti", "I campi 'Nuova password' e 'Conferma nuova password' non corrispondono.",
                                            "Rientrare in 'Preferenze' per cambiare la password")


            # Fijar adult_pin
            adult_pin = ""
            if settings_post["adult_request_password"] == "true":
                adult_pin = adult_password
            set_setting("adult_pin", adult_pin)

        else:
            platformtools.dialog_ok("Canale per adulti", "La password non è corretta.",
                                    "Le modifiche apportate in questa sezione non vengono salvate.")

            # Deshacer cambios
            set_setting("adult_mode", settings_pre.get("adult_mode","0"))
            set_setting("adult_request_password", settings_pre.get("adult_request_password", "true"))


        # Borramos settings auxiliares
        set_setting('adult_aux_intro_password', '')
        set_setting('adult_aux_new_password1', '')
        set_setting('adult_aux_new_password2', '')


def get_setting(name, channel="", server=""):
    """
    Retorna el valor de configuracion del parametro solicitado.

    Devuelve el valor del parametro 'name' en la configuracion global o en la configuracion propia del canal 'channel'.

    Si se especifica el nombre del canal busca en la ruta \addon_data\plugin.video.streamondemand\settings_channels el archivo channel_data.json
    y lee el valor del parametro 'name'. Si el archivo channel_data.json no existe busca en la carpeta channels el archivo 
    channel.xml y crea un archivo channel_data.json antes de retornar el valor solicitado.
    Si el parametro 'name' no existe en channel_data.json lo busca en la configuracion global y si ahi tampoco existe devuelve un str vacio.

    Parametros:
    name -- nombre del parametro
    channel [opcional] -- nombre del canal

    Retorna:
    value -- El valor del parametro 'name'

    """

    # Specific channel setting
    if channel:

        # logger.info("config.get_setting reading channel setting '"+name+"' from channel xml")
        from core import channeltools
        value = channeltools.get_channel_setting(name, channel)
        # logger.info("config.get_setting -> '"+repr(value)+"'")

        return value

    elif server:
        # logger.info("config.get_setting reading server setting '"+name+"' from server xml")
        from core import servertools
        value = servertools.get_server_setting(name, server)
        # logger.info("config.get_setting -> '"+repr(value)+"'")

        return value

    # Global setting
    else:
        # logger.info("config.get_setting reading main setting '"+name+"'")
        value = __settings__.getSetting(name)

        # Translate Path if start with "special://"
        if value.startswith("special://") and "librarypath" not in name:
            value = xbmc.translatePath(value)

        # hack para devolver el tipo correspondiente
        settings_types = get_settings_types()

        if settings_types.get(name) in ['enum', 'number']:
            value = int(value)

        elif settings_types.get(name) == 'bool':
            value = value == 'true'

        elif not settings_types.has_key(name):
            try:
                t = eval (value)
                value = t[0](t[1])
            except:
                value = None

        return value


def set_setting(name, value, channel="", server=""):
    """
    Fija el valor de configuracion del parametro indicado.

    Establece 'value' como el valor del parametro 'name' en la configuracion global o en la configuracion propia del
    canal 'channel'.
    Devuelve el valor cambiado o None si la asignacion no se ha podido completar.

    Si se especifica el nombre del canal busca en la ruta \addon_data\plugin.video.streamondemand\settings_channels el archivo channel_data.json
    y establece el parametro 'name' al valor indicado por 'value'. Si el archivo channel_data.json no existe busca en la carpeta channels el archivo 
    channel.xml y crea un archivo channel_data.json antes de modificar el parametro 'name'.
    Si el parametro 'name' no existe lo añade, con su valor, al archivo correspondiente.


    Parametros:
    name -- nombre del parametro
    value -- valor del parametro
    channel [opcional] -- nombre del canal

    Retorna:
    'value' en caso de que se haya podido fijar el valor y None en caso contrario

    """
    if channel:
        from core import channeltools
        return channeltools.set_channel_setting(name, value, channel)
    elif server:
        from core import servertools
        return servertools.set_server_setting(name, value, server)
    else:
        try:
            settings_types = get_settings_types()

            if settings_types.get(name) == 'bool':
                if value:
                    new_value = "true"
                else:
                    new_value = "false"

            elif settings_types.get(name):
                new_value = str(value)

            else:
                if isinstance(value,basestring):
                    new_value = "(%s, %s)" % (type(value).__name__, repr(value))

                else:
                    new_value = "(%s, %s)" % (type(value).__name__, value)

            __settings__.setSetting(name, new_value)

        except:
            return None

        return value


def get_settings_types():
    """
    Devuelve un diccionario con los parametros (key) de la configuracion global y sus tipos (value)

    :return: dict 
    """
    WIN10000 = xbmcgui.Window(10000)
    settings_types = WIN10000.getProperty(PLUGIN_NAME + "_settings_types")

    if not settings_types:
        infile = open(os.path.join(get_runtime_path(), "resources", "settings.xml"))
        data = infile.read()
        infile.close()

        matches = re.findall('<setting id="([^"]*)" type="([^"]*)', data)
        settings_types = "{%s}" % ",".join("'%s': '%s'" % tup for tup in matches)

        WIN10000.setProperty(PLUGIN_NAME + "_settings_types", settings_types)

    return eval(settings_types)


def get_localized_string(code):
    dev = __language__(code)

    try:
        dev = dev.encode("utf-8")
    except:
        pass

    return dev


def get_library_config_path():
    value = get_setting("librarypath")
    if value == "":
        verify_directories_created()
        value = get_setting("librarypath")
    return value


def get_library_path():
    return xbmc.translatePath(get_library_config_path())


def get_temp_file(filename):
    return xbmc.translatePath(os.path.join("special://temp/", filename))


def get_runtime_path():
    return xbmc.translatePath(__settings__.getAddonInfo('Path'))


def get_data_path():
    dev = xbmc.translatePath(__settings__.getAddonInfo('Profile'))

    #Crea el directorio si no existe
    if not os.path.exists(dev):
        os.makedirs(dev)

    return dev


def get_cookie_data():
    import os
    ficherocookies = os.path.join(get_data_path(), 'cookies.dat')

    cookiedatafile = open(ficherocookies, 'r')
    cookiedata = cookiedatafile.read()
    cookiedatafile.close()

    return cookiedata


# Test if all the required directories are created
def verify_directories_created():
    from core import logger
    from core import filetools
    from platformcode import xbmc_library

    config_paths = [["librarypath",      "library"],
                    ["downloadpath",     "downloads"],
                    ["downloadlistpath", "downloads/list"],
                    ["settings_path",    "settings_channels"]]

    for path, default in config_paths:
        saved_path = get_setting(path)

        # Biblioteca
        if path == "librarypath":
            #set_setting("library_version", "v5")
            if not saved_path:
                saved_path = xbmc_library.search_library_path()
                if saved_path:
                    set_setting(path, saved_path)

        if not saved_path:
            saved_path = "special://profile/addon_data/plugin.video." + PLUGIN_NAME + "/" + default
            set_setting(path, saved_path)


        if get_setting("library_set_content")== True and path in ["librarypath","downloadpath"]:
            # logger.debug("library_set_content %s" % get_setting("library_set_content"))
            xbmc_library.add_sources(saved_path)

        saved_path = xbmc.translatePath(saved_path)
        if not filetools.exists(saved_path):
            logger.debug("Creating %s: %s" % (path, saved_path))
            filetools.mkdir(saved_path)


    config_paths = [["folder_movies", "CINE"],
                    ["folder_tvshows", "SERIES"]]

    for path, default in config_paths:
        saved_path = get_setting(path)

        if not saved_path:
            saved_path = default
            set_setting(path, saved_path)

        content_path = filetools.join(get_library_path(), saved_path)
        if not filetools.exists(content_path):
            logger.debug("Creating %s: %s" % (path, content_path))
            if filetools.mkdir(content_path) and get_setting("library_set_content")== True:
                xbmc_library.set_content(default)

        elif get_setting("library_ask_set_content") == 2:
            xbmc_library.set_content(default)

    try:
        from core import scrapertools
        # Buscamos el archivo addon.xml del skin activo
        skindir = filetools.join(xbmc.translatePath("special://home"), 'addons', xbmc.getSkinDir(),
                                 'addon.xml')
        # Extraemos el nombre de la carpeta de resolución por defecto
        folder = ""
        data = filetools.read(skindir)
        res = scrapertools.find_multiple_matches(data, '(<res .*?>)')
        for r in res:
            if 'default="true"' in r:
                folder = scrapertools.find_single_match(r, 'folder="([^"]+)"')
                break

        # Comprobamos si existe en pelisalacarta y sino es así, la creamos
        default = filetools.join(get_runtime_path(), 'resources', 'skins', 'Default')
        if folder and not filetools.exists(filetools.join(default, folder)):
            filetools.mkdir(filetools.join(default, folder))

        # Copiamos el archivo a dicha carpeta desde la de 720p si éste no existe o si el tamaño es diferente
        if folder and folder != '720p':
            for root, folders, files in filetools.walk(filetools.join(default, '720p')):
                for f in files:
                    if not filetools.exists(filetools.join(default, folder, f)) or \
                          (filetools.getsize(filetools.join(default, folder, f)) != 
                           filetools.getsize(filetools.join(default, '720p', f))):
                        filetools.copy(filetools.join(default, '720p', f),
                                       filetools.join(default, folder, f),
                                       True)
    except:
        import traceback
        logger.error("Al comprobar o crear la carpeta de resolución")
        logger.error(traceback.format_exc())
