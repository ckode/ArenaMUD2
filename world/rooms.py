#  ArenaMUD2 - A multiplayer combat game - http://arenamud.david-c-brown.com
#  Copyright (C) 2012 - David C Brown & Mark Richardson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re

from utils.defines import DIRS, NORTH, NE, EAST, SE
from utils.defines import SOUTH, SW, WEST, NW, UP, DOWN
from utils.defines import WHITE, GREEN, LCYAN, LMAGENTA


class Room:
    """
    Room class
    """
    
    def __init__(self):
        """
        Initialize room object.
        """
        
        self.id          = None
                
        self.name        = "Room"
        self.nospawn     = False
        
        self.dirs        = {}
        self.dirs[NORTH] = None
        self.dirs[NE]    = None
        self.dirs[EAST]  = None
        self.dirs[SE]    = None
        self.dirs[SOUTH] = None
        self.dirs[SW]    = None
        self.dirs[WEST]  = None
        self.dirs[NW]    = None
        self.dirs[UP]    = None
        self.dirs[DOWN]  = None
        
        self.spell       = None
        self.light       = 3     
        self.players     = {}
        self.pSpells     = []
        self.items       = {}
        
        
        
    def __repr__(self):
        """
        Gets room name
        """
        
        return self.name
     
        
                
                
    def getExits(self):
        """
        Return exits text for display in room description
        """
        
        exits = ""     
        for x in range(NORTH, DOWN):
            if self.dirs[x]:
                if exits == "":
                    exits += DIRS[x]
                else:
                    exits += ", {0}".format(DIRS[x])
        if exits == "":
            exits = "NONE."
        else:
            exits += "."
        
        return exits
 
    
    def getItems(self):
        """
        Return list of items in room for room display.
        """
        
        items = ""     
        for item in self.items.keys():
            if item <> "" and items is "":
                items += item
            else:
                items += ", {0}".format(item)
                
        if items is not "":
            items += "."
        
        return items

    def hasExit(self, dir):
        """
        Return true if an exit exists in the direction given
        """
        if self.dirs[dir]:
            return True
        else:
            return False

    def whosInRoom(self, player):
        """
        Return a list of who is in the room.
        """
        
        found = False
        ptext = ""
        for _player in self.players.keys():
            if _player <> player.name:
                if found:
                    ptext += ", {0}".format(_player)
                else:
                    ptext += _player
                    found = True
        
        if len(ptext) > 0:
            return ptext + "."
        else:
            return None
                
    
    def findPlayerInRoom(self, player, Name):
        """
        Search room players for a match
        with name given.
        """
        victimList = []   
        found = []
        cName = Name.capitalize()
            
        NameSearch = re.compile( re.escape(Name.lower()) )
        for name, victim in self.players.items():
            if cName == name:
                found.append(victim)
                return found
            if name is not "" and name <> player.name:
                if NameSearch.match( name.lower() ):
                    victimList.append(victim)
    
        return victimList
        
        