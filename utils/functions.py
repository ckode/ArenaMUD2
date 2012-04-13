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

import commands.communicate
from utils.defines import WHITE
from utils.defines import DIRS
from utils.defines import PURGATORY


def movePlayer(player, direction):
    """
    Moves player from one room to another.
    """
        
    # If player died before the move occured, do nothing
    if player.status == PURGATORY:
        return
        
    player.resting = False
             
    if player.held:
        player.moving = False
        sendToPlayer( player, "You cannot move!" )           
        
    commands.communicate.tellWorld( player, "{1}You can't go {0}, move isn't implemented yet!".format(DIRS[direction], WHITE), 
                       "{2}{0} tried to go {1}, but move isn't implemented yet!".format(player, DIRS[direction], WHITE) )