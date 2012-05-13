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

from utils.defines import LOGIN, PLAYING, GETCLASS, PURGATORY
from utils.defines import BLUE, WHITE, YELLOW, CYAN
import utils.gameutils
import character.functions
from character.classes import Classes
import logger.gamelogger




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
    
    # not blank, 15 characters or less and all characters are alpha or numberic
    if line == "" or len(line) > 15 or not line.isalnum():
        player.sendLine("Invalid name, please try again.")
        askUsername(player)
        return  
    
    from character.players import AllPlayers                    
    player.name = line[:1].upper() + line[1:]
    if player.name in AllPlayers.keys():
        player.sendLine("Name already exists, please try again.")
        askUsername(player)
        return          
       
    logger.gamelogger.logger.log.info( "{0} just logged in.".format(player) )
    player.status = GETCLASS
    askClass(player)

    
    
    
def askClass(player):
    """
    getUsername()
    
    Ask user for a username.
    """
    player.sendLine("Choose your class.")
    for each in Classes.keys():
        player.sendLine(" - {0}) {1}".format(each, Classes[each].name))
        
    player.transport.write("\r\nEnter your choice: ")
  
  
  
    
def getClass(player, line):
    

    if line == "" or not line.isdigit():
        player.sendLine("Invalid choice, please try again.")
        askClass(player)
        return         
        
    choice = int(line)
    
    if choice in Classes.keys():    
        from world.maps import World
        from character.players import AllPlayers        
        AllPlayers[player.name] = player
        character.functions.applyClassAttributes(player, choice)
        
        player.status = PURGATORY
    
        from character.communicate import tellWorld, sendToRoomNotPlayer
        from world.maps import World
    
        tellWorld( player, "Welcome!", "{0} has joined!".format(player.name) )
        utils.gameutils.purgatoryHelpMsg(player)
   
    else:
        player.sendLine("Invalid choice, please try again.")
        askClass(player)
        return            
        
    