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

from ConfigParser import ConfigParser 
import logger.gamelogger
import world.maps
import sys




    
#==================================================
# Class Config
#
# All configurations read from the config file
# are read into this configurations object
# as GameConfig.  It is loaded at start up
#==================================================
class Config():
    """
    Config class reads the configuration file and
    loads it into a global configurations object 
    that the game can access.
    """
    
    def __init__(self):
        """Initializes the config object"""
        
        self.configFile          = "ArenaMUD2.cfg"
          
        self.loadConfig(self.configFile)
        
        
    def loadConfig(self, cfg):
        """
        Load configuration file from disk
        """

        # Load the config file
        config = ConfigParser()
        try:
            config.readfp(open(cfg))
        except IOError as (errno, strerror):
            print "I/O error opening {0}: {1}".format(cfg, strerror) 
            sys.exit(1)
        except:
            print "Configuration Error: Failure loading configuration file."
            sys.exit(1)            
        
        try:
            self.name               = config.get("ArenaMUD2", "ServerName")
            self.port               = config.getint("ArenaMUD2", "ServerPort")
            self.maxplayers         = config.getint("ArenaMUD2", "MaxPlayers")
            self.datadir            = "data/"      #config.get("ArenaMUD2", "DataDirectory")
            self.mapsdir            = "maps/"      #config.get("ArenaMUD2", "MapsDirectory")
            self.maps               = config.get("ArenaMUD2", "MapList").split()
            self.logFile            = config.get("ArenaMUD2", "LogFile")         
            self.logLevel           = config.getint("ArenaMUD2", "LogLevel")
            self.consoleLogLevel    = config.getint("ArenaMUD2", "ConsoleLogLevel")
        except:
            print "Configuration Error: Failure loading configuration file."
            sys.exit(1)



# Initialize game config and game logging
GameConfig = Config()
logger.gamelogger.logger = logger.gamelogger.GameLogger(GameConfig)
world.maps.World = world.maps.GameMap(GameConfig.maps[0])