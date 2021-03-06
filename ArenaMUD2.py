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


# Twisted imports
from twisted.internet.protocol import ServerFactory
from twisted.internet import reactor
from twisted.conch.telnet import TelnetTransport
from twisted.internet.task import LoopingCall

# Python imports
import sys

# ArenaMUD2 imports
import config.gameconfig
import utils.gameutils
import world.maps

#from config.gameconfig import GameConfig
from combat.queue import CombatQueue
from combat.functions import doCombatRound
from utils.gameutils import restHealing, naturalHealing, doRoomSpells
from utils.gameutils import doDurationEffectSpells, saveAllPlayers
import character.players
import logger.gamelogger
import character.classes
from world.items import loadItems
from utils.defines import SERVERVERSION



class SonzoFactory(ServerFactory):
    """SonzoFactory is the Twisted network server for the game"""
    
    def __init__(self):
        """Initialize any attributes the server needs"""
        self.combatQueue = CombatQueue()
        
       
    def TwoSecondLoop(self):
        """
        Run all events scheduled on a 2 second interval.
        """
        
       #doRoomSpells()
        doDurationEffectSpells()
     
    def FourSecondLoop(self):
        """
        Run all events scheduled on a 4 second interval.
        """

        # Do rest healing.
        restHealing()
        # Do combat round
        doCombatRound(self.combatQueue)  
       
    def FifteenSecondLoop(self):
        """
        Run all events scheduled on a 15 second interval.
        """

        naturalHealing()

    def SixtySecondLoop(self):
        """
        Run all events scheduled on a 60 second interval.
        """

        saveAllPlayers()
    

#============================================
# Start Game
#============================================
def startup():
    """main()"""
    
    config.gameconfig.GameConfig = config.gameconfig.Config()
    GameConfig = config.gameconfig.GameConfig
    logger.gamelogger.logger = logger.gamelogger.GameLogger(GameConfig)
    world.maps.World = world.maps.GameMap(GameConfig.maps[0])
    character.classes.Classes = character.classes.loadClasses()
    utils.gameutils.welcomeScreen = utils.gameutils.LoadAnsiScreens(GameConfig.motdPath)
    
    
    if character.classes.Classes is False or logger.gamelogger.logger is False:
        sys.exit(1)
    
    #Create server factory
    factory = SonzoFactory()

    factory.protocol = lambda: TelnetTransport(character.players.Player)
    reactor.listenTCP(GameConfig.port, factory)
    logger.gamelogger.logger.log.info("Starting ArenaMUD2 Version: {0}".format(SERVERVERSION))
    
    # 4 Second Loop
    TwoSecondLoop = LoopingCall(factory.TwoSecondLoop)
    TwoSecondLoop.start(2)    
    
    # 4 Second Loop
    FourSecondLoop = LoopingCall(factory.FourSecondLoop)
    FourSecondLoop.start(4)
    
    # 15 Second Loop
    FifteenSecondLoop = LoopingCall(factory.FifteenSecondLoop)
    FifteenSecondLoop.start(15)
     
    # 60 Second Loop
    SixtySecondLoop = LoopingCall(factory.SixtySecondLoop)
    SixtySecondLoop.start(60)    
    
    reactor.run()

   



if __name__ == '__main__':
    """If main, start main()."""

    startup()