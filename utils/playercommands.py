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

from utils.defines import WHITE, RED, BROWN, YELLOW
from character.functions import sendToRoomNotPlayer
import combat.functions
from utils.defines import DIRS, NORTH, NE, EAST, SE
from utils.defines import SOUTH, SW, WEST, NW, UP, DOWN


def showMap( player ):
    """
    Display current z-axis level of the map.
    """
    
    from world.maps import World
   
    z = int(player.room[2:])
    r = "{0}".format(WHITE)
    d = "|---" * 10 + "|"
 
    player.sendLine( "{0}".format(World.levelnames[z]).center(40, " ")    )
    
    for x in range(World.height):
        player.sendLine(d)
        for y in range(World.width):
            room = "{0}{1}{2}".format(x, y, z)
            if World.mapGrid[room]:
                if room == player.room:
                    r = r + "|{0}You{1}".format(RED, WHITE)
                else:
                    r = r + "|   "
            else:
                r = r + "|###"
            if y == (World.width - 1):
                r = r + "|"
        player.sendLine(r) 
        r = "{0}".format(WHITE)
        
    player.sendLine(d)  
    player.statLine()
    
def showLevel( player ):
    """
    version of showMap that shows doors.
    """
    
    from world.maps import World
   
    z = int(player.room[2:])
    roomLine = "{0}".format(WHITE)
    exitLine = "{0}".format(WHITE)
    marker = ''
     
    player.sendLine("{0}{1}{2}".format(YELLOW, (World.levelnames[z]).center(27, " "), WHITE))
    
    for x in range(World.height):
        for y in range(World.width):
            room = "{0}{1}{2}".format(x, y, z)
            if World.mapGrid[room]:
                if room == player.room:
                    marker = "{0}X{1}".format(RED, WHITE)
                else:
                    marker = '#'
                if World.mapGrid[room].hasExit(EAST) and World.mapGrid[room].hasExit(WEST):
                    roomLine += '-' + marker + '-'
                elif World.mapGrid[room].hasExit(WEST):
                    roomLine += '-' + marker + ' '
                elif World.mapGrid[room].hasExit(EAST):
                    roomLine += ' ' + marker + '-'
                else:
                    roomLine += ' ' + marker + ' '
                if World.mapGrid[room].hasExit(SW):
                    exitLine += '/'
                else:
                    exitLine += ' '
                if World.mapGrid[room].hasExit(SOUTH):
                    exitLine += '|'
                else:
                    exitLine += ' '
                if World.mapGrid[room].hasExit(SE):
                    exitLine += '\\'
                else:
                    exitLine += ' '
            else:
                if y==0:
                    roomLine += '  '
                    exitLine += '  '
                    continue
                if y == (World.width - 1):
                    roomLine += '  '
                    exitLine += '  '
                    continue
                
                roomLine = roomLine + '   '
                exitLine += '   '
                            
        player.sendLine(roomLine)
        player.sendLine(exitLine)
        roomLine = "{0}".format(WHITE)
        exitLine = "{0}".format(WHITE)
        
                
    player.statLine()
    
    
def breakCombat(player):
    """
    Break off combat if engaged.
    """
    
    if player.attacking:
        sendToRoomNotPlayer( player, "{0}{1} breaks off combat.".format(BROWN, player.name) )
    combat.functions.endCombat( player ) 
    player.statLine()