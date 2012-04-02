#  ArenaMUD2 - A multiplayer combat game - http://arenamud.david-c-brown.com
#  Copyright (C) 2009, 2010 - David C Brown & Mark Richardson
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


# Twisted imports
from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor
from twisted.conch.telnet import TelnetTransport

# Python imports
import logging

# ArenaMUD2 imports
from config.gameconfig import Config, GameConfig
from logger.gamelogger import logger, console
from character.players import Player



class SonzoFactory(ServerFactory):
    """SonzoFactory is the Twisted network server for the game"""
    
    def __init__(self):
        """Initialize any attributes the server needs"""
        pass
        



#============================================
# Start Game
#============================================
def startup():
    """main()"""
    
    #Create server factory
    factory = SonzoFactory()

    factory.protocol = lambda: TelnetTransport(Player)
    reactor.listenTCP(GameConfig.port, factory)
    console("Starting ArenaMUD2 Version: NoDamnVersion -  A SonzoSoft Product.")
    reactor.run()

   



if __name__ == '__main__':
    """If main, start main()."""
    
    logger = logging.getLogger("ArenaMUD2")
    GameConfig = Config()
    startup()