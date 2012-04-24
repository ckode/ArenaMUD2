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
from utils.defines import HP, MAXHP, POWER, MAXPOWER
from utils.defines import BLIND, HELD, STEALTH, VISION
from utils.defines import ATTACKS, ATTKSKILL, CRITICAL
from utils.defines import BONUSDAMAGE, DAMAGEABSORB
from utils.defines import KILLS, DEATHS, SNEAKING, MOVING
from utils.defines import MAXDAMAGE, MINDAMAGE, RESTING


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

        self.stats = { HP:              0,
                       MAXHP:           0,
                       POWER:           0,
                       MAXPOWER:        0,
                       BLIND:           False,
                       HELD:            False,
                       VISION:          3,
                       STEALTH:         0,
                       SNEAKING:        False,
                       ATTACKS:         0,
                       ATTKSKILL:       0,
                       MAXDAMAGE:       0,
                       MINDAMAGE:       0,
                       BONUSDAMAGE:     0,
                       DAMAGEABSORB:    0,
                       CRITICAL:        0,
                       KILLS:           0,
                       DEATHS:          0,
                       MOVING:          False
                     }

        self.weaponText = {}
        self.powerDesc = ""
        self.attacking = None
        self.spells = {}

        




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
            character.communicate.tellWorld(self, None, "{0}{1} has logged off.".format(BLUE, self.name) )
            self.sendLine("Goodbye!")
            logger.gamelogger.logger.log.info( "{0} just logged off.".format(self.name) )
            if self.status is PLAYING:
                del world.maps.World.mapGrid[self.room].players[self.name]            
            del AllPlayers[self.name]
            

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
            if self.status is PLAYING:
                del world.maps.World.mapGrid[self.room].players[self.name]
            del AllPlayers[self.name]
            


    def lineReceived(self, line):
        """
        Handles lines received from the client.
        """

        utils.parser.GameParser(self, line)




    def statLine(self):
        """
        Displays players statline.
        """

        if self.status is PURGATORY:
            self.transport.write( "{0}%>".format(WHITE) )
            return
        
        statline = "[HP={0}/{1}={2}]: ".format(self.stats[HP], self.powerDesc, self.stats[POWER]) 
        if self.stats[RESTING]:
            statline = "{0}{1} ".format(statline, "(resting) ")
        self.transport.write(DELETELEFT)
        self.transport.write(FIRSTCOL)
        self.transport.write( "{0}{1}".format(WHITE, statline) )        



    def resetStats(self):
        """
        Resets a players stats before respawning.
        """

        character.functions.applyClassAttributes( self, self.classid )
        self.stats[HP] = self.stats[MAXHP]
        self.stats[POWER] = self.stats[MAXPOWER]
        self.stats[SNEAKING] = False
        self.stats[RESTING] = False
        self.stats[MOVING] = False
        self.stats[HELD] = False
        self.stats[BLIND] = False
        self.stats[BONUSDAMAGE] = 0
        self.stats[DAMAGEABSORB] = 0
        self.spells.clear()
        self.attacking = None


    def displayDescription(self, player):
        """
        Displays a description of the player.
        """
        character.functions.sendToPlayer( player, "{0} is a {1}".format(self.name, self.playerclass) )