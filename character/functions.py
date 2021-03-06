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

from twisted.internet import reactor

import random

from character.communicate import sendToPlayer, tellWorld, sendToRoomNotPlayer
import world.maps 
import character.classes
import combat.functions
import utils.gameutils

from utils.defines import WHITE, LCYAN, LMAGENTA, GREEN, BLUE, LRED
from utils.defines import DIRS, OPPOSITEDIRS, DOWN, UP
from utils.defines import NORTH, NE, EAST, SE
from utils.defines import SOUTH, SW, WEST, NW
from utils.defines import PURGATORY, PLAYING
from utils.defines import YOUHIT, YOUMISS, VICTIMHIT
from utils.defines import VICTIMMISS, ROOMHIT, ROOMMISS
from utils.defines import BS_HIT_YOU, BS_HIT_VICTIM, BS_HIT_ROOM
from utils.defines import HP, MAXHP
from utils.defines import BLIND, HELD, STEALTH, VISION
from utils.defines import ATTACKS, ATTKSKILL, CRITICAL
from utils.defines import BONUSDAMAGE, DAMAGEABSORB
from utils.defines import KILLS, DEATHS, SNEAKING
from utils.defines import MAXDAMAGE, MINDAMAGE, RESTING
from utils.defines import MOVING, DODGE, BS_MULTIPLIER, ADMIN
from utils.defines import MOVERATE, SLOWMOVERATE, SLOWED

def movePlayer(player, direction):
    """
    Moves player from one room to another.
    """
        
    # If player died before the move occured, do nothing
    if player.status == PURGATORY:
        return
        
    player.stats[RESTING]= False
             
    if player.stats[MOVING] is True:
        sendToPlayer( player, "You are already moving, slow down!" )
        return
    
    if player.stats[HELD]:
        player.stats[MOVING] = False
        sendToPlayer( player, "You cannot move!" )           
        
    curRoom = world.maps.World.mapGrid[player.room]
    # Run into the wall/ceiling/floor, if no door
    if not curRoom.dirs[direction]:
        if direction is DOWN:
            sendToPlayer(player, "You run into the floor!" )
            sendToRoomNotPlayer(player, "{0} ran into the floor!".format(player))
            
        elif direction is UP:
            sendToPlayer( player, "You run into the ceiling!" )
            sendToRoomNotPlayer(player, "{0} ran into the ceiling!".format(player))            
            
        else:
            sendToPlayer(player, "You run into the {0} wall!".format(DIRS[direction]))
            sendToRoomNotPlayer(player, "{0} ran into the {1} wall!".format(player, DIRS[direction]))
            
    else:
        if player.getAttr(SLOWED):
            moverate = SLOWMOVERATE
        else:
            moverate = MOVERATE
            
        player.stats[MOVING] = True
        if player.getAttr(SNEAKING):
            sendToPlayer(player, "Sneaking...")
        
        reactor.callLater(moverate, move, player, direction)
        return
    
    player.setAttr(SNEAKING, False)
  
  
        
        
def move(player, direction):
    """
    Moves the character from one room to the next.
    """
    
    curRoom = world.maps.World.mapGrid[player.room]
    door = curRoom.dirs[direction]
    roomid = world.maps.World.doors[door].getExitRoom(curRoom.id)
    newRoom = world.maps.World.mapGrid[roomid]
    brokesneak = False
    
    if player.getAttr(SNEAKING) and not utils.gameutils.stealthRoll(player):
        player.setAttr(SNEAKING, False)
        sendToRoomNotPlayer(player, "{0}You notice {1} sneaking out to the {2}.".format(LRED, player, DIRS[direction])) 
        sendToPlayer(player, "{0}You make a sound".format(LRED))
        brokesneak = True
    elif not player.getAttr(SNEAKING):      
        sendToRoomNotPlayer( player, "{0} left to the {1}.".format(player, DIRS[direction])) 
        
    del curRoom.players[player.name]
    newRoom.players[player.name] = player
    player.room = newRoom.id

    if brokesneak:
        sendToRoomNotPlayer(player, "{0}You notice {1} sneaking into the room from the {2}.".format(LRED, player, DIRS[OPPOSITEDIRS[direction]])) 
    elif not player.getAttr(SNEAKING):
        sendToRoomNotPlayer(player, "{0} entered from the {1}.".format(player, DIRS[OPPOSITEDIRS[direction]])) 
    
    displayRoom(player, player.room)
    player.stats[MOVING] = False
    

    
