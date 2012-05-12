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
import random

from twisted.internet import reactor

import character.communicate
import utils.gameutils
import combat.functions
import logger.gamelogger
import world.maps
from copy import deepcopy

# Spell types
from utils.defines import DURATIONDAMAGE, ROOMSPELL, HEAL, DURATIONHEAL
from utils.defines import BUFF, DEBUFF, DIRECTDAMAGE, DISSPELL
from utils.defines import AREADAMGE, AREADURATION

# Spell text effects
from utils.defines import YOU, ROOM, VICTIM
# Spell effects stats
from utils.defines import HP, MAXHP
from utils.defines import BLIND, HELD, STEALTH, VISION
from utils.defines import ATTACKS, ATTKSKILL, CRITICAL
from utils.defines import BONUSDAMAGE, DAMAGEABSORB
from utils.defines import MAXDAMAGE, MINDAMAGE, RESTING
from utils.defines import DEATHS, KILLS, STUN

# Define magic stats
from utils.defines import SPELLID, STYPE, SCLASS, SPELLNAME
from utils.defines import TARGET, GESTURE, S_END_TEXT, TEXTEFFECTS
from utils.defines import DURATIONEFFECT, CASTER, SPELLVICTIM, COOLDOWN
from utils.defines import DURATION, MNEMONIC, SPELLEFFECTS

# Colors
from utils.defines import BLUE, RED, LBLUE


# Stats that can be changed and not undone with spell completes (heal, damage)
DirectEffects = [HP]
ROOMSPELLS = [ ROOMSPELL ]
CASTABLE = [ BUFF, DEBUFF, DIRECTDAMAGE, HEAL, DISSPELL, DURATIONDAMAGE, DURATIONHEAL ]
DAMAGESPELLS = [ DEBUFF, DIRECTDAMAGE, DISSPELL, DURATIONDAMAGE ]
BREAKSCOMBAT = [ STUN ]
AREASPELL = [ AREADAMGE, AREADURATION ]


