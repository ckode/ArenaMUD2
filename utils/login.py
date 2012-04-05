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



def askUsername(player):
    """
    getUsername()
    
    Ask user for a username.
    """
    
    player.transport.write("Enter your login or type 'new': ")
    
    
def getUsername(player, line):
    """
    getUsername()
    
    Check for username or new and work.
    """
    
    player.name = line
    AllPlayers[player.name] = player
    player.STATUS = PLAYING