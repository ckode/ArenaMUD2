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



class Door:
    """
    Doors class
    """

    def __init__(self):
        """
        Initialize Doors object.
        """
        
        self.id = None
        self.exit1 = None
        self.exit2 = None
        
    
    def __repr__(self):
        """
        String defining object
        """
        return "Door ID: {0} exit1: {1} exit2: {2}".format(self.id, self.exit1, self.exit2)
        
    def getExitRoom(self, roomid):
        """
        getExitRoom(self, roomid)
        
        Return the room the door leads too.
        Takes current room's roomid.
        """
        
        if self.exit1 == roomid:
            return self.exit2
        else:
            return self.exit1
        
        