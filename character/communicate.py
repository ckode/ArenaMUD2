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

import character.players 
import world.maps

from utils.defines import WHITE, LBLUE, LGREEN, MAGENTA
from utils.defines import DELETELEFT, FIRSTCOL
from utils.defines import PLAYING, PURGATORY




def say( player, line ):
    """
    say()
    
    Say something to the room you are in.
    """
    
    sendToPlayer(player, "{1}You said:{2} {0}".format(line, LGREEN, WHITE) )
    sendToRoomNotPlayer(player, "{2}{0} says:{3} {1}".format(player, line, LGREEN, WHITE) )    
            

 
 
def sendToRoom(roomid, line):
    """
    sendToRoom(self, line)
    
    Send text to everyone in the room.
    """
     
    World = world.maps.World            
    for _player in world.maps.World.mapGrid[roomid].players.keys():
        sendToPlayer(character.players.AllPlayers[_player], line)
            
def sendToRoomNotPlayer(player, line):
    """
    sendToRoomNotPlayer(self, line)
    
    Send text to everyone in the room except the player.
    """
     
    World = world.maps.World            
    for _player in world.maps.World.mapGrid[player.room].players.keys():
        if player.name is not _player:
            sendToPlayer(character.players.AllPlayers[_player], line)
            

def sendToRoomNotPlayerOrVictim(player, victim, line):
    """
    sendToRoomNotPlayerOrVictim(self, line)
    
    Send text to everyone in the room except the player or
    victim.  Usually used in combat.
    """
     
    World = world.maps.World            
    for _player in world.maps.World.mapGrid[player.room].players.keys():
        if player.name is not _player and victim.name is not _player:
            sendToPlayer(character.players.AllPlayers[_player], line)

            
 
def sendToPlayer(player, line):
    """
    Player->sendToPlayer(self, line):
          
    Handles any flags before any sending
    text to the player.
    """
                
    player.transport.write(DELETELEFT)
    player.transport.write(FIRSTCOL)
    player.sendLine(line + WHITE)
    if player.status == PLAYING or player.status == PURGATORY:
        player.statLine()        
 
           
def tellWorld( player, playerMsg, OtherPlayersMsg ):
    """
    tellWorld(player, playerMsg, OtherPlayersMsg)
    
    Tell everyone connected a message.  
    
    playerMsg is message to tell the Player. "None" for 
    no message.
    
    OtherPlayerMsg is the message to tell all other
    players in the game. (cannot be None)
    """
    
    if playerMsg is not None:
        sendToPlayer( player, "{1}{0}{2}".format(playerMsg, LBLUE, WHITE) )    
        
    for client in character.players.AllPlayers.values(): 
        if client is not player and (client.status is PLAYING or client.status is PURGATORY):
            sendToPlayer( client, "{1}{0}{2}".format(OtherPlayersMsg, LBLUE, WHITE) )    
    
    
    
def gossip( player, msg):
    """
    Shouts messages to all players with 
    player.status = playing
    """
    for client in character.players.AllPlayers.values(): 
        if client.status is PLAYING or client.status is PURGATORY:
            if player.status is PURGATORY:
                sendToPlayer( client, "{0}{1} gossips (purgatory): {2}".format(MAGENTA, player.name, msg) )     
            else:
                sendToPlayer( client, "{0}{1} gossips: {2}".format(MAGENTA, player.name, msg) )     
        
            
    