class PlayerSpells:
    """
    The PlayerSpells class.  
    """
    
    def __init__(self):
        
        self.attrib = { SPELLID: None,
                        STYPE: None,
                        SCLASS: None,
                        SPELLNAME: "",
                        TARGET: None,
                        GESTURE: "",
                        S_END_TEXT: "",
                        TEXTEFFECTS: {},
                        DURATIONEFFECT: "",
                        CASTER: None,
                        SPELLVICTIM: None,
                        COOLDOWN: 0,
                        DURATION: 0,
                        MNEMONIC: "",
                        SPELLEFFECTS: {}
                      } 
 
    
    def getAttr(self, attribute):
        """
        Returns the specified spell attribute.
        """

        if self.attrib.has_key(attribute):
            return self.attrib[attribute]
        else:
            logger.gamelogger.logger.error("Error getting attribute: Invalid spell attribute: {0}".format(attribute))
            return None
        
        
    def setAttr(self, attribute, value):
        """
        Returns the specified spell attribute.
        """

        if self.attrib.has_key(attribute):
            self.attrib[attribute] = value
        else:
            logger.gamelogger.logger.error("Error setting attribute: Invalid spell attribute: {0}".format(attribute))

        
        
    def durationEffect(self):
        """
        Execute the spell's effects.
        """
                
        caster = self.getAttr(CASTER)
        victim = self.getAttr(SPELLVICTIM)
        
        self.setAttr(DURATION, self.getAttr(DURATION) - 1)
        if self.getAttr(DURATION) < 0:
            self.removeDurationEffects()
            return
                
        for stat, value in self.getAttr(SPELLEFFECTS).items():
            if stat in DirectEffects:
                valuetext = abs(value)
                ptext = self.getAttr(TEXTEFFECTS)[YOU].format(valuetext)
                if value < 1:
                    COLOR = RED
                else:
                    COLOR = BLUE                
                character.communicate.sendToPlayer(victim, "{0}{1}".format(COLOR, ptext))
                victim.stats[stat] += value
                if victim.stats[HP] < 1:
                    if caster:
                        caster.stats[KILLS] += 1
                    victim.stats[DEATHS] += 1
                    combat.functions.playerKilled(victim)
                
                

                
        
     
    def removeDurationEffects(self):
        """
        Remove duration spell effects.
        """

        victim = self.getAttr(SPELLVICTIM)
        character.communicate.sendToPlayer(victim, "{0}{1}".format(BLUE, self.getAttr(S_END_TEXT)))
        for stat, value in self.getAttr(SPELLEFFECTS).items():
            if stat in victim.stats.keys():
                victim.stats[stat] -= int(value[0])
            else:
                from logger.gamelogger import logger
                logger.log.error("Spell stat does not exist in player: {0}".format(stat))
         
        del victim.spells[self.getAttr(SPELLID)]      
        


    def applyDurationEffects(self):
        """
        Apply duration spell effects.
        """
        
        victim = self.getAttr(SPELLVICTIM)
        
        if self.getAttr(SPELLID) in victim.spells.keys():
            victim.spells[self.getAttr(SPELLID)] = self
            return
        else:
            victim.spells[self.getAttr(SPELLID)] = self
            for stat, value in self.getAttr(SPELLEFFECTS).items():
                if stat in victim.stats.keys():
                    self.breaksCombat(stat)
                    victim.stats[stat] += int(value[0])
                else:
                    from logger.gamelogger import logger
                    logger.log.error("Spell stat does not exist in player: {0}".format(stat))
         
        
        
                    
                    
    def applyMagic(self):
        """
        Apply magic effects to player.
        """
        
        def getRandomValue(value1, value2):
            """
            Get random value between two numbers.
            This is required because it could be 
            negative numbers.
            """
            
            if value1 > value2:
                return random.randint(value2, value1)
            else:
                return random.randint(value1, value2)
        
        victim = self.getAttr(SPELLVICTIM)
        caster = self.getAttr(CASTER)
        
        combat.functions.endCombat(caster)    
        if self.getAttr(DURATION) is 0:
            for stat, value in self.getAttr[SPELLEFFECTS].items():
                values = value.split("!")
                
                if len(values) > 1:
                    dmg = getRandomValue(int(values[0]), int(values[1]))
                else:
                    dmg = value
                if stat in DirectEffects:      
                    value = abs(dmg)
                    ptext = self.getAttr[SPELLEFFECTS][YOU].format(value)
                    if dmg < 1:
                        COLOR = RED
                    else:
                        COLOR = BLUE
                    character.communicate.sendToPlayer( victim, "{0}{1}".format(COLOR, ptext) )
                    utils.gameutils.healPlayer(victim, stat, dmg)
                    if victim.stats[HP] < 1:
                        if caster:
                            caster.stats[KILLS] += 1
                        victim.stats[DEATHS] += 1
                        combat.functions.playerKilled(victim)                 
                    victim.statLine()
                elif stat is DISSPELL:
                    # Call DISSPELL
                    pass
                
        else:
            self.applyDurationEffects()
        
        
                    

    def castSpell(self, player, cmd):
        """
        Try to cast the spell.
        """
        
        if player.spellsCasted.has_key(self.getAttr(MNEMONIC)):
            character.communicate.sendToPlayer(player, "You haven't recovered from your last attempt of {0}.".format(self.getAttr(SPELLNAME)))
            return
        
        if len(cmd) is 2:
            vicName = cmd[1]
            victims = world.maps.World.mapGrid[player.room].findPlayerInRoom(player, vicName)
            if not victims:
                character.communicate.sendToPlayer( player, "You do not see {0} here.".format(vicName) )
                return
            elif len(victims) > 1:
                character.communicate.sendToPlayer(player, "Who do you want to cast on?")
                for name in victims:
                    character.communicate.sendToPlayer(player, " - {0}".format(name))           
                return
            
            else:
                self.setAttr(CASTER, player) 
                self.setAttr(SPELLVICTIM, victims[0])
                
                if self.getAttr(STYPE) in DAMAGESPELLS and player is victims[0]:
                    character.communicate.sendToPlayer(player, "Are you a masochist?")
                    return    
                
                self.displaySpellText()
                self.applyMagic()
                              
        else:
            self.setAttr(CASTER, player) 
            if self.getAttr(STYPE) in AREASPELL:
                self.applyToRoom()
                return
                
            self.setAttr(SPELLVICTIM, player)
            if self.getAttr(STYPE) in DAMAGESPELLS:
                character.communicate.sendToPlayer(player, "Are you a masochist?")
                return   
            
            self.displaySpellText()
            self.applyMagic()
        
        # seed is an specific castings id. see utils.gameutils.resetCooldown() for further info.     
        seed = random.randint(0, 10000)
        self.getAttr(CASTER).spellsCasted[self.getAttr(MNEMONIC)] = seed
        reactor.callLater(self.getAttr(COOLDOWN), utils.gameutils.resetCooldown, player, self.getAttr(MNEMONIC), seed)
        
        
    def displayAreaSpellText(self):
        """
        Display area spell text.
        """
        
        if "{0}" in self.getAttr*TEXTEFFECTS[YOU]:
            pass
            
    def displaySpellText(self):
        """
        Tell the room about casting the spell.
        """
        
        victim = self.getAttr(SPELLVICTIM)
        caster = self.getAttr(CASTER)
        ptext = self.getAttr(TEXTEFFECTS)[YOU].format(victim.name)
        vtext = self.getAttr(TEXTEFFECTS)[VICTIM].format(caster.name)
        
        # If casting on self, don't name himself twice (text most fit this)
        if "{1}" in self.getAttr(TEXTEFFECTS)[ROOM]:
            rtext = self.getAttr(TEXTEFFECTS)[ROOM].format(caster.name, victim.name)
        else:
            rtext = self.getAttr(TEXTEFFECTS)[ROOM].format(caster.name)
        
        if victim is not caster:
            character.communicate.sendToPlayer(caster, "{0}{1}".format(LBLUE, ptext))
            character.communicate.sendToPlayer(victim, "{0}{1}".format(LBLUE, vtext))
            character.communicate.sendToRoomNotPlayerOrVictim(caster, victim, "{0}{1}".format(LBLUE, rtext))
        else:
            character.communicate.sendToPlayer(caster, "{0}{1}".format(LBLUE, ptext))
            character.communicate.sendToRoomNotPlayer(caster, "{0}{1}".format(LBLUE, rtext))
        
        
        
    def breaksCombat(self, stat):
        """
        Checks to see if spell breaks combat.
        """

        if stat in BREAKSCOMBAT:
            combat.functions.endCombat(self.getAttr(SPELLVICTIM))
            
            
    def applyToRoom(self, adsf):
        """
        Apply spell to everyone in the room.
        """
        
        caster = self.getAttr(CASTER)
        
        for _victim in world.maps.World.mapGrid[caster.room].playerInRoom().values():
            newspell = deepcopy(self)
            newspell.setAttr(CASTER, caster)
            if _victim is not caster:
                newspell.setAttr(SPELLVICTIM, _victim)        
                newspell.applyMagic()
            
            
        
