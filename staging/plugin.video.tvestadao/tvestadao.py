import sys, urllib, urllib2
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import util
import re

import CommonFunctions

WEB_PAGE_BASE='http://tv.estadao.com.br'
SEARCH_URL_BEGIN='http://tv.estadao.com.br/videos-busca?q='
SEARCH_URL_END=''
THUMB_URL_BEGIN='/thumbs/'
THUMB_URL_END='/resources/jpg/'
XML_URL_BEGIN='http://front.multimidia.estadao.com.br/ESTA/swf/data/pt/video-player/video/'
SWF_URL='http://front.multimidia.estadao.com.br/ESTA/swf/ACTPlayer.swf'
PAGE_NUM_PARAM_BEGIN='pagina='
PAGE_NUM_PARAM_END= '#maisVideos'

def createItemURI(itemName):
    if len(itemName) >= 6:
        strURI = itemName[len(itemName)-1] + '/' + itemName[len(itemName)-2] + '/' + itemName[len(itemName)-3] + '/' + itemName[len(itemName)-4] + '/' + itemName
    else:
        strURI = itemName
    return strURI

def extractItemIdFromURL(inURL):
    URLparts = []
    URLparts = inURL.split(',')
    if len(URLparts) > 1:
        return URLparts[len(URLparts)-1]
    else:
        return ''
    
def playVideo(userAgent, params):
    common = CommonFunctions
    url = params['v']
    headers = { 'User-Agent' : userAgent, 'Content-Type' : 'text/html;charset=utf-8' }
    req2 = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req2)
    if response and response.getcode() == 200:
        content = response.read()
        videoTitle = common.parseDOM(content, name = "title", ret = False)
        videoLink = common.parseDOM(content, name = "file", ret = False)
        videoThumb = common.parseDOM(content, name = "image", ret = False)
        util.playMedia(videoTitle[0], videoThumb[0], videoLink[0], 'Video')
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to get video information' % (params['v']))

def resizeThumb(origThumbURL, thumbSize):
    return re.sub( THUMB_URL_BEGIN + '[0-9]+' + THUMB_URL_END, THUMB_URL_BEGIN + thumbSize + THUMB_URL_END, origThumbURL)

