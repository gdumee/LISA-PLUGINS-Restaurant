# -*- coding: UTF-8 -*-
#-----------------------------------------------------------------------------
# project     : Lisa plugins
# module      : Restaurant
# file        : Restaurant.py
# description : Manage guests requests about restaurant in a hotel
# author      : G.Audet
#-----------------------------------------------------------------------------
# copyright   : Neotique
#-----------------------------------------------------------------------------
# TODO : 

#
Version = "1.0.0"



#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------
#Mandatory
from lisa.server.plugins.IPlugin import IPlugin
import gettext
import inspect
import os


#ohters
from lisa.Neotique.NeoConv import NeoConv


#-----------------------------------------------------------------------------
# Plugin Restaurant class
#-----------------------------------------------------------------------------
class Restaurant(IPlugin):
    """
    Plugin main class
    """
    def __init__(self):
        super(Restaurant, self).__init__(plugin_name = "Restaurant")
        self.WITDate = NeoConv(self._).WITDate
        self.time2str = NeoConv(self._).time2str

    #-----------------------------------------------------------------------------
    #              Publics  Fonctions
    #-----------------------------------------------------------------------------
    def getmenuRestau(self, jsonInput):
        """
        get menu for evening, lunch, tomorrow...  
        """
        #print jsonInput
        
        # Get informations
        dDate = self.WITDate(jsonInput)
        
        #get menu
        if dDate['delta'] < 0 :           #fatal
            return {"plugin": "Restaurant","method": "get_menuRestau","body": self._("previous date")}
        elif dDate['delta'] > 0 :        #fatal
            return {"plugin": "Restaurant","method": "get_menuRestau","body": self._("not yet")}
        else :                                #==0   get menu
            menu = self._getmenu(part=dDate['part'],tpart=dDate['tpart'])
            return {"plugin": "Restaurant","method": "get_menuRestau","body": menu}

    #-----------------------------------------------------------------------------
    def gettimeRestau(self, jsonInput):
        """
        get opening hours 
        """
        #print jsonInput
        dDate = self.WITDate(jsonInput)
        
        message = self._gettime(part=dDate['part'],tpart=dDate['tpart'])
        return {"plugin": "Restaurant","method": "gettimeRestau","body": message}
 
    #-----------------------------------------------------------------------------
    def reserveRestau(self, jsonInput):
        """
        set a reservation
        """
        return {"plugin": "Restaurant","method": "set_Restau","body": "Trés bien je note votre réservation"}

    #-----------------------------------------------------------------------------



    #-----------------------------------------------------------------------------
    #              privates functions
    #-----------------------------------------------------------------------------
    def _getmenu(self,part,tpart) :
        """
        get menu
        """
        if part == 'alltheday' :
            message = self._('no-menu')
        else  :
            menu = {
            u'name': u'Restaurant',
            u'menu': {
                u'morning':{u'plat' : u'petit déjeuner à la française'},
                u'midday': {u'plat' : u'bavette et frites et dessert du jour'},
                u'evening': {u'plat' : u'soupe de poisson et ses croutons'}
            }
            }
            message = self._('menu').format(moment=tpart,menu=menu['menu'][part]['plat'])
        
        
        return message
    #-----------------------------------------------------------------------------
    def _gettime(self,part,tpart) :
        """
        get opening hours
        """
        message=''
        if part == 'alltheday' :
            for t in ('morning','midday','evening') :
                menu = {
                u'name': u'Restaurant',
                u'heure': {
                    u'morning' : {u'depart': '06:00',u'fin' : '09:30'},
                    u'midday' : {u'depart' : '12:00',u'fin' : '14:00'},
                    u'evening' : {u'depart' : '18:10',u'fin': '21:30'}
                },
                }
                starttime = self.time2str(menu['heure'][t]['depart'],pMinutes=0)
                stoptime = self.time2str(menu['heure'][t]['fin'],pMinutes=0)
                message += self._('opening').format(moment=t,starttime = starttime,stoptime = stoptime)
        else  :
            menu = {
            u'name': u'Restaurant',
            u'heure': {
                u'morning' : {u'depart': '06:00',u'fin' : '09:30'},
                u'midday' : {u'depart' : '12:00',u'fin' : '14:00'},
                u'evening' : {u'depart' : '18:10',u'fin': '21:30'}
            },
            }
            starttime = self.time2str(menu['heure'][part]['depart'],pMinutes=0)
            stoptime = self.time2str(menu['heure'][part]['fin'],pMinutes=0)
            message = self._('opening').format(moment=tpart,starttime = starttime,stoptime = stoptime)
        return message
#-----------------------------------------------------------------------------
# End of Plugin Restaurant class
#-----------------------------------------------------------------------------






#-----------------------------------------------------------------------------
# Tests
#-----------------------------------------------------------------------------
if __name__ == "__main__" :
  
    hotel_restau_getmenu = {'from': u'Lisa-Web', 'zone': u'WebSocket', u'msg_id': u'67765841-b544-4896-89ea-52ab4dfb6001', 
                    u'msg_body': u'quel est le menu ce soir',
                    u'outcome': {
                        u'entities': {
                            u'datetime': {u'body': u'ce soir', u'start': 17, u'end': 24, u'value': {u'to': u'2014-07-12T13:00:00.000+04:00', u'from': u'2014-07-11T12:00:00.000+04:00'}}
                        },
                        u'confidence': 0.901,
                        u'intent': u'hotel_restau_getmenu'
                    },
                    'type': u'chat'
                }
    hotel_restau_getime = {'from': u'Lisa-Web', 'zone': u'WebSocket', u'msg_id': u'67765841-b544-4896-89ea-52ab4dfb6001', 
                    u'msg_body': u'quel est le menu ce soir',
                    u'outcome': {
                        u'entities': {
                            u'datetime': {u'body': u'ce soir', u'start': 17, u'end': 24, u'value': {u'to': u'2014-07-12T00:00:00.000+04:00', u'from': u'2014-07-11T18:00:00.000+04:00'}}
                        },
                        u'confidence': 0.901,
                        u'intent': u'hotel_restau_getime'
                    },
                    'type': u'chat'
                }

    essai =Restaurant() #class init
    
    #ret = essai.getmenuRestau(hotel_restau_getmenu)
    ret = essai.gettimeRestau(hotel_restau_getime)
    print ret['body']
    


# --------------------- End of Minuteur.py  ---------------------
