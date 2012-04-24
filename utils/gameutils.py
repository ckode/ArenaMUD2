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

from character.players import AllPlayers

from utils.defines import PLAYING
from utils.defines import CYAN, YELLOW

import character.communicate

def restHealing():
    """
    If player resting, rest heal him.
    """
    
    healRate = 15
    for player in AllPlayers.values():
        # If player isn't playing.  No need to heal
        if player.status is not PLAYING:
            continue
        if player.resting:
            if (player.hp + healRate) > player.maxhp:
                player.hp = player.maxhp
            else:
                player.hp += healRate
                
            player.statLine()
            
            
            
def naturalHealing():
    """
    Natural healing loop.
    """
    
    healRate = 5
    for player in AllPlayers.values():
        # If player isn't playing.  No need to heal
        if player.status is not PLAYING:
            continue        
        if (player.hp + healRate) > player.maxhp:
            player.hp = player.maxhp
        else:
            player.hp += healRate
            
        player.statLine()
        
        
def purgatoryHelpMsg(player):
    character.communicate.sendToPlayer( player, "{0}Command had no effect. Type '{1}spawn{0}' to spawn or type '{1}help{0}' for help.".format(CYAN, YELLOW) )