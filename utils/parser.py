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
from copy import deepcopy

import world.maps
import world.magic

from utils.login import getUsername, getClass
from utils.text import cleanPlayerInput
from utils.defines import LOGIN, PLAYING, GETCLASS, PURGATORY, STUN
from utils.defines import SCLASS, TARGET, SNEAKING
from utils.defines import CYAN, WHITE, YELLOW
from utils.defines import NORTH, NE, EAST, SE, SOUTH, SW, WEST, NW, UP, DOWN
from utils.playercommands import showMap, showLevel, breakCombat, look

import utils.gameutils
import character.functions
import character.communicate

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
    elif player.status is PURGATORY:
        PurgatoryParser(player, line)
        return



# Command list.
commands = { '/quit':            "",
             'north':            "",
             'ne':               "",
             'northeast':        "",
             'east':             "",
             'se':               "",
             'southeast':        "",
             'south':            "",
             'sw':               "",
             'southwest':        "",
             'west':             "",
             'nw':               "",
             'northwest':        "",
             'up':               "",
             'down':             "",
             'rest':             "",
             'map':              showMap,
             'attack':           "",
             'break':            breakCombat,
             'rest':             "",
             'gossip':           "",
             'level':            showLevel,
             'look':             "",
             'who':              "",
             'sneak':            "",
             'reloadspells':     "",
             'admin':            ""
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
    
    if player.stats[STUN] is 1:
        character.communicate.sendToPlayer(player, "You are stun!")
        return
    
    # If just hit enter, display room
    if line == "":
        #world.maps.World.mapGrid[player.room].displayRoom(player)
        character.functions.displayRoom(player, player.room)
        return      
    
    
    cmd = line.split()
    
    # If casting a spell.
    if SpellParser(player, cmd):
        return
    
    cmdstr = re.compile(re.escape(cmd[0].lower()))
                        
          
    for each in commands.keys():
        if cmdstr.match(each): 
            if each == "/quit" and len(cmd[0]) > 1:
                player.disconnectClient()
                return
            elif each == "north" and len(cmd) == 1 and len(cmd[0]) != 2:
                character.functions.movePlayer(player, NORTH)
                return
            elif (each == "ne" and len(cmd) == 1 and len(cmd[0]) == 2):
                character.functions.movePlayer(player, NE)
                return
            elif (each == "northeast" and len(cmd) == 1 and len(cmd[0]) > 5 ):
                character.functions.movePlayer(player, NE)
                return
            elif each == "east" and len(cmd) == 1 and len(cmd[0]) != 2:
                character.functions.movePlayer(player, EAST)
                return
            elif (each == "se" and len(cmd) == 1 and len(cmd[0]) == 2):
                character.functions.movePlayer(player, SE)
                return
            elif (each == "southeast" and len(cmd) == 1 and len(cmd[0]) > 5):
                character.functions.movePlayer(player, SE)
                return
            elif each == "south" and len(cmd) == 1 and len(cmd[0]) != 2:
                character.functions.movePlayer(player, SOUTH)
                return
            elif (each == "sw" and len(cmd) == 1 and len(cmd[0]) == 2):
                character.functions.movePlayer(player, SW)
                return
            elif (each == "southwest" and len(cmd) == 1 and len(cmd[0]) > 5 ):
                character.functions.movePlayer(player, SW)
                return
            elif each == "west" and len(cmd) == 1 and len(cmd[0]) != 2:
                character.functions.movePlayer(player, WEST)
                return
            elif (each == "nw" and len(cmd) == 1 and len(cmd[0]) == 2):
                character.functions.movePlayer(player, NW)
                return
            elif (each == "northwest" and len(cmd) == 1 and len(cmd[0]) > 5 ):
                character.functions.movePlayer(player, NW)
                return
            elif each == "up" and len(cmd) == 1 and len(cmd[0]) != 2:
                character.functions.movePlayer(player, UP)
                return
            elif each == "down" and len(cmd) == 1 and len(cmd[0]) != 2:
                character.functions.movePlayer(player, DOWN)
                return
            elif each == "rest" and len(cmd) == 1 and len(cmd[0]) == 4:
                character.functions.rest(player)
                return                            
            elif each == "map" and len(cmd) == 1 and len(cmd[0]) == 3:
                commands[each](player)
                return
            elif each == "level" and len(cmd) == 1 and len(cmd[0]) == 5:
                commands[each](player)
                return    
            elif each == "attack" and len(cmd) == 2:
                combat.functions.attack(player, cmd[1])
                return                
            elif each == "break" and len(cmd) == 1 and len(cmd[0]) > 2:
                commands[each](player)
                return
            elif each == "gossip" and len(cmd) > 1 and len(cmd[0]) > 2:
                character.communicate.gossip(player, line[(len(cmd[0]) + 1):])
                return            
            elif each == "look" and len(cmd) > 1:
                look(player, line[(len(cmd[0]) + 1):])
                return
            elif each == "who" and len(cmd) is 1:
                utils.playercommands.who(player)
                return  
            elif each == "sneak" and len(cmd) is 1 and len(cmd[0]) > 1:
                utils.playercommands.Sneak(player)
                return
            elif each == "reloadspells" and len(cmd) is 1:
                world.maps.World.CastableSpells = world.magic.loadPlayerSpells()
                return
            elif each == "admin" and len(cmd) > 1 and len(cmd[0]) > 2:
                utils.playercommands.requestAdmin(player, line[(len(cmd[0]) + 1):])
                return          
            
            
    from character.communicate import say
    player.setAttr(SNEAKING, False)
    say( player, line )
 
    

# Purgatory command list.
PurgatoryCommands = { '/quit':            "",
                      'gossip':           "",
                      'spawn':            "",
                      'who':              ""
               }        
 
def PurgatoryParser(player, line):
    """
    Parse commands for players in
    the purgatory state.
    """
    
    cmd = line.split()
    
    if len(cmd) == 0:
        player.statLine()
        return    
    
    cmdstr = re.compile(re.escape(cmd[0].lower()))
                         
           
    for each in PurgatoryCommands.keys():
        if cmdstr.match(each): 
            if each == "/quit" and len(cmd[0]) > 1:
                player.disconnectClient()
                return     
            elif each == "gossip" and len(cmd) > 1 and len(cmd[0]) > 2:
                character.communicate.gossip(player, line[(len(cmd[0]) + 1):])
                return                
            elif each == "spawn":
                if len(cmd[0]) > 2 and len(cmd) == 1:
                    character.functions.spawnPlayer(player)
                    return
                continue                
            elif each == "who" and len(cmd) is 1:
                utils.playercommands.who(player)
                return               

    utils.gameutils.purgatoryHelpMsg(player)


def SpellParser(player, cmd):
    """
    Look for player casting spells.
    """
    
    spellList = world.maps.World.CastableSpells
        
    if len(cmd[0]) is 4 and cmd[0] in spellList.keys():
        if len(cmd) is spellList[cmd[0]].getAttr(TARGET) or spellList[cmd[0]].getAttr(TARGET) is 3 and len(cmd) < 3:
            if spellList[cmd[0]].getAttr(SCLASS) is player.classid:
                spell = deepcopy(spellList[cmd[0]])
                spell.castSpell(player, cmd)
                return True
            else:
                pass
                
    return False