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

import character.communicate
import combat.functions
import logger.gamelogger

# Spell types
from utils.defines import DURATIONSPELL, ROOMDURATIONSPELL, ROOMSPELL
from utils.defines import BUFF, DIRECTEFFECT
# Spell text effects
from utils.defines import YOU, ROOM, VICTIM
# Spell effects stats
from utils.defines import HP, MAXHP, POWER, MAXPOWER
from utils.defines import BLIND, HELD, STEALTH, VISION
from utils.defines import ATTACKS, ATTKSKILL, CRITICAL
from utils.defines import BONUSDAMAGE, DAMAGEABSORB
from utils.defines import MAXDAMAGE, MINDAMAGE, RESTING
from utils.defines import DEATHS, KILLS
# Colors
from utils.defines import BLUE, RED


# Stats that can be changed and not undone with spell completes (heal, damage)
DirectEffects = [HP, POWER]
ROOMSPELLS = [ ROOMDURATIONSPELL, ROOMSPELL ]


class Magic:
    """
    The magic class.  
    """
    
    def __init__(self):
        self.sType = None
        self.sClass = None
        self.name = ""
        self.duration = None
        self.memonic = ""
        self.preText = ""
        self.postText = ""
        self.textEffect = {}
        self.stats = {}
        self.caster = None
        self.victim = None
        
        

    def durationEffect(self,):
        """
        Execute the spell's effects.
        """

        global DirectEffects
        
        self.duration -= 1
        if self.duration < 0:
            character.communicate.sendToPlayer( self.victim, "{0}{1}".format(BLUE, self.postText) )
            self.removeDurationEffects()
            return False
                
        for stat, value in self.stats.items():
            if stat in DirectEffects:
                valuetext = str(value).replace("-", "")
                ptext = self.textEffect[YOU].format(valuetext)
                if value < 1:
                    COLOR = RED
                else:
                    COLOR = BLUE                
                character.communicate.sendToPlayer( self.victim, "{0}{1}".format(COLOR, ptext) )
                victim.stats[stat] += value
                if victim.stats[HP] < 1:
                    if self.caster:
                        self.caster.stats[KILLS] += 1
                    self.victim.stats[DEATHS] += 1
                    combat.functions.playerKilled(self.victim)
                elif victim.stats[POWER] < 0:
                    victim.stats[POWER] = 0
                    
        return True

                
        
     
    def removeDurationEffects(self):
        """
        Remove duration spell effects.
        """
        
        for stat, value in self.stats.items():
            if stat not in DirectEffects:
                valuetext = str(value).replace("-", "")
                ptext = self.textEffect[YOU].format(valuetext)
                if value < 1:
                    COLOR = RED
                else:
                    COLOR = BLUE                
                character.communicate.sendToPlayer( self.victim, "{0}{1}".format(COLOR, ptext) )
                if stat in self.victim.stats.keys():
                    self.victim.stats[stat] -= value
                else:
                    from logger.gamelogger import logger
                    logger.log.error( "Spell stat does not exist in player: {0}".format(stat) )
               
                    
                    
                    
    def applyMagic(self, victim, caster):
        """
        Apply magic effects to player.
        """
        
        self.victim = victim
        self.caster = caster
        
        if self.duration is 0:
            for stat, value in self.stats.items():
                if stat in DirectEffects:      
                    valuetext = str(value).replace("-", "")
                    ptext = self.textEffect[YOU].format(valuetext)
                    if value < 1:
                        COLOR = RED
                    else:
                        COLOR = BLUE
                    character.communicate.sendToPlayer( self.victim, "{0}{1}".format(COLOR, ptext) )
                    victim.stats[stat] += value
                    if victim.stats[HP] < 1:
                        if self.caster:
                            self.caster.stats[KILLS] += 1
                        self.victim.stats[DEATHS] += 1
                        combat.functions.playerKilled(self.victim)
                    elif victim.stats[POWER] < 0:
                        victim.stats[POWER] = 0                    
        
        
        
def loadMagic():
    """
    Loads players classes from database 
    and returns a dicts of class objects.
    """
    
    from logger.gamelogger import logger
	
    #try:
    conn = sqlite3.connect(os.path.join("data", "ArenaMUD2.db"))
    cursor = conn.cursor()
    cursor.execute("""SELECT sid,
                                 name,
                                 stype,
                                 sclass,
                                 duration,
                                 memonic,
                                 pretext,
                                 posttext,
                                 texteffect1,
                                 texteffect2,
                                 texteffect3,
                                 stats FROM magic;""")
        
    results = cursor.fetchall()

    #except:
    #    logger.log.critical( "Database errors using: ArenaMUD2.db" )


    spells = {}
    x = 1
    #logger.log.debug("Loading classes.")
    for row in results:
        sid                                   = row[0]
        
        spells[sid]                           = Magic()
        spells[sid].name                      = str(row[1])  
        spells[sid].sType                     = row[2]
        spells[sid].sClass                    = str(row[3])
        spells[sid].duration                  = row[4]
        spells[sid].memonic                   = str(row[5])
        spells[sid].preText                   = str(row[6])
        spells[sid].postText                  = str(row[7])
        spells[sid].textEffect[YOU]           = str(row[8])
        spells[sid].textEffect[VICTIM]        = str(row[9])
        spells[sid].textEffect[ROOM]          = str(row[10])
        stattext                              = str(row[11])
        
        for each in stattext.split("|"):
            stat, value = each.split(":")
            spells[sid].stats[int(stat)] = int(value)
        
        
    return spells