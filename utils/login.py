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
from utils.defines import BLUE, WHITE, YELLOW, CYAN, LRED, SERVERVERSION
from utils.defines import PLAYERID, TOTALKILLS, TOTALDEATHS, ADMIN, HIGHKILLSTREAK
from utils.defines import PLAYERVISITS, PLAYERLASTVISIT, PLAYERCREATED, PLAYERPASSWD

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
    from utils.gameutils import welcomeScreen
    
    player.transport.write(welcomeScreen)
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
    for each in character.classes.Classes.keys():
        player.sendLine(" - {0}) {1}".format(each, character.classes.Classes[each].name))
        
    player.transport.write("\r\nEnter your choice: ")
  
  
  
    
def getClass(player, line):
    

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
    


    
def loadPlayer(player, name):
    """
    Loads player from the database.  If not exist, 
    return False.
    """
        
    from logger.gamelogger import logger
        
    sql = """SELECT id,
                    name,
                    passwd,
                    totalkills,
                    totaldeaths,
                    highestkillstreak,
                    visits,
                    adminlevel,
                    created,
                    lastvisit FROM players where name = {0} COLLATE NOCASE;""".format(name)
            
    try:
        conn = sqlite3.connect(os.path.join("data", "players.db"), detect_types=sqlite3.PARSE_DECLTYPE)
        cursor = conn.cursor()
        cursor.execute(sql)
            
        results = cursor.fetchall()
    
    except:
        logger.log.critical("Database errors using: players.db")
        
    
    if len(results) is 0:
        return False
    
    else:
        player.setAttr(PLAYERID, row[0])
        player.name = str(row[1])
        player.setAttr(PLAYERPASSWD, str(row[2]))
        player.setAttr(TOTALKILLS, row[3])
        player.setAttr(TOTALDEATHS, row[4])
        player.setAttr(HIGHKILLSTREAK, row[5])
        player.setAttr(PLAYERVISITS, row[6])
        player.setAttr(ADMIN, row[7])
        player.setAttr(PLAYERCREATED, row[8])
        player.setAttr(PLAYERLASTVISIT, row[9])
                       
    
    