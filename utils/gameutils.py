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

from character.players import AllPlayers
import world.maps

from utils.defines import PLAYING
from utils.defines import CYAN, YELLOW, LRED, BLUE, LGREEN, BLUE, WHITE
from utils.defines import HP, MAXHP, POWER, MAXPOWER, RESTING

import character.communicate

def restHealing():
    """
    If player resting, rest heal him.
    """
    
    healRate = 15
    for player in AllPlayers.values():
        # If player isn't playing.  No need to heal
        if player.status is not PLAYING:
            continue
        if player.stats[RESTING]:
            healPlayer(player, HP, healRate)       
            player.statLine()
            
            
            
def naturalHealing():
    """
    Natural healing loop.
    """
    
    healRate = 5
    for player in AllPlayers.values():
        # If player isn't playing.  No need to heal
        if player.status is not PLAYING:
            continue        
        
        healPlayer(player, HP, healRate)     
        player.statLine()
        
        
        
def healPlayer(player, STAT, value):
    """
    Add value to players STAT unless
    above max STAT.  (HP, and POWER)
    """
    
    STAT = int(STAT)
    if STAT is HP:
        maxvalue = player.stats[MAXHP]
    else:
        return
    
    if value > 0:
        if (player.stats[STAT] + value) > maxvalue:
            player.stats[STAT] = maxvalue
        else:
            player.stats[STAT] += value    
    else:
        player.stats[STAT] += value

    

def doRoomSpells():
    """
    Execute rooms spells
    """
    from world.maps import World
    
    for rid in World.roomsList:
        room = World.mapGrid[rid]
        if room.spell:
            if room.spell.preText:
                character.communicate.sendToRoom(room.id, room.spell.preText)
            for player in room.players.values():
                room.spell.applyMagic(player, None)


def doDurationEffectSpells():
    """
    Apply duration effects of spells.
    """
    for player in AllPlayers.values():
        # If player isn't playing.  No need to heal
        if player.status is not PLAYING:
            continue  
        for spell in player.spells.values():
            spell.durationEffect()
            
            
    
def purgatoryHelpMsg(player):
    character.communicate.sendToPlayer(player, "{0}Command had no effect. Type '{1}spawn{0}' to spawn or type '{1}help{0}' for help.".format(CYAN, YELLOW))
    
    
def getHealthColor(player):
    """
    Returns the health color based on
    how players heal precentage is.
    """
    
    if player.stats[HP] < ((float(player.stats[MAXHP]) / 100) * 25):
        hpcolor = LRED
    elif player.stats[HP] < ((float(player.stats[MAXHP]) / 100) * 50):
        hpcolor = YELLOW
    elif player.stats[HP] < ((float(player.stats[MAXHP]) / 100) * 75):
        hpcolor = LGREEN
    elif player.stats[HP] < ((float(player.stats[MAXHP]) / 100) * 85):
        hpcolor = WHITE
    elif player.stats[HP] < ((float(player.stats[MAXHP]) / 100) * 95):
        hpcolor = WHITE
    else:
        hpcolor = WHITE
            
    # If player.hp is higher than maxhp, make it blue (only a buff can do this)
    if player.stats[HP] > player.stats[MAXHP]:
        hpcolor = BLUE    
        
    return hpcolor



def resetCooldown(player, spellid, seed):
    """
    Reset cooldown for a spell that has been casted.
    """
    
    if player:
        if player.spellsCasted.has_key(spellid):
            # seed is to ensure cooldown is removing for the correct casting as
            # the caster could have died and recasted the spell
            if player.spellsCasted[spellid] is seed:
                del player.spellsCasted[spellid]
                
                
                
def getRandomValue(value1, value2):
    """
    Get random value between two numbers.
    This is required because it could be 
    negative numbers.
    """
    
    value1 = int(value1)
    value2 = int(value2)
    if value1 > value2:
        return random.randint(value2, value1)
    else:
        return random.randint(value1, value2)