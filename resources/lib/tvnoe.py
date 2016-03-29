# -*- coding: UTF-8 -*-
#/*
# *
# *
# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with this program; see the file COPYING.  If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *
# */

import re,os,urllib,urllib2,shutil,traceback,cookielib,HTMLParser


import util,resolver
from bs4 import BeautifulSoup


from provider import ContentProvider, cached

HDRS = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:38.0) Gecko/20100101 Firefox/38.0"}


class NoRedirectionHTTPErrorProcessor(urllib2.HTTPErrorProcessor):

    def http_response(self, request, response):
        return response


class TvNoeContentProvider(ContentProvider):

    def __init__(self,username=None,password=None,filter=None):
        ContentProvider.__init__(self,'tvnoe.cz','http://www.tvnoe.cz',username,password,filter)
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar()))
        urllib2.install_opener(opener)
        self.order_by = ''
        self.strict_search = False

    def capabilities(self):
        return ['resolve', 'categories', '!download']
   

    def list(self,url):       
        if url.find('#live#') == 0:            
            return self.list_live(util.request(self._url('live')))        
        return []
    
    
    #def parse_xml(self,url):
    #    return BeautifulSoup(util.request(url), 'xml', from_encoding='utf-8')
    
    
    #def _loadXspf(self, url): 
    #    bs = self.parse_xml(url)
    #    return [t.text for t in bs.find_all('location')]
            
    def _loadXspf(self, url): 
        xspf = util.request(url)
        return re.findall('<location><!\[CDATA\[(.*)\]\]>',xspf,re.IGNORECASE|re.DOTALL);        
        
        

    def list_live(self,page):
        page = util.substr(page,'icovlc.png','</section>')
        result = []
        namePat = re.compile('(rtmp\d+)\.xspf')        
        for m in re.finditer('<a href=\"(?P<url>[^\"]+)[^>]+>',page,re.IGNORECASE|re.DOTALL):
            url = m.group('url')
            xsfpItems = self._loadXspf(self._url(url))
            if len(xsfpItems) < 1:
                continue                        
            nameMatch = namePat.search(url)             
            item = self.video_item()
            item['url'] = xsfpItems[0]
            #item['url'] = 'rtmp://w100.quickmedia.tv/prozeta-live04/_definst_?id=mPlsL8ctdFZnlK-03/prozeta-live04-MP4_176p-1.stream'
            
            item['title'] = nameMatch.group(1)
            result.append(item)
            
        return result

    def categories(self):
        result = []
        item = self.dir_item()
        item['title'] = 'Živě'
        item['url'] = '#live#'
        result.append(item)        
        return result
    
    def getRedirectionTarget(self, url):
        opener = urllib2.build_opener(NoRedirectionHTTPErrorProcessor)
        response = opener.open(url)
        targetUrl = response.headers.get('Location', url)        
        response.close()
        return targetUrl

    def resolve(self,item,captcha_cb=None,select_cb=None):        
        url =self.getRedirectionTarget(item['url'])        
        return self.video_item(url)
        
        
        #if len(result)==1:
        #    return result[0]
        #elif len(result) > 1 and select_cb:
        #    return select_cb(result)




if __name__ == '__main__':
    cp = TvNoeContentProvider()
    cp.list('#live#')
    
