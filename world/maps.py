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

import sqlite3

import world.doors
import world.rooms
from utils.defines import WHITE
from utils.defines import DIRS, NORTH, NE, EAST, SE
from utils.defines import SOUTH, SW, WEST, NW, UP, DOWN
from utils.defines import PURGATORY


World = None

class GameMap:
    """
    GameMap()
    
    Object that hold all map data.
    """
    
    def __init__(self, mapdb):
        """
        GameMap->__init__(self, mapdb)
        
        Creates GameMap object and loads maps
        """

        from logger.gamelogger import logger
        
        self.mapGrid  = {}
        self.doors    = {}
        self.height   = 10
        self.width    = 10
        self.depth    = 10

         
         
        # create 10x10x10 game world grid
        for x in range(self.height):
            for y in range(self.width):
                for z in range(self.depth):
                    roomid = "{0}{1}{2}".format(x, y, z)
                    self.mapGrid[roomid] = None
 
        
        try:
            conn = sqlite3.connect("data\\" + mapdb)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM DOORS;")
            d_results = cursor.fetchall()
            cursor.execute("SELECT * FROM ROOMS;")
            r_results = cursor.fetchall()
            
        except:
            logger.log.critical( "Database errors using: {0}".format(mapdb) )
                
        
        logger.log.info("Loading doors.")    
        # Load doors
        for row in d_results:
            self.doors[row[0]]           = world.doors.Door()
            self.doors[row[0]].exits1    = row[1]
            self.doors[row[0]].exits1    = row[2]
       
        logger.log.info("Loading rooms.")
        # Load rooms into grid. 
        for row in r_results:
            rid = str(row[0]).zfill(3)
            
            self.mapGrid[rid]               = world.rooms.Room()
            
            self.mapGrid[rid].name          = str(row[1])
            self.mapGrid[rid].dirs[NORTH]   = row[2]            
            self.mapGrid[rid].dirs[NE]      = row[3]
            self.mapGrid[rid].dirs[EAST]    = row[4]            
            self.mapGrid[rid].dirs[SE]      = row[5]
            self.mapGrid[rid].dirs[SOUTH]   = row[6]            
            self.mapGrid[rid].dirs[SW]      = row[7]
            self.mapGrid[rid].dirs[WEST]    = row[8]            
            self.mapGrid[rid].dirs[NW]      = row[9]
            self.mapGrid[rid].dirs[UP]      = row[10]            
            self.mapGrid[rid].dirs[DOWN]    = row[11]
            self.mapGrid[rid].spell         = row[12]
            self.mapGrid[rid].light         = row[13]                     
            
            
            
    def getExit(self, direction):
        """
        Returns exit directions.
        """
                            
        x = roomid[0]
        y = roomid[1]
        z = roomid[2]
            
            

            
                            
      
