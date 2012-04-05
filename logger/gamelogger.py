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

import logging




class GameLogger:
    """
    GameLogger Class
    """
    
    def __init__(self, config):
        """
        Init GameLogger class object.
        """

        # store log levels in the class object
        self.logLevel = config.logLevel
        self.consoleLogLevel = config.consoleLogLevel
                
        # create logger
        self.log = logging.getLogger("ArenaMUD2")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        self.log.setLevel(logging.DEBUG)
        
        # create log file handler and set log level
        self.logFile = logging.FileHandler("ArenaMUD2.log")
        self.logFile.setLevel(self.logLevel)
        self.logFile.setFormatter(formatter)
        
        # create console handler and set log level
        self.console = logging.StreamHandler()
        self.console.setLevel(self.consoleLogLevel)
        self.console.setFormatter(formatter)
                            
        # add handlers to the logger object
        self.log.addHandler(self.logFile)
        self.log.addHandler(self.console)
        
    
    def setConsoleLogLevel(self, level):
        """
        setConsoleLogLevel()
        
        Allow you to change the console's log level.
        """
        
        self.consoleLogLevel = level
        self.console.setLevel(self.consoleLogLevel)
        
        
    def setLogLevel(self, level):
        """
        setLogLevel()
        
        Allows you to change the log level of the file logger.
        """

        self.logLevel = level
        self.logFile.setLevel(self.logLevel)
    
    
logger = None

  