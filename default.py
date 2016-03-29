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
import sys
import os
sys.path.append( os.path.join ( os.path.dirname(__file__),'resources','lib') )
import tvnoe
import xbmcprovider,xbmcaddon,xbmcutil,xbmc
import util
import traceback,urllib2

__scriptid__   = 'plugin.video.tvnoe.cz'                                    
__scriptname__ = 'tvnoe.cz'
__addon__      = xbmcaddon.Addon(id=__scriptid__)
__language__   = __addon__.getLocalizedString
__set          = __addon__.getSetting

#settings = {'quality':__set('quality')}
settings = {'downloads':__addon__.getSetting('downloads'), 'quality':__addon__.getSetting('quality')}

params = util.params()
#if params=={}:
#    xbmcutil.init_usage_reporting( __scriptid__)
provider = tvnoe.TvNoeContentProvider()



#import pydevd
#pydevd.settrace(stdoutToServer=True, stderrToServer=True)

'''
class TvnoeXBMContentProvider(xbmcprovider.XBMCMultiResolverContentProvider):

    def resolve(self,url):
        result = xbmcprovider.XBMCMultiResolverContentProvider.resolve(self,url)
        if result:
            # ping tvnoe.cz GA account
            host = 'tvnoe.cz'
            tc = 'UA-35173050-1'
            try:
                utmain.main({'id':__scriptid__,'host':host,'tc':tc,'action':url})
            except:
                print 'Error sending ping to GA'
                traceback.print_exc()
        return result

TvnoeXBMContentProvider(provider,settings,__addon__).run(params)
'''
xbmcprovider.XBMCMultiResolverContentProvider(provider,settings,__addon__).run(params)



