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
from utils.defines import DIRECTDAMAGE, DIRECTHEAL
from utils.defines import DURATIONDAMAGE, DURATIONHEAL
from utils.defines import AREADAMAGE, AREADURATIONDAMAGE
from utils.defines import AREAHEAL, AREADURATIONHEAL
from utils.defines import DISPELL, AREADISSPELL

# Room spell types
from utils.defines import ROOMSPELL

# Spell text effects
from utils.defines import YOU, ROOM, VICTIM, DURATIONEFFECT
# Spell effects stats
from utils.defines import HP, MAXHP
from utils.defines import BLIND, HELD, STEALTH, VISION
from utils.defines import ATTACKS, ATTKSKILL, CRITICAL
from utils.defines import BONUSDAMAGE, DAMAGEABSORB
from utils.defines import MAXDAMAGE, MINDAMAGE, RESTING
from utils.defines import DEATHS, KILLS, STUN, SNEAKING

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
CASTABLE = [ DIRECTDAMAGE, DIRECTHEAL, DURATIONDAMAGE, DURATIONHEAL, AREADAMAGE, AREAHEAL, AREADURATIONDAMAGE, AREADURATIONHEAL, DISPELL, AREADISSPELL ]
DAMAGESPELLS = [ DIRECTDAMAGE, DURATIONDAMAGE, AREADAMAGE, AREADURATIONDAMAGE, DISPELL, AREADISSPELL ]
BREAKSCOMBAT = [ STUN ]
AREASPELLS = [ AREADAMAGE, AREAHEAL, AREADURATIONDAMAGE, AREADURATIONHEAL, AREADISSPELL ]


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
 
    def __repr__(self):
        """
        Name representation.
        """
        return self.getAttr(SPELLNAME)
    
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
                if len(value) > 1:
                    dmg = utils.gameutils.getRandomValue(int(value[0]), int(value[1]))
                else:
                    dmg = int(value[0])
                    
                if "{0}" in self.getAttr(TEXTEFFECTS)[DURATIONEFFECT]:
                    valuetext = abs(int(dmg))
                    ptext = self.getAttr(TEXTEFFECTS)[DURATIONEFFECT].format(valuetext)
                else:
                    ptext = self.getAttr(TEXTEFFECTS)[DURATIONEFFECT]
            
                character.communicate.sendToPlayer(victim, "{0}{1}".format(LBLUE, ptext))
                newvalue = victim.getAttr(stat) + dmg
                victim.setAttr(stat, newvalue)
                if victim.getAttr(HP) < 1:
                    if caster:
                        combat.functions.applyKillStats(victim, killer=caster)
                    else:
                        combat.function.applyKillStats(victim)
                    
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

        else:
            victim.spells[self.getAttr(SPELLID)] = self
            for stat, value in self.getAttr(SPELLEFFECTS).items():
                if len(value) > 1:
                    dmg = utils.gameutils.getRandomValue(int(value[0]), int(value[1]))
                else:
                    dmg = value[0]
                    
                if stat in victim.stats.keys():
                    self.breaksCombat(stat)
                    victim.stats[stat] += int(dmg)
                else:
                    from logger.gamelogger import logger
                    logger.log.error("Spell stat does not exist in player: {0}".format(stat))
                    
        self.displaySpellText(None)
        
        
    def applyAreaDurationEffects(self):
        """
        Apply area duration spell effects.
        """
        
        caster = self.getAttr(CASTER)
        
        for _victim in world.maps.World.mapGrid[caster.room].playersInRoom().values():
            if _victim is caster and self.getAttr(STYPE) in DAMAGESPELLS:
                continue
            if self.getAttr(SPELLID) in _victim.spells.keys():
                _victim.spells[self.getAttr(SPELLID)] = deepcopy(self)
                _victim.spells[self.getAttr(SPELLID)].setAttr(SPELLVICTIM, _victim)
                _victim.spells[self.getAttr(SPELLID)].setAttr(CASTER, caster)

            else:
                _victim.spells[self.getAttr(SPELLID)] = deepcopy(self)
                _victim.spells[self.getAttr(SPELLID)].setAttr(SPELLVICTIM, _victim)
                _victim.spells[self.getAttr(SPELLID)].setAttr(CASTER, caster)
                for stat, value in self.getAttr(SPELLEFFECTS).items():              
                    if len(value) > 1:
                        dmg = utils.gameutils.getRandomValue(int(value[0]), int(value[1]))
                    else:
                        dmg = value[0]
                    
                        if stat in _victim.stats.keys():
                            self.breaksCombat(stat)
                            _victim.stats[stat] += int(dmg)
                        else:
                            from logger.gamelogger import logger
                            logger.log.error("Spell stat does not exist in player: {0}".format(stat))
                    
        self.displayAreaSpellText(None)
        
        
        
    def applyAreaMagic(self):
        """
        Apply magic effects to player.
        """    
        
        dmg = None
        caster = self.getAttr(CASTER)
        
        combat.functions.endCombat(caster)    
        if self.getAttr(DURATION) is 0:
            for stat, value in self.getAttr(SPELLEFFECTS).items():
                if len(value) > 1:
                    dmg = utils.gameutils.getRandomValue(int(value[0]), int(value[1]))
                else:
                    dmg = value[0]
                    
                if stat in DirectEffects:      
                    value = int(dmg)
                    for _victim in world.maps.World.mapGrid[caster.room].playersInRoom().values():
                        if _victim is caster and self.getAttr(STYPE) in DAMAGESPELLS:
                            continue
                        self.setAttr(SPELLVICTIM, _victim)      
                        statvalue = _victim.getAttr(stat) + value
                        _victim.setAttr(stat, statvalue)
                    
                    self.displayAreaSpellText(value)
                    for _victim in world.maps.World.mapGrid[caster.room].playersInRoom().values():
                        if _victim.getAttr(HP) < 1:
                            if caster:
                                combat.functions.applyKillStats(_victim, killer=caster)
                            else:
                                combat.function.applyKillStats(_victim)
                                
                            combat.functions.playerKilled(_victim)                 
                            _victim.statLine()
                    
                elif stat is DISSPELL:
                    # Call DISSPELL
                    pass
                
        else:
            self.applyAreaDurationEffects()
            
            
                    
    def applyMagic(self):
        """
        Apply magic effects to player.
        """    
        
        dmg = None
        victim = self.getAttr(SPELLVICTIM)
        caster = self.getAttr(CASTER)
        
        combat.functions.endCombat(caster)    
        if self.getAttr(DURATION) is 0:
            for stat, value in self.getAttr(SPELLEFFECTS).items():
                if len(value) > 1:
                    dmg = utils.gameutils.getRandomValue(int(value[0]), int(value[1]))
                else:
                    dmg = value[0]
                if stat in DirectEffects:      
                    value = int(dmg)
                    statvalue = victim.getAttr(stat) + value
                    victim.setAttr(stat, statvalue)
                    self.displaySpellText(value)
                    if victim.getAttr(HP) < 1:
                        if caster:
                            combat.functions.applyKillStats(victim, killer=caster)
                        else:
                            combat.function.applyKillStats(victim)
                        
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
        
        player.setAttr(SNEAKING, False)
        self.setAttr(CASTER, player)
        
        if player.spellsCasted.has_key(self.getAttr(MNEMONIC)):
            character.communicate.sendToPlayer(player, "You haven't recovered from your last attempt of {0}.".format(self.getAttr(SPELLNAME)))
            return
         
        if len(cmd) is 2:
            if self.getAttr(STYPE) in AREASPELLS:
                character.communicate.sendToPlayer( player, "You cannot target an area spell.")
                return
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
                
                self.applyMagic()
                              
        else:         
            if self.getAttr(STYPE) in AREASPELLS:
                self.applyAreaMagic()
                
            else:    
                self.setAttr(SPELLVICTIM, player)
                if self.getAttr(STYPE) in DAMAGESPELLS:
                    character.communicate.sendToPlayer(player, "Are you a masochist?")   
                    return
                else:
                    self.applyMagic()
        
        # seed is an specific castings id. see utils.gameutils.resetCooldown() for further info.     
        seed = random.randint(0, 10000)
        self.getAttr(CASTER).spellsCasted[self.getAttr(MNEMONIC)] = seed
        reactor.callLater(self.getAttr(COOLDOWN), utils.gameutils.resetCooldown, player, self.getAttr(MNEMONIC), seed)
        
        
        
    def displayAreaSpellText(self, value):
        """
        Display area spell text.
        """
        
        caster = self.getAttr(CASTER)
        
        if value:
            if value < 1:
                COLOR = RED
            else:
                COLOR = LBLUE 
                
            value = abs(value)
            ptext = self.getAttr(TEXTEFFECTS)[YOU].format(value)
            rtext = self.getAttr(TEXTEFFECTS)[ROOM].format(caster.name, value)
            
        else:
            COLOR = LBLUE
            ptext = self.getAttr(TEXTEFFECTS)[YOU]
            rtext = self.getAttr(TEXTEFFECTS)[ROOM].format(caster.name)            
        
        character.communicate.sendToPlayer(caster, "{0}{1}".format(COLOR, ptext))
        character.communicate.sendToRoomNotPlayer(caster, "{0}{1}".format(COLOR, rtext))
            
            
            
    def displaySpellText(self, value):
        """
        Tell the room about casting the spell.
        """
        
        victim = self.getAttr(SPELLVICTIM)
        caster = self.getAttr(CASTER)
        
        if value:
            if value < 1:
                COLOR = RED
            else:
                COLOR = LBLUE
                
            value = abs(value)
            ptext = self.getAttr(TEXTEFFECTS)[YOU].format(victim.name, value)
            vtext = self.getAttr(TEXTEFFECTS)[VICTIM].format(caster.name, value)
            rtext = self.getAttr(TEXTEFFECTS)[ROOM].format(caster.name, victim.name, value)  
            
        else:
            COLOR = LBLUE
            ptext = self.getAttr(TEXTEFFECTS)[YOU].format(victim.name)
            vtext = self.getAttr(TEXTEFFECTS)[VICTIM].format(caster.name)
            rtext = self.getAttr(TEXTEFFECTS)[ROOM].format(caster.name, victim.name)        
        
        
        if victim is not caster:
            character.communicate.sendToPlayer(caster, "{0}{1}".format(COLOR, ptext))
            character.communicate.sendToPlayer(victim, "{0}{1}".format(COLOR, vtext))
            character.communicate.sendToRoomNotPlayerOrVictim(caster, victim, "{0}{1}".format(COLOR, rtext))
        else:
            character.communicate.sendToPlayer(caster, "{0}{1}".format(LBLUE, ptext))
            character.communicate.sendToRoomNotPlayer(caster, "{0}{1}".format(COLOR, rtext))
        
        
        
    def breaksCombat(self, stat):
        """
        Checks to see if spell breaks combat.
        """

        if stat in BREAKSCOMBAT:
            combat.functions.endCombat(self.getAttr(SPELLVICTIM))
            
            

            
            
        
def loadPlayerSpells():
    """
    Loads players classes from database 
    and returns a dicts of class objects.
    """
    
    from logger.gamelogger import logger
    
	
    try:
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
                                 durationeffect,
                                 effects FROM playerspells;""")
        
        results = cursor.fetchall()

    except sqlite3.Error, e:
        logger.log.critical("Error using loadPlayerSpells(): {0}".format(e.args[0]))


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
        
        spells[mnemonic].attrib[TEXTEFFECTS][YOU]            = str(row[10])
        spells[mnemonic].attrib[TEXTEFFECTS][VICTIM]         = str(row[11])
        spells[mnemonic].attrib[TEXTEFFECTS][ROOM]           = str(row[12])
        spells[mnemonic].attrib[TEXTEFFECTS][DURATIONEFFECT] = str(row[13])

        stattext                                    = str(row[14])
        
        for each in stattext.split("|"):
            stat, value = each.split(":")
            value = value.split("!")
            spells[mnemonic].attrib[SPELLEFFECTS][int(stat)] = value
        
        
    return spells

