import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import os

import util, tvestadao

ADDON_ID = 'plugin.video.tvestadao'

addon = xbmcaddon.Addon(id=ADDON_ID)
addon_dir = xbmc.translatePath( addon.getAddonInfo('path') )
fanart = addon.getAddonInfo('path') + '/fanart.jpg'
print fanart

# Get Settings
USER_AGENT = addon.getSetting('user_agent')
#THUMBNAIL_SIZE = addon.getSetting('thumbnail_size')
THUMBNAIL_SIZE = '300'

# Parse parameters
parameters = util.parseParameters()

if 'v' in parameters:
    tvestadao.playVideo(USER_AGENT, parameters)
elif 'f' in parameters:
    tvestadao.listVideos(USER_AGENT, THUMBNAIL_SIZE, parameters, fanart, addon.getLocalizedString(30005))
elif 's' in parameters:
    if 'q' not in parameters:
        dialog = xbmcgui.Dialog()
        searchText = dialog.input('Enter search string', type=xbmcgui.INPUT_ALPHANUM)
    else:
        searchText = parameters['q']
    tvestadao.doSearch(USER_AGENT, THUMBNAIL_SIZE, parameters, searchText, fanart, addon.getLocalizedString(30005))
else:
    tvestadao.buildMenu(USER_AGENT, fanart, addon.getLocalizedString(30004))
# Ends list of items for xbmc
util.endListing()