def displayRoom(player, room):
    """
    Display the room
    """
    
    if player.getAttr(ADMIN) is True:
        adminDisplayRoom(player, room)
        return
        
    curRoom = world.maps.World.mapGrid[room]
    
    if player.stats[BLIND]:
        sendToPlayer( player, "{0}You are blind.".format(WHITE) )
        return
        
    if player.stats[VISION] < curRoom.light:
        sendToPlayer( player, "{0}You cannot see anything, it's too dark.".format(WHITE) )
        return
     
        
    sendToPlayer( player, "{0}{1}".format(LCYAN, curRoom.name) )
      
    items = curRoom.getItems()
    if items:
        sendToPlayer( player, "{0}You notice: {1}".format(LMAGENTA, items) )
        
    playersinroom = curRoom.whosInRoom(player)
    if playersinroom is not None:
        sendToPlayer( player, "{0}Also here:{1} {2}".format(GREEN, LMAGENTA, playersinroom) )
            
    sendToPlayer( player, "{0}Obvious exits: {1}{2}".format(GREEN, curRoom.getExits(), WHITE) )
        
        
        
def adminDisplayRoom(player, room):
    """
    Displays helpful info about rooms and doors for correcting mistakes in maps
    """
    curRoom = world.maps.World.mapGrid[room]
    exitstr = ''
    
    sendToPlayer( player, "{0}{1} - (Room #: {2})".format(LCYAN, curRoom.name, room) )
    
    items = curRoom.getItems()
    if items:
        sendToPlayer( player, "{0}You notice: {1}".format(LMAGENTA, items) )
        
    playersinroom = curRoom.whosInRoom(player)
    if playersinroom is not None:
        sendToPlayer( player, "{0}Also here:{1} {2}".format(GREEN, LMAGENTA, playersinroom) )
        
    for x in range(NORTH, DOWN + 1):
        if curRoom.dirs[x]:
            if exitstr == '':
                exitstr += DIRS[x] + '(' + str(curRoom.dirs[x]) + ')'
            else:
                exitstr += ", {0}({1})".format(DIRS[x], curRoom.dirs[x])
                
    if exitstr == "":
        exitstr = "NONE."
    else:
        exitstr += "."
            
    sendToPlayer( player, "{0}Obvious exits: {1}{2}".format(GREEN, exitstr, WHITE) )

                
def spawnPlayer( player ):
    """
    Spawn the player in the map.
    """
    
    room = random.sample(world.maps.World.roomsList, 1)[0]
    
    # Uncomment below to force spawn in a certain room
    room = "544"
    
    player.room = room
    world.maps.World.mapGrid[room].players[player.name] = player
    player.status = PLAYING
    sendToRoomNotPlayer( player, "{0}{1} appears in a flash!{2}".format(BLUE, player, WHITE) )
    tellWorld( player, None, "{0} has entered the arena!".format(player.name) )
    
    displayRoom(player, player.room)
    
    
    
def applyClassAttributes(player, classid):
    """
    Apply choosen player class attributes
    to the player.
    """  

    Classes = character.classes.Classes
    
    player.stats[ATTACKS]             = Classes[classid].attacks
    player.stats[ATTKSKILL]           = Classes[classid].attkSkill
    player.stats[MAXDAMAGE]           = Classes[classid].maxDamage
    player.stats[MINDAMAGE]           = Classes[classid].minDamage
    player.weaponText[YOUHIT]         = Classes[classid].weaponText[YOUHIT]
    player.weaponText[YOUMISS]        = Classes[classid].weaponText[YOUMISS]
    player.weaponText[VICTIMHIT]      = Classes[classid].weaponText[VICTIMHIT]
    player.weaponText[VICTIMMISS]     = Classes[classid].weaponText[VICTIMMISS]
    player.weaponText[ROOMHIT]        = Classes[classid].weaponText[ROOMHIT]
    player.weaponText[ROOMMISS]       = Classes[classid].weaponText[ROOMMISS]
    player.weaponText[BS_HIT_YOU]     = Classes[classid].weaponText[BS_HIT_YOU]
    player.weaponText[BS_HIT_VICTIM]  = Classes[classid].weaponText[BS_HIT_VICTIM]
    player.weaponText[BS_HIT_ROOM]    = Classes[classid].weaponText[BS_HIT_ROOM]
    player.stats[MAXHP]               = Classes[classid].maxhp
    player.stats[HP]                  = Classes[classid].maxhp
    player.stats[STEALTH]             = Classes[classid].stealth
    player.stats[CRITICAL]            = Classes[classid].critical
    player.stats[DODGE]               = Classes[classid].dodge
    player.classid                    = Classes[classid].classid
    player.stats[BS_MULTIPLIER]       = Classes[classid].bsmultiplier
    player.playerclass                = Classes[classid].name
    

def rest(player):
    """
    Set player in resting state.
    """
    
    combat.functions.endCombat(player)
    sendToPlayer( player, "You stop to rest." )
    sendToRoomNotPlayer( player, "{0} stops to rest.".format(player.name) )
    player.stats[RESTING] = True
    player.statLine()