def doSearch (userAgent, thumbSize, params, searchString, fanart=None, nextPageString='NEXT PAGE'):
    common = CommonFunctions
    if 'p' in params:
        page = params['p']
    else:
        page = 1
    url = SEARCH_URL_BEGIN + searchString + SEARCH_URL_END + '&' + PAGE_NUM_PARAM_BEGIN + str(page) + PAGE_NUM_PARAM_END
    headers = { 'User-Agent' : userAgent }
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    if response and response.getcode() == 200:
        content = response.read()
        myVideos = common.parseDOM(content, name = "div", attrs = { 'class': 'listaItem' }, ret = False)
        for myVideo in myVideos:
            videoLink = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'imgLink' }, ret = False)
            videoLinkHref = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'imgLink' }, ret = 'href')
            VideoCategory = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'imgLink' }, ret = 'title')
            if len(videoLinkHref) > 1:
                myVideoLinkHref = videoLinkHref[0]
                myVideoCategory = VideoCategory[0]
                
            else:
                myVideoLinkHref = videoLinkHref
                myVideoCategory = VideoCategory
            myParam = {}
            xmlLink = XML_URL_BEGIN + createItemURI(extractItemIdFromURL(myVideoLinkHref)) + '.xml'            
            myParam['v'] = xmlLink
            thumbLink = common.parseDOM(videoLink, name = 'img', ret = 'src')
            myVideoTitleSection = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'textoTv4' }, ret = None)
            myVideoTitle = myVideoTitleSection[0].encode('utf-8')
            myVideoDateTimeSection = common.parseDOM(myVideo, name = 'p', attrs = { 'class': 'textoTv1' }, ret = None)
            myVideoDateTime = myVideoDateTimeSection[0].encode('utf-8').split('|')
            if len(myVideoDateTime) > 1:
                myDateTime = myVideoDateTime[len(myVideoDateTime) - 1]
            else:
                myDateTime = myVideoDateTimeSection[0].encode('utf-8')
            myThumbLink = resizeThumb(thumbLink[0], thumbSize)
            util.addMenuItem('[COLOR=FFFF0000]' + str.upper(myVideoCategory.encode('utf-8')) + '[/COLOR] [COLOR=FF0000FF]' + myDateTime + '[/COLOR] ' + myVideoTitle, util.makeLink(myParam), icon=None, thumbnail=myThumbLink, folder=False, fanart=fanart)
        myParam2 = { 's': 'yes' , 'q': searchString, 'p' : str(int(page) + 1) }
        util.addMenuItem(nextPageString + ' >>>', util.makeLink(myParam2), icon=None, thumbnail=None, folder=True, fanart=fanart)
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to get video information' % (params['video']))      
    
    
  
    
def listVideos(userAgent, thumbSize, params, fanart=None, nextPageString='NEXT PAGE'):
    common = CommonFunctions
    if 'p' in params:
        page = params['p']
    else:
        page = 1
    params_f = params['f']
    url = WEB_PAGE_BASE + params['f'] + '?' + PAGE_NUM_PARAM_BEGIN + str(page) + PAGE_NUM_PARAM_END
    headers = { 'User-Agent' : userAgent }
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    if response and response.getcode() == 200:
        content = response.read()
        myVideos = common.parseDOM(content, name = "div", attrs = { 'class': 'listaItem' }, ret = False)
        for myVideo in myVideos:
            videoLink = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'imgLink' }, ret = False)
            videoLinkHref = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'imgLink' }, ret = 'href')
            VideoCategory = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'imgLink' }, ret = 'title')
            if len(videoLinkHref) > 1:
                myVideoLinkHref = videoLinkHref[0]
                myVideoCategory = VideoCategory[0]
                
            else:
                myVideoLinkHref = videoLinkHref
                myVideoCategory = VideoCategory
            myParam = {}
            xmlLink = XML_URL_BEGIN + createItemURI(extractItemIdFromURL(myVideoLinkHref)) + '.xml'            
            myParam['v'] = xmlLink
            thumbLink = common.parseDOM(videoLink, name = 'img', ret = 'src')
            myVideoTitleSection = common.parseDOM(myVideo, name = 'a', attrs = { 'class': 'textoTv4' }, ret = None)
            myVideoTitle = myVideoTitleSection[0].encode('utf-8')
            myVideoDateTimeSection = common.parseDOM(myVideo, name = 'p', attrs = { 'class': 'textoTv1' }, ret = None)
            myVideoDateTime = myVideoDateTimeSection[0].encode('utf-8').split('|')
            if len(myVideoDateTime) > 1:
                myDateTime = myVideoDateTime[len(myVideoDateTime) - 1]
            else:
                myDateTime = myVideoDateTimeSection[0].encode('utf-8')
            myThumbLink = resizeThumb(thumbLink[0], thumbSize)
            util.addMenuItem('[COLOR=FFFF0000]' + str.upper(myVideoCategory.encode('utf-8')) + '[/COLOR] [COLOR=FF0000FF]' + myDateTime + '[/COLOR] ' + myVideoTitle, util.makeLink(myParam), icon=None, thumbnail=myThumbLink, folder=False, fanart=fanart)
        myParam2 = { 'f': params_f , 'p' : str(int(page) + 1) }
        util.addMenuItem(nextPageString + ' >>>', util.makeLink(myParam2), icon=None, thumbnail=None, folder=True, fanart=fanart)
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to get video information' % (params['video']))      


 
def buildMenu(user_agent, fanart=None, searchString='SEARCH'):
    common = CommonFunctions
    url = WEB_PAGE_BASE + '/index.php'
    headers = { 'User-Agent' : user_agent }
    req = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(req)
    if response and response.getcode() == 200:
        content = response.read()
        subHtml = common.parseDOM(content, name = "div", attrs = { 'id': 'menuTvestadao' }, ret = False) 
        myHrefs = common.parseDOM(subHtml, name = 'a', ret = 'href')
        myNames = common.parseDOM(subHtml, name = 'a', ret = False)
        if len(myHrefs) >= 1:
            util.addMenuItem('<<< ' + searchString + ' >>>', util.makeLink( { 's' : 'yes' } ), icon=None, thumbnail=None, folder=True, fanart=fanart)
        i = 0
        for majorlink in myHrefs:
            myParam = {}
            myParam['f'] = majorlink
            util.addMenuItem(myNames[i].encode('utf-8'), util.makeLink(myParam), icon=None, thumbnail=None, folder=True, fanart=fanart)
            i = i + 1
    else:
        util.showError(ADDON_ID, 'Could not open URL %s to create menu' % (url))
 