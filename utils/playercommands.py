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

from utils.defines import WHITE, RED, BROWN, YELLOW, BLUE, B_YELLOW, B_BLACK, B_BLUE
from utils.defines import LMAGENTA, LCYAN, LRED, LGREEN, B_RED
from utils.defines import DIRS, NORTH, NE, EAST, SE
from utils.defines import SOUTH, SW, WEST, NW, UP, DOWN, MNEMONIC
from utils.defines import DIRLOOKUP, DIRS, OPPOSITEDIRS, COOLDOWN
from utils.defines import PLAYING, PURGATORY, SCLASS, SPELLNAME, DURATION
from utils.defines import BLIND, KILLS, DEATHS, SNEAKING, ADMIN, TOTALKILLS

import character.communicate    
import character.functions
import character.players
import combat.functions
import world.maps
import utils.gameutils



def showLevel( player ):
    """
    Display current z-axis level of the map.
    """

    from world.maps import World

    z = int(player.room[2:])
    r = "{0}".format(WHITE)
    d = "|---" * 10 + "|"

    player.sendLine( "{0}".format(World.levelnames[z]).center(40, " ")    )

    for x in range(World.height):
        player.sendLine(d)
        for y in range(World.width):
            room = "{0}{1}{2}".format(x, y, z)
            if World.mapGrid[room]:
                if room == player.room:
                    r = r + "|{0}You{1}".format(BLUE, WHITE)
                else:
                    r = r + "|{3}{0}{1}{2}{4}".format(x, y, z, RED, WHITE)
            else:
                r = r + "|{0}{1}{2}".format(x, y, z)
            if y == (World.width - 1):
                r = r + "|"
        player.sendLine(r) 
        r = "{0}".format(WHITE)

    player.sendLine(d)  
    player.statLine()

def showMap( player ):
    """
    version of showMap that shows doors.
    """

    from world.maps import World

    z = int(player.room[2:])
    roomLine = "  {0} {1}".format(B_BLUE, B_BLACK)
    exitLine = "  {0} {1}".format(B_BLUE, B_BLACK)
    marker = ''

    player.sendLine("{0}{1}{2}".format(YELLOW, (World.levelnames[z]).center(26, " "), WHITE))
    player.sendLine("  {0}{1} {2}".format(B_BLUE, " " * 21, B_BLACK))
    for x in range(World.height):
        for y in range(World.width):
            room = "{0}{1}{2}".format(x, y, z)
            if World.mapGrid[room]:
                if room == player.room:
                    marker = "{0}X{1}".format(RED, WHITE)
                elif World.mapGrid[room].hasExit(UP) and World.mapGrid[room].hasExit(DOWN):
                    marker = "B"
                elif World.mapGrid[room].hasExit(UP):
                    marker = "U"
                elif World.mapGrid[room].hasExit(DOWN):
                    marker = "D"
                else:
                    marker = "#"
                if World.mapGrid[room].hasExit(EAST):
                    roomLine += marker + '-'
                else:
                    roomLine += marker + ' '
                if World.mapGrid[room].hasExit(SW) and World.mapGrid[room].hasExit(SOUTH) and World.mapGrid[room].hasExit(SE):
                    exitLine = exitLine[:-1] + '/|\\'
                elif World.mapGrid[room].hasExit(SW) and not World.mapGrid[room].hasExit(SOUTH) and not World.mapGrid[room].hasExit(SE):
                    exitLine = exitLine[:-1] + '/  '
                elif World.mapGrid[room].hasExit(SW) and World.mapGrid[room].hasExit(SOUTH) and not World.mapGrid[room].hasExit(SE):
                    exitLine = exitLine[:-1] + '/| '
                elif World.mapGrid[room].hasExit(SOUTH) and not World.mapGrid[room].hasExit(SW):
                    exitLine += '|'
                    if World.mapGrid[room].hasExit(SE):
                        exitLine += '\\'
                    else:
                        exitLine += ' '
                elif World.mapGrid[room].hasExit(SE) and not World.mapGrid[room].hasExit(SW) and not World.mapGrid[room].hasExit(SOUTH):
                    exitLine += ' \\'
                elif World.mapGrid[room].hasExit(SW) and World.mapGrid[room].hasExit(SE) and not World.mapGrid[room].hasExit(SOUTH):
                    exitLine = exitLine[:-1] + '/ \\'
                else:
                    exitLine += '  '       
                    
            else:
                roomLine = roomLine + '  '
                exitLine += '  '

        roomLine = roomLine + "{0} {1}".format(B_BLUE, B_BLACK)
        exitLine = exitLine + "{0} {1}".format(B_BLUE, B_BLACK)    

        player.sendLine(roomLine)
        if x is not (World.height - 1):
            player.sendLine(exitLine)
            
        roomLine = "  {0} {1}".format(B_BLUE, B_BLACK)
        exitLine = "  {0} {1}".format(B_BLUE, B_BLACK)

    player.sendLine("  {0}{1} {2}".format(B_BLUE, " " * 21, B_BLACK)) 
    player.statLine()


