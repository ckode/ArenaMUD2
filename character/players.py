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
import utils.parser
import character.communicate
import character.functions 
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
    Player character class. 
    """
    
    def __init__(self):
        """
        Initialize the Player class object
        """

        self.status = LOGIN
        self.IP = None
        self.room = ""
        self.name = "Unknown"
        self.playerclass = ""
        self.classid = 0
        
        # Combat
        self.attacks = 0
        self.attkSkill = 0
        self.critical = 0
        self.maxDamage = 0
        self.minDamage = 0
        self.weaponText = {}
        self.maxPower = 100
        self.power = 100
        self.powerDesc = ""
        self.hp = 0
        self.maxhp = 0
        self.steath = 0
        
        self.sneaking = False
        self.resting = False
        self.moving = False
        self.held = False
        self.blind = False
        self.vision = 3
        
        self.attacking = None
        
        
                
        
    def __repr__(self):
        """
        Player->__call__()
        """
        return self.name
    
    
    def connectionMade(self):
        """
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
        Disconnect a client and clean up game information.
        """
              
        # Remove from AllPlayers before disconnecting
        if AllPlayers.has_key(self.name):
            # replace del with function to do full cleanup.
            character.communicate.tellWorld(self, None, "{0}{1} has quit!!!".format(BLUE, self.name) )
            self.sendLine("Goodbye!")
            logger.gamelogger.logger.log.info( "{0} just logged off.".format(self.name) )
            del AllPlayers[self.name]
            del world.maps.World.mapGrid[self.room].players[self.name]
            
        self.transport.loseConnection()
      
      
    def connectionLost(self, reason):
        """
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
        Handles lines received from the client.
        """
        
        utils.parser.GameParser(self, line)
        
        
        
   
    def statLine(self):
        """
        Displays players statline.
        """
        
        statline = "[HP={0}/{1}={2}]: ".format(self.hp, self.powerDesc, self.power) 
        if self.resting:
            statline = "{0}{1} ".format(statline, "(resting) ")
        self.transport.write(DELETELEFT)
        self.transport.write(FIRSTCOL)
        self.transport.write( "{0}{1}".format(WHITE, statline) )        
        
        
        
    def resetStats(self):
        """
        Resets a players stats before respawning.
        """
        
        character.functions.applyClassAttributes( self, self.classid )
        self.hp = self.maxhp
        self.power = self.maxPower
        self.sneaking = False
        self.resting = False
        self.moving = False
        self.held = False
        self.blind = False
        self.attacking = None