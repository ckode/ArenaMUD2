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
        self.nw          = None
        self.n           = None
        self.ne          = None
        self.e           = None
        self.se          = None
        self.s           = None
        self.sw          = None
        self.w           = None
        self.u           = None
        self.w           = None
        
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
        Return exits text
        """
        
        exitsExists = False
        
        if self.n:
            exits = "north"
            count += 1        
        if self.ne:
            if not exitsExists:
                exits = "northeast"
            else:
                exits += ", northeast"
        if self.e:
            if not exitsExists:
                exits = "east"
            else:
                exits += ", east" 
        if self.se:
            if not exitsExists:
                exits = "southeast"
            else:
                exits += ", southeast" 
        if self.s:
            if not exitsExists:
                exits = "south"
            else:
                exits += ", south"               
        if self.sw:
            if not exitsExists:
                exits = "southwest"
            else:
                exits += ", southwest"
        if self.sw:
            if not exitsExists:
                exits = "southwest"
            else:
                exits += ", southwest"
        if self.w:
            if not exitsExists:
                exits = "west"
            else:
                exits += ", west"
        if self.nw:
            if not exitsExists:
                exits = "northwest"
            else:
                exits += ", northwest"
        if exitsExists is None:
            exits += "NONE."
        else:
            exits += "."
        
        return exits
 

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
                
    
    def displayRoom(self, player):
        """
        Display the room
        """
        from commands.communicate import WHITE, GREEN, LCYAN, LMAGENTA
        
        if player.blind:
            player.sendLine( "{0}You are blind.".format(WHITE) )
            return
        
        if player.vision < self.light:
            player.sendLine( "{0}You cannot see anything, it's too dark.".format(WHITE) )
            return
        
        player.sendLine( "{0}{1}".format(LCYAN, self.name) )
        
        playersinroom = self.whosInRoom(player)
        if playersinroom is not None:
            player.sendLine( "{0}Also here:{1} {2}".format(GREEN, LMAGENTA, playersinroom) )
            
        player.sendLine("{0}Obvious exits: {1}{2}".format(GREEN, self.getExits(), WHITE) )
        
        
        