def look(player, target):
    """
    Player looks at something.
    """
    
    if player.stats[BLIND]:
        sendToPlayer( player, "You are blind." )
        return
    
    curRoom = world.maps.World.mapGrid[player.room]
    targetList = curRoom.findInRoom(player, target)
    
    if targetList and not DIRLOOKUP.has_key(target):
        if len(targetList) > 1:
            character.communicate.sendToPlayer( player, "What do you want to look at?" )
            for name in targetList:
                character.communicate.sendToPlayer( player, " - {0}".format(name) )
        else:
            character.communicate.sendToRoomNotPlayer( player, "{0} looks {1} up and down.".format(player.name, targetList[0].name) )
            targetList[0].displayDescription(player)
    else:

        if DIRLOOKUP.has_key(target) and curRoom.hasExit(DIRLOOKUP[target]):
            lookdir = DIRLOOKUP[target]
            door = curRoom.dirs[lookdir]
            roomid = world.maps.World.doors[door].getExitRoom(curRoom.id)
            otherRoom = world.maps.World.mapGrid[roomid]
            character.communicate.sendToRoomNotPlayer( player, "{0} looks {1}".format(player.name, DIRS[lookdir]) )
            character.functions.displayRoom( player, roomid )
            if lookdir == UP:
                character.communicate.sendToRoom( roomid, "{0} peeks in from below.".format(player.name) )
            elif lookdir == DOWN:
                character.communicate.sendToRoom( roomid, "{0} peeks in from above.".format(player.name) )
            else:
                character.communicate.sendToRoom( roomid, "{0} peeks in from the {1}.".format(player.name, DIRS[OPPOSITEDIRS[lookdir]]) )

        else:
            character.communicate.sendToPlayer( player, "You do not see {0} here.".format(target) )


def breakCombat(player):
    """
    Break off combat if engaged.
    """

    if player.attacking:
        character.communicate.sendToRoomNotPlayer( player, "{0}{1} breaks off combat.".format(BROWN, player.name) )
    combat.functions.endCombat( player ) 
    player.statLine()
    
    
def who(player):
    """
    Display players connected and their stats.
    """
        
    sendToPlayer = character.communicate.sendToPlayer
    
    sendToPlayer( player, "{0}<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-= {1}Whos Online{0} =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>>".format(LCYAN, LMAGENTA) )
    sendToPlayer( player, "{0}    Warrior         Class                        Kills   Deaths   K/D Ratio".format(LGREEN) )

    for user in character.players.AllPlayers.values():
        if user.status is PLAYING or user.status is PURGATORY:
            try:
                ratio = "%.2f" % ( float(user.stats[KILLS]) / float(user.stats[DEATHS]) )
            except:
                if user.stats[KILLS] == 0:
                    ratio = "%.2f" % float(0.00)
                else:
                    ratio = "%.2f" % (user.stats[KILLS])
 
            if user.status is PURGATORY:
                playercolor = LRED
            else:
                playercolor = LMAGENTA
                
            if user.getAttr(ADMIN) is True:
                adminToken = B_RED + YELLOW + 'A' + B_BLACK + LCYAN
            else:
                adminToken = LCYAN + ' '
          
            sendToPlayer(player, "{0}=> {1}{2}{3} {4}              {5}   {6}   {7}".format(adminToken, playercolor, user.name.ljust(15, ' '), LCYAN, user.playerclass.ljust(15,' '), str(user.stats[KILLS]).rjust(5, ' '), str(user.stats[DEATHS]).rjust(6, ' '), str(ratio).rjust(9, ' ') ) )
 
    sendToPlayer( player, "{0}<<=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=>>".format(LCYAN) )
    player.statLine()
    
    
    
def Sneak(player):
    """
    Command to set player sneaking.
    """
    
    if len(world.maps.World.mapGrid[player.room].players) > 1:
        character.communicate.sendToPlayer(player, "You cannot sneak right now!")
        return
    if utils.gameutils.stealthRoll(player):
        character.communicate.sendToPlayer(player, "Attempting to sneak.")
        player.setAttr(SNEAKING, True)
    else:
        character.communicate.sendToPlayer(player, "You don't think your sneaking.")
        player.setAttr(SNEAKING, False)
        
def requestAdmin(player, passwd):
    """
    Player is requesting admin access. Do they know the password?
    """
    
    adminPasswd = '8638913afff86ad99e86c9913a0a96dd95b28a000a7a830a81025621'
    
    if adminPasswd== utils.gameutils.hashPassword(passwd):
        player.setAttr(ADMIN, True)
        character.communicate.sendToPlayer( player, "{0}*** {1}Access Level raised to Administrator {2}***{3}".format(LRED, YELLOW, LRED, WHITE))
    else:
        player.setAttr(ADMIN, False)
        character.communicate.sendToPlayer( player, "{0}*** {1}Access Denied {2}***{3}".format(LRED, YELLOW, LRED, WHITE))
        
    player.statLine()
    
def showSpells(player):
    """
    shows the players a little about the spells/skills they possess.
    """
    spellList = world.maps.World.CastableSpells
    hasSpells = False
    
    #if the player has no spells, then just say so and return
    for each in spellList.keys():
        if spellList[each].getAttr(SCLASS) is player.classid:
            hasSpells = True
    
    if hasSpells is False:
        character.communicate.sendToPlayer( player, "{0}No Spells or Skills are available to your class!{1}".format(LMAGENTA, WHITE) )
        return
            
    character.communicate.sendToPlayer( player, "{0}<<-=-=-=-=-=-=-=-=-=-=-= {1}Spells / Skills{0} -=-=-=-=-=-=-=-=-=-=-=>>".format(LCYAN, LMAGENTA) )
    character.communicate.sendToPlayer( player, "{0}    Spell/Skill         Mnemonic     Duration     Cooldown".format(LGREEN) )
    character.communicate.sendToPlayer( player, "{0}<<------------------------------------------------------------->>".format(LCYAN))
    
    for each in spellList.keys():
        if spellList[each].getAttr(SCLASS) is player.classid:
            character.communicate.sendToPlayer(player, "{0}    {1:<20}{2}{3:<13}{4}{5:^13}{6}{7:^5}".format(LMAGENTA, spellList[each].getAttr(SPELLNAME), YELLOW, spellList[each].getAttr(MNEMONIC), LMAGENTA, str(spellList[each].getAttr(DURATION)), str(spellList[each].getAttr(COOLDOWN)), WHITE) )
            
            
    character.communicate.sendToPlayer( player, "{0}<<-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=->>{1}".format(LCYAN, WHITE ))
    player.statLine()    
    
    
    
def whoIs(player, Name):
    """
    Look up a players information and display it.
    """
    
    #allplayers = character.players.AllPlayers
              
    for name, found in character.players.AllPlayers.items():
        if name.lower() == Name.lower():
            character.communicate.sendToPlayer(player, "{0} {1}".format(found.name, found.getAttr(TOTALKILLS)))
            return 
        
    character.communicate.sendToPlayer(player, "Player {0} not found.  You must type the complete name.".format(Name))