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

import world.maps
from utils.login import getUsername, getClass
from utils.text import cleanPlayerInput
from utils.defines import LOGIN, PLAYING, GETCLASS
from utils.defines import NORTH, NE, EAST, SE, SOUTH, SW, WEST, NW, UP, DOWN
from utils.playercommands import showMap, breakCombat
from character.functions import movePlayer, displayRoom, rest
from character.communicate import gossip

#from combat.functions import attack
import combat.functions

            
            
            
def statusMatrix(player, line):
    """
    Routes player's input based on their
    status if statis isn't "PLAYING"
    """
    
    if player.status is LOGIN:
        getUsername(player, line)
        return 
    elif player.status is GETCLASS:
        getClass(player, line)
        return



# Command list.
commands = { '/quit':            "",
             'north':            movePlayer,
             'ne':               movePlayer,
             'northeast':        movePlayer,
             'east':             movePlayer,
             'se':               movePlayer,
             'southeast':        movePlayer,
             'south':            movePlayer,
             'sw':               movePlayer,
             'southwest':        movePlayer,
             'west':             movePlayer,
             'nw':               movePlayer,
             'northwest':        movePlayer,      
             'up':               movePlayer,
             'down':             movePlayer,
             'rest':             "",
             'map':              showMap,
             'attack':           "",
             'break':            breakCombat,
             'rest':             rest,
             'gossip':           gossip
           }

def GameParser(player, line):
    """
    GameParser()
    
    Parses information send my client and
    makes decisions based on that information.
    """
    
    line = cleanPlayerInput(line)
    
    # If not playing, don't use main game parser
    if player.status is not PLAYING:
        statusMatrix(player, line)
        return
 
    # If just hit enter, display room
    if line == "":
        #world.maps.World.mapGrid[player.room].displayRoom(player)
        displayRoom(player, player.room)
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
            elif each == "map" and len(cmd) == 1 and len(cmd[0]) == 3:
                commands[each](player)
                return         
            elif each == "attack" and len(cmd) == 2:
                combat.functions.attack(player, cmd[1])
                return                
            elif each == "break" and len(cmd) == 1 and len(cmd[0]) > 2:
                commands[each](player)
                return        
            elif each == "gossip" and len(cmd) > 1 and len(cmd[0]) > 2:
                commands[each](player, line[(len(cmd[0]) + 1):])
                return                 
            
    from character.communicate import say
    say( player, line )
 
    
        
 
            

    
