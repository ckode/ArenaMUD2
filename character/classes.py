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
from utils.defines import ROOMHIT, ROOMMISS, BS_HIT_YOU, BS_HIT_VICTIM
from utils.defines import BS_HIT_ROOM



class PlayerClass:
    """
    ArenaMUD Player Classes
    """
    
    def __init__(self):
        """
        Initialize PlayerClass object.
        """
        
        self.classid = 0
        self.name = ""       
        self.desc = ""
        self.attacks = 0
        self.attkSkill = 0
        self.maxDamage = 0
        self.minDamage = 0
        self.weaponText = {}
        self.maxhp = 0
        self.stealth = 0
        self.critical = 0
        self.dodge = 0
        
        


def loadClasses():
    """
    Loads players classes from database 
    and returns a dicts of class objects.
    """
    
    from logger.gamelogger import logger
	
    try:
        conn = sqlite3.connect(os.path.join("data", "ArenaMUD2.db"))
        cursor = conn.cursor()
        cursor.execute("""SELECT id,
                                 name,
                                 attacks,
                                 attackskill,
                                 maxdamage,
                                 mindamage,
                                 maxhp,
                                 stealth,
                                 weapontextyouhit,
                                 weapontextyoumiss,
                                 weapontextvictimhit,
                                 weapontextvictimmiss,
                                 weapontextroomhit,
                                 weapontextroommiss,
                                 bs_hit_you,
                                 bs_hit_victim,
                                 bs_hit_room,                                 
                                 critical,
                                 dodge,
                                 backstabmultiplier,
                                 classdesc FROM classes;""")
        
        results = cursor.fetchall()

    except:
        logger.log.critical( "Database errors using: ArenaMUD2.db" )


    classes = {}

    #logger.log.debug("Loading classes.")
    for row in results:
        cid                                    = row[0]
    
        classes[cid]                           = PlayerClass()
        classes[cid].classid                   = cid
        classes[cid].name                      = str(row[1])
        classes[cid].attacks                   = row[2]
        classes[cid].attkSkill                 = row[3]
        classes[cid].maxDamage                 = row[4]
        classes[cid].minDamage                 = row[5]
        classes[cid].maxhp                     = row[6]
        classes[cid].stealth                   = row[7]
        classes[cid].weaponText[YOUHIT]        = str(row[8])
        classes[cid].weaponText[YOUMISS]       = str(row[9])
        classes[cid].weaponText[VICTIMHIT]     = str(row[10])
        classes[cid].weaponText[VICTIMMISS]    = str(row[11])
        classes[cid].weaponText[ROOMHIT]       = str(row[12])
        classes[cid].weaponText[ROOMMISS]      = str(row[13])
        classes[cid].weaponText[BS_HIT_YOU]    = str(row[14])
        classes[cid].weaponText[BS_HIT_VICTIM] = str(row[15])
        classes[cid].weaponText[BS_HIT_ROOM]   = str(row[16])
        classes[cid].critical                  = row[17]
        classes[cid].dodge                     = row[18]
        classes[cid].bsmultiplier              = row[19]
        classes[cid].desc                      = str(row[20])
        

    #logger.log.debug("{0} classes loaded.".format(len(classes)))
    return classes    
    
Classes = loadClasses()
