import sys
import os
import urllib
import urlparse
import utility
from skystreaming.skystreaming import Skystreaming
from skystreaming.exception.authentication_error import AuthenticationError
from skystreaming.exception.account_error import AccountError

import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmc


ADDON = xbmcaddon.Addon()
HANDLE = int(sys.argv[1])
BASEURL = sys.argv[0]
ARGS = urlparse.parse_qs(sys.argv[2][1:])
ADDON_ID = ADDON.getAddonInfo('id')

xbmcplugin.setContent(HANDLE, 'movies')

# create the addon data directory if not exists
addon_data_dir = os.path.join(xbmc.translatePath('special://userdata/addon_data').decode('utf-8'), ADDON_ID)
if not os.path.exists(addon_data_dir):
    os.makedirs(addon_data_dir)

# create playlist file
playlists_file = os.path.join(addon_data_dir, 'playLists.txt')


def build_url(query):
    """build the plugin url"""
    return BASEURL + '?' + urllib.urlencode(query)


def ok(title, message, message2=None, message3=None):
    """show the ok dialog"""
    dlg = xbmcgui.Dialog()
    dlg.ok(title, message, message2, message3)


def notify(message):
    """show the notification"""
    time = 5000  # in miliseconds
    addon_name = ADDON.getAddonInfo('name')
    addon_icon = ADDON.getAddonInfo('icon')
    xbmc.executebuiltin('Notification(%s, %s, %d, %s)' % (addon_name, message, time, addon_icon))


def log(msg):
    """log a message"""
    xbmc.log('SKYSTREAMING: %s' % msg, xbmc.LOGERROR)


def fetch_playlist():
    """fetch the Skystreaming playlist"""
    skystreaming = Skystreaming()

    if not ADDON.getSetting('email') or not ADDON.getSetting('password'):
        notify(ADDON.getLocalizedString(11004))
        ADDON.openSettings()
        return None

    try:
        skystreaming.login(ADDON.getSetting('email'), ADDON.getSetting('password'))
        playlist = skystreaming.get_playlist()
        channels_list = utility.m3u2list(playlist)
        utility.save_list(playlists_file, channels_list)
        return playlist
    except AuthenticationError as e:
        log(e.http_message)
        notify(ADDON.getLocalizedString(11001))
    except AccountError as e:
        log(e.message)
        notify(ADDON.getLocalizedString(11002))


def list_channels():
    """show channels on the kodi list."""
    playlist = utility.read_list(playlists_file)

    if not playlist:
        ok(ADDON.getLocalizedString(11005), ADDON.getLocalizedString(11006))
        return None

    for channel in playlist:
        url = channel['url'].encode('utf-8')
        name = channel['display_name'].encode('utf-8')
        action_url = build_url({'mode': 'play', 'url': url, 'name': name})
        item = xbmcgui.ListItem(name, iconImage='DefaultVideo.png')
        item.setInfo(type='Video', infoLabels={'Title': name})
        xbmcplugin.addDirectoryItem(handle=HANDLE, url=action_url, listitem=item)

    xbmcplugin.endOfDirectory(HANDLE, cacheToDisc=False)


def play_channel(url, name):
    """play a channel"""
    item = xbmcgui.ListItem(name, iconImage='DefaultVideo.png')
    item.setInfo(type='Video', infoLabels={'Title': name})
    xbmc.Player().play(url, item)


def start():
    """start the plugin"""
    mode = ARGS.get('mode', None)
    if mode is None:
        fetch_playlist()
        list_channels()
    elif mode[0] == 'play':
        play_channel(ARGS.get('url')[0], ARGS.get('name')[0])
