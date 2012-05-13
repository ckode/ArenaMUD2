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
from character.classes import Classes
import combat.functions

from utils.defines import WHITE, LCYAN, LMAGENTA, GREEN, BLUE
from utils.defines import DIRS, OPPOSITEDIRS, DOWN, UP
from utils.defines import PURGATORY, PLAYING
from utils.defines import YOUHIT, YOUMISS, VICTIMHIT
from utils.defines import VICTIMMISS, ROOMHIT, ROOMMISS
from utils.defines import HP, MAXHP
from utils.defines import BLIND, HELD, STEALTH, VISION
from utils.defines import ATTACKS, ATTKSKILL, CRITICAL
from utils.defines import BONUSDAMAGE, DAMAGEABSORB
from utils.defines import KILLS, DEATHS, SNEAKING
from utils.defines import MAXDAMAGE, MINDAMAGE, RESTING
from utils.defines import MOVING, DODGE


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
            sendToPlayer( player, "You run into the floor!" )
            sendToRoomNotPlayer( player, "{0} ran into the floor!".format(player) )
            return
        elif direction is UP:
            sendToPlayer( player, "You run into the ceiling!" )
            sendToRoomNotPlayer( player, "{0} ran into the ceiling!".format(player) )            
            return
        else:
            sendToPlayer( player, "You run into the {0} wall!".format(DIRS[direction]) )
            sendToRoomNotPlayer( player, "{0} ran into the {1} wall!".format(player, DIRS[direction]) )     
            return
    else:
        player.stats[MOVING] = True
        reactor.callLater(.5, move, player, direction)
  
  
        
        
def move(player, direction):
    """
    Moves the character from one room to the next.
    """
    
    curRoom = world.maps.World.mapGrid[player.room]
    door = curRoom.dirs[direction]
    roomid = world.maps.World.doors[door].getExitRoom(curRoom.id)
    newRoom = world.maps.World.mapGrid[roomid]
    
    sendToRoomNotPlayer( player, "{0} left to the {1}.".format(player, DIRS[direction]) ) 
    del curRoom.players[player.name]
    newRoom.players[player.name] = player
    player.room = newRoom.id
    sendToRoomNotPlayer( player, "{0} entered from the {1}.".format(player, DIRS[OPPOSITEDIRS[direction]]) ) 
    displayRoom(player, player.room)
    player.stats[MOVING] = False
    

    
def displayRoom(player, room):
    """
    Display the room
    """
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
    player.stats[MAXHP]               = Classes[classid].maxhp
    player.stats[HP]                  = Classes[classid].maxhp
    player.stats[STEALTH]             = Classes[classid].stealth
    player.stats[CRITICAL]            = Classes[classid].critical
    player.stats[DODGE]               = Classes[classid].dodge
    player.classid                    = Classes[classid].classid
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