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

from character.players import AllPlayers, LOGIN
from utils.login import getUsername


def GameParser(player, line):
    """
    GameParser()
    
    Parses information send my client and
    makes decisions based on that information.
    """
    
    # Probably make a "status" checker function to handle status not PLAYING.
    if player.STATUS is LOGIN:
        getUsername(player, line)
        return
    
    player.sendLine( "You said: {0}".format(line) )
    
    for client in AllPlayers.values():     
        if client is not player:
            client.sendLine( "{0}: {1}".format(player, line) )
        
            
