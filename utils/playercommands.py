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

from utils.defines import WHITE, RED, BROWN, YELLOW, BLUE
from utils.defines import DIRLOOKUP, DIRS, OPPOSITEDIRS
import character.communicate    
import character.functions
import combat.functions
import world.maps
from utils.defines import DIRS, NORTH, NE, EAST, SE
from utils.defines import SOUTH, SW, WEST, NW, UP, DOWN


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
    roomLine = "{0}".format(WHITE)
    exitLine = "{0}".format(WHITE)
    marker = ''

    player.sendLine("{0}{1}{2}".format(YELLOW, (World.levelnames[z]).center(27, " "), WHITE))

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
                    marker = '#'
                if World.mapGrid[room].hasExit(EAST) and World.mapGrid[room].hasExit(WEST):
                    roomLine += '-' + marker + '-'
                elif World.mapGrid[room].hasExit(WEST):
                    roomLine += '-' + marker + ' '
                elif World.mapGrid[room].hasExit(EAST):
                    roomLine += ' ' + marker + '-'
                else:
                    roomLine += ' ' + marker + ' '
                if World.mapGrid[room].hasExit(SW):
                    exitLine += '/'
                else:
                    exitLine += ' '
                if World.mapGrid[room].hasExit(SOUTH):
                    exitLine += '|'
                else:
                    exitLine += ' '
                if World.mapGrid[room].hasExit(SE):
                    exitLine += '\\'
                else:
                    exitLine += ' '
            else:
                if y==0:
                    roomLine += '  '
                    exitLine += '  '
                    continue
                if y == (World.width - 1):
                    roomLine += '  '
                    exitLine += '  '
                    continue

                roomLine = roomLine + '   '
                exitLine += '   '

        player.sendLine(roomLine)
        player.sendLine(exitLine)
        roomLine = "{0}".format(WHITE)
        exitLine = "{0}".format(WHITE)


    player.statLine()


def look(player, target):
    """
    Player looks at something.
    """
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