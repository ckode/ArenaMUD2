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

from character.players import LOGIN, PLAYING, AllPlayers

from logger.gamelogger import logger



def askUsername(player):
    """
    getUsername()
    
    Ask user for a username.
    """
    player.sendLine("Welcome to ArenaMUD2.")
    player.transport.write("Enter your login or type 'new': ")
    
    
def getUsername(player, line):
    """
    getUsername()
    
    Check for username or new and work.
    """
    
    player.name = line.capitalize()
    AllPlayers[player.name] = player
    logger.log.info( "{0} just logged in.".format(player) )
    player.STATUS = PLAYING
    
    from commands.communicate import tellWorld
    from world.maps import World
    
    tellWorld( player, "You have entered the battlefield!", "{0} has entered the battlefield!".format(player) )
    World.mapGrid[player.room].players[player.name] = player 
    World.mapGrid[player.room].displayRoom(player)