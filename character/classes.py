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

import sqlite3
import os

from utils.defines import YOUHIT, YOUMISS, VICTIMHIT, VICTIMMISS
from utils.defines import ROOMHIT, ROOMMISS

class PlayerClass:
    """
    ArenaMUD Player Classes
    """
    
    def __init__(self):
        """
        Initialize PlayerClass object.
        """
        
        self.name = ""       
        self.desc = ""
        self.attacks = 0
        self.attkSkill = 0
        self.maxDamage = 0
        self.minDamage = 0
        self.weaponText = {}
        self.powerDesc = ""
        self.maxhp = 0
        self.stealth = 0
        self.critical = 0
        
        


def loadClasses():
    """
    Loads players classes from database 
    and returns a dicts of class objects.
    """
    
    from logger.gamelogger import logger
	
    try:
        conn = sqlite3.connect(os.path.join("data", "ArenaMUD2.db"))
        cursor = conn.cursor()
        cursor.execute("""SELECT name,
                                 attacks,
                                 attackskill,
                                 maxdamage,
                                 mindamage,
                                 powerdesc,
                                 maxhp,
                                 stealth,
                                 weapontextyouhit,
                                 weapontextyoumiss,
                                 weapontextvictimhit,
                                 weapontextvictimmiss,
                                 weapontextroomhit,
                                 weapontextroommiss,
                                 critical,
                                 classdesc FROM classes;""")
        results = cursor.fetchall()

    except:
        logger.log.critical( "Database errors using: ArenaMUD2.db" )


    classes = {}
    x = 1
    #logger.log.debug("Loading classes.")
    for row in results:

        classes[x]                           = PlayerClass()
        classes[x].name                      = str(row[0])
        classes[x].attacks                   = row[1]
        classes[x].attkSkill                 = row[2]
        classes[x].maxDamage                 = row[3]
        classes[x].minDamage                 = row[4]
        classes[x].powerDesc                 = str(row[5])
        classes[x].maxhp                     = row[6]
        classes[x].stealth                   = row[7]
        classes[x].weaponText[YOUHIT]        = str(row[8])
        classes[x].weaponText[YOUMISS]       = str(row[9])
        classes[x].weaponText[VICTIMHIT]     = str(row[10])
        classes[x].weaponText[VICTIMMISS]    = str(row[11])
        classes[x].weaponText[ROOMHIT]       = str(row[12])
        classes[x].weaponText[ROOMMISS]      = str(row[13])
        classes[x].critical                  = row[14]
        classes[x].desc                      = str(row[15])
        x += 1

    #logger.log.debug("{0} classes loaded.".format(len(classes)))
    return classes    
    
Classes = loadClasses()
