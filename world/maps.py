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

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class GameMap:
    """
    GameMap()
    
    Object that hold all map data.
    """
    
    def __init__(self, mapdb):
        """
        GameMap->__init__(self, mapdb)
        
        Creates an empty map grid.
        """
        
        self.mapGrid  = {}
        self.height   = 10
        self.width    = 10
        self.depth    = 10
        
        def buildGrid(self):
            """
            buildGrid()
            
            Build grid inside of a dictionary
            with roomid being the key.
            """
            
            # create 10x10x10 game world grid
            for x in range(self.height):
                for y in range(self.width):
                    for z in range(self.depth):
                        roomid = "{0}{1}{2}".format(x, y, z)
                        self.mapGrid[roomid] = None
            
        
        
        
        def getExits(self, roomid):
            """
            Returns exit directions.
            """
                            
            x = roomid[0]
            y = roomid[1]
            z = roomid[2]
                            
      