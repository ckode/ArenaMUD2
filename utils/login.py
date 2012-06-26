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

from twisted.conch.telnet import ECHO

from utils.defines import LOGIN, PLAYING, GETCLASS, PURGATORY
from utils.defines import BLUE, WHITE, YELLOW, CYAN, LRED, SERVERVERSION
from utils.defines import PLAYERID, TOTALKILLS, TOTALDEATHS, ADMIN, HIGHKILLSTREAK
from utils.defines import PLAYERVISITS, PLAYERLASTVISIT, PLAYERCREATED, PLAYERPASSWD
from utils.defines import GETNEWPASSWORD, CREATEPLAYER, CONFIRMPASSWORD, GETPASSWORD
from utils.defines import GETNEWUSERNAME, CLEARSCREEN

#from utils.defines import ECHO, NOECHO

import utils.gameutils
import character.functions
import character.classes
import logger.gamelogger

# Python imports
import sqlite3


def askUsername(player):
    """
    getUsername()
    
    Ask user for a username.
    """

    player.transport.write("{0}Enter your login or type 'new':{1} ".format(YELLOW, WHITE))
    
    
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
    
    if player.status is LOGIN:
        # If "new", create new player. TODO: Setup the new character creation functionality 
        if line.lower() == "new":
            player.status = CREATEPLAYER
            createPlayer(player)
            return
    
    from character.players import AllPlayers               

    # Check to see if the player's name is already connected.
    for name in AllPlayers.keys():
        if line.lower() in name.lower():
            player.sendLine("User is already connected, please try again.")
            askUsername(player)
            return
    
    # See if player exists in database.
    if player.status is LOGIN:
        if utils.gameutils.userCheck(line):
            player.name = line
            player.loadPlayer()
            player.status = GETPASSWORD
            player.transport.write("Enter your password: ")
            return
        else:
            player.sendLine("Username entered does not exist, please try again.")
            askUsername(player)
            return
        
    elif player.status is GETNEWUSERNAME:
        # name can't be "new"
        if line.lower() == "new":
            player.sendLine("Invalid name, please try again.")
            player.status = LOGIN
            askUsername(player)
            return  
             
        if not utils.gameutils.userCheck(line):
            player.name = line[:1].upper() + line[1:]
            player.status = GETNEWPASSWORD
            # Disable local echo to not show passwords being typed.
            #player.transport._dont(ECHO)
            askPlayerPassword(player)
            return
        else:
            character.communicate.sendToPlayer(player, "Username already exist, please try again.")
            player.status = LOGIN
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
    player.sendLine("{0}Choose your class.".format(CLEARSCREEN))
    for each in character.classes.Classes.keys():
        player.sendLine(" - {0}) {1}".format(each, character.classes.Classes[each].name))
        
    player.transport.write("\r\nEnter your choice: ")
  
  
  
    
def getClass(player, line):
    """
    Get's the player's choice of character class.
    """    

    if line == "" or not line.isdigit():
        player.sendLine("Invalid choice, please try again.")
        askClass(player)
        return         
        
    choice = int(line)
    
    if choice in character.classes.Classes.keys():    
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
    
    
def getPasswd(player, line):
    """
    Get new password from player.
    """
      
    status = player.status
    
    if line == "" and status is GETNEWPASSWORD:
        character.communicate.sendToPlayer(player, "Blank passwords not allowed, please try again.")
        player.transport.write("Enter your password: ")   
        return
    
    if status == GETPASSWORD:
        if player.getAttr(PLAYERPASSWD) == utils.gameutils.hashPassword(line):
            player.save()
            player.status = GETCLASS
            askClass(player)
        else:
            character.communicate.sendToPlayer(player, "Password incorrect, please try again.")
            player.transport.write("Enter your password: ")
            return
        
    if status is GETNEWPASSWORD:
        player.newpasswd = utils.gameutils.hashPassword(line)
        player.status = CONFIRMPASSWORD
        askPlayerPassword(player)
        return
    
    elif status is CONFIRMPASSWORD:
        if player.newpasswd == utils.gameutils.hashPassword(line):
            player.setAttr(PLAYERPASSWD, player.newpasswd)
            # After passwords entered, reenable local echo.
            #player.transport._do(ECHO)
            
            # If player is being created, ask for class next.
            if player.getAttr(PLAYERID) is 0:
                player.status = GETCLASS
                player.createPlayer()
                askClass(player)
                return
            # Otherwise just change their passwords.
            else:
                character.communicate.sendToPlayer("Password changed.")
                player.status = PURGATORY
                player.save()
        else:
            player.status = GETNEWPASSWORD
            player.sendLine("Passwords did not match, please try again.")
            askPlayerPassword(player)
            return
                
        
            
def askPlayerPassword(player):
    """
    Ask player for new password.
    """
    
    status = player.status
    
    if status is GETNEWPASSWORD:
        player.transport.write("Enter new password: ")
        return
    elif status is CONFIRMPASSWORD:
        player.transport.write("Confirm new password: ")
        
    
    
def createPlayer(player):
    """
    Create new player.
    """
    
    status = player.status
    
    player.transport.write("Enter a new username: ")
    player.status = GETNEWUSERNAME
    return
    
    