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

from character.players import AllPlayers, LOGIN, PLAYING

from utils.login import getUsername
from utils.text import cleanPlayerInput
from world.maps import World
from world.maps import NORTH, NE, EAST, SE, SOUTH, SW, WEST, NW, UP, DOWN



# Command list.
commands = { '/quit':            "",
             'north':            World.movePlayer,
             'ne':               World.movePlayer,
             'northeast':        World.movePlayer,
             'east':             World.movePlayer,
             'se':               World.movePlayer,
             'southeast':        World.movePlayer,
             'south':            World.movePlayer,
             'sw':               World.movePlayer,
             'southwest':        World.movePlayer,
             'west':             World.movePlayer,
             'nw':               World.movePlayer,
             'northwest':        World.movePlayer,      
             'up':               World.movePlayer,
             'down':             World.movePlayer,
             'rest':             ""
             
           }

def GameParser(player, line):
    """
    GameParser()
    
    Parses information send my client and
    makes decisions based on that information.
    """
    
    line = cleanPlayerInput(line)
    
    # If not playing, don't use main game parser
    if player.STATUS is not PLAYING:
        statusMatrix(player, line)
        return
 
    # If just hit enter, display room
    if line == "":
        World.mapGrid[player.room].displayRoom(player)
        return      
    
    cmd = line.split()
    cmdstr = re.compile(re.escape(cmd[0].lower()))
                        
          
    for each in commands.keys():
        if cmdstr.match(each): 
            if each == "/quit" and len(cmd[0]) > 1:
                player.disconnectClient()
                return
            elif each == "north" and len(cmd) == 1 and len(cmd[0]) != 2:
                commands[each](player, NORTH)
                return
            elif (each == "ne" and len(cmd) == 1 and len(cmd[0]) == 2):
                commands['northeast'](player, NE)
                return
            elif (each == "northeast" and len(cmd) == 1 and len(cmd[0]) > 5 ):
                commands['northeast'](player, NE)
                return
            elif each == "east" and len(cmd) == 1 and len(cmd[0]) != 2:
                commands[each](player, EAST)
                return
            elif (each == "se" and len(cmd) == 1 and len(cmd[0]) == 2): 
                commands['southeast'](player, SE)
                return
            elif (each == "southeast" and len(cmd) == 1 and len(cmd[0]) > 5):
                commands['southeast'](player, SE)
                return
            elif each == "south" and len(cmd) == 1 and len(cmd[0]) != 2:
                commands[each](player, SOUTH)
                return
            elif (each == "sw" and len(cmd) == 1 and len(cmd[0]) == 2):
                commands['southwest'](player, SW)
                return
            elif (each == "southwest" and len(cmd) == 1 and len(cmd[0]) > 5 ):
                commands['southwest'](player, SW)
                return
            elif each == "west" and len(cmd) == 1 and len(cmd[0]) != 2:
                commands[each](player, WEST)
                return
            elif (each == "nw" and len(cmd) == 1 and len(cmd[0]) == 2):
                commands['northwest'](player, NW)
                return
            elif (each == "northwest" and len(cmd) == 1 and len(cmd[0]) != 2):
                commands['northwest'](player, NW)
                return
            elif each == "up" and len(cmd) == 1 and len(cmd[0]) != 2:
                commands[each](player, UP)
                return
            elif each == "down" and len(cmd) == 1 and len(cmd[0]) != 2:
                commands[each](player, DOWN)
                return
            elif each == "rest" and len(cmd) == 1 and len(cmd[0]) == 4:
                commands[each](player)
                return                            
                 
    from commands.communicate import say
    say( player, line )
 
    
        
 
            
def statusMatrix(player, line):
    """
    Routes player's input based on their
    status if statis isn't "PLAYING"
    """
    
    if player.STATUS is LOGIN:
        getUsername(player, line)
        return 