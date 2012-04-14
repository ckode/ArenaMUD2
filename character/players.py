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

 
AllPlayers = {} 

# Twisted imports
from twisted.conch.telnet import StatefulTelnetProtocol

# ArenaMUD2 imports

import world.maps

import logger.gamelogger
import commands.parser
import character.communicate
from utils.defines import BLUE, WHITE 
from utils.defines import DELETELEFT, FIRSTCOL
from utils.defines import PLAYING, LOGIN, PURGATORY


# Python imports



#===========================================
# Player class. 
#
# All players are of this type
#===========================================
class Player(StatefulTelnetProtocol):
    """
    Player character class. Sub-class of Character. Each user is defined by Player.
    """
    
    def __init__(self):
        """
        Player->__init__()
        
        Initialize the Player class object
        """
        self.status = LOGIN
        self.IP = None
        self.room = "000"
        self.name = "Unknown"
        
        
        self.resting = False
        self.moving = False
        self.held = False
        self.blind = False
        self.vision = 3
        
        
        
    def __repr__(self):
        """
        Player->__call__()
        """
        return self.name
    
    
    def connectionMade(self):
        """
        Player->connectionMade(): Overrides Twisted's method.
        
        Called when someone connects to the server.
        """
     
        self.IP = self.transport.getPeer().host
        logger.gamelogger.logger.log.info("{0} CONNECTED!".format(self.IP))
        
        # Check for max players 
        from config.gameconfig import GameConfig
        if len(AllPlayers) >= GameConfig.maxplayers:
            logger.gamelogger.logger.log.info("To many connected.  Refusing new client: {0}".format(self.IP))
            self.sendLine(player, "Too many connections, try again later.")
            self.disconnectClient()
        
        from utils.login import askUsername    
        askUsername(self)    
        
            
    def disconnectClient(self):
        """
        Player->disconnectClient()  Overrides Twisted's method.
        
        Disconnect a client and clean up game information.
        """
              
        # Remove from AllPlayers before disconnecting
        if AllPlayers.has_key(self.name):
            # replace del with function to do full cleanup.
            character.communicate.tellWorld(player, "Goodbye!", "{0}{1} has quit!!!".format(BLUE, player.name) )
            logger.gamelogger.logger.log.info( "{0} just logged off.".format(self.name) )
            del AllPlayers[self.name]
            del world.maps.World.mapGrid[self.room].players[self.name]
            
        self.transport.loseConnection()
      
      
    def connectionLost(self, reason):
        """
        Player->connectionList()  Overrides Twisted's method.
        
        Player lost connection.  Clean up.
        """
        
        # Remove from AllPlayers before disconnecting
        if AllPlayers.has_key(self.name):
            logger.gamelogger.logger.log.info( "{0} just hung up!!!".format(self.name) )
            # replace del with function to do full cleanup.
            character.communicate.tellWorld(self, None, "{0}{1} just hung up!!!".format(BLUE, self.name) )
            del AllPlayers[self.name]
            del world.maps.World.mapGrid[self.room].players[self.name]
      
    
    def lineReceived(self, line):
        """
        Player->lineReceived()  Overrides Twisted's method.
        
        Handles lines received from the client.
        """
        
        commands.parser.GameParser(self, line)
        
        
        
   
    def statLine(self):
        """
        Player->statLine(self)
        
        Displays players statline.
        """
        self.transport.write(DELETELEFT)
        self.transport.write(FIRSTCOL)
        self.transport.write("[Fake Statline]: " + WHITE)        
        