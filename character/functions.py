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
from world.maps import World
from utils.defines import WHITE, LCYAN, LMAGENTA, GREEN
from utils.defines import DIRS, OPPOSITEDIRS, DOWN, UP
from utils.defines import PURGATORY


def movePlayer(player, direction):
    """
    Moves player from one room to another.
    """
        
    # If player died before the move occured, do nothing
    if player.status == PURGATORY:
        return
        
    player.resting = False
             
    if player.moving is True:
        sendToPlayer( player, "You are already moving, slow down!" )
        return
    
    if player.held:
        player.moving is False
        sendToPlayer( player, "You cannot move!" )           
        
    curRoom = World.mapGrid[player.room]
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
        player.moving = True
        reactor.callLater(.5, move, player, direction)
  
  
        
        
def move(player, direction):
    """
    Moves the character from one room to the next.
    """
    
    curRoom = World.mapGrid[player.room]
    door = curRoom.dirs[direction]
    roomid = World.doors[door].getExitRoom(curRoom.id)
    newRoom = World.mapGrid[roomid]
    
    sendToRoomNotPlayer( player, "{0} left to the {1}.".format(player, DIRS[direction]) ) 
    del curRoom.players[player.name]
    newRoom.players[player.name] = player
    player.room = newRoom.id
    sendToRoomNotPlayer( player, "{0} entered from the {1}.".format(player, DIRS[OPPOSITEDIRS[direction]]) ) 
    displayRoom(player, player.room)
    player.moving = False
    

    
def displayRoom(player, room):
    """
    Display the room
    """
    curRoom = World.mapGrid[room]
    
    if player.blind:
        sendToPlayer( player, "{0}You are blind.".format(WHITE) )
        return
        
    if player.vision < curRoom.light:
        sendToPlayer( player, "{0}You cannot see anything, it's too dark.".format(WHITE) )
        return
     
        
    sendToPlayer( player, "{0}{1}".format(LCYAN, curRoom.name) )
      
    playersinroom = curRoom.whosInRoom(player)
    if playersinroom is not None:
        sendToPlayer( player, "{0}Also here:{1} {2}".format(GREEN, LMAGENTA, playersinroom) )
            
    sendToPlayer( player, "{0}Obvious exits: {1}{2}".format(GREEN, curRoom.getExits(), WHITE) )
        
        
        
def spawnPlayer( player ):
    """
    Spawn the player in the map.
    """
    
    room = random.sample(World.roomsList, 1)[0]
    player.room = room
    World.mapGrid[room].players[player.name] = player