def loadPlayerSpells():
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
                                 mnemonic,
                                 target,
                                 gesture,
                                 posttext,
                                 cooldown,
                                 texteffect1,
                                 texteffect2,
                                 texteffect3,
                                 effects FROM playerspells;""")
        
    results = cursor.fetchall()

    #except:
    #    logger.log.critical( "Database errors using: ArenaMUD2.db" )


    spells = {}
    
    x = 1
    #logger.log.debug("Loading classes.")
    for row in results:
        sid                                      = row[0]
        mnemonic                                  = str(row[5])
        
        spells[mnemonic]                              = PlayerSpells()
        spells[mnemonic].setAttr(SPELLID, sid)
        spells[mnemonic].setAttr(SPELLNAME, str(row[1]))
        spells[mnemonic].setAttr(STYPE, row[2])
        spells[mnemonic].setAttr(SCLASS, row[3])
        spells[mnemonic].setAttr(DURATION, row[4])
        spells[mnemonic].setAttr(MNEMONIC, mnemonic)
        spells[mnemonic].setAttr(TARGET, row[6])
        spells[mnemonic].setAttr(GESTURE, str(row[7]))
        spells[mnemonic].setAttr(S_END_TEXT, str(row[8]))
        spells[mnemonic].setAttr(COOLDOWN, row[9])
        
        spells[mnemonic].attrib[TEXTEFFECTS][YOU]    = str(row[10])
        spells[mnemonic].attrib[TEXTEFFECTS][VICTIM] = str(row[11])
        spells[mnemonic].attrib[TEXTEFFECTS][ROOM]   = str(row[12])

        stattext                                    = str(row[13])
        
        for each in stattext.split("|"):
            stat, value = each.split(":")
            value = value.split("!")
            spells[mnemonic].attrib[SPELLEFFECTS][int(stat)] = value
        
        
    return spells

