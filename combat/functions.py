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

import random

from world.maps import World
from character.players import AllPlayers
from character.communicate import sendToPlayer, sendToRoomNotPlayerOrVictim
from character.communicate import  sendToRoomNotPlayer, tellWorld
from character.functions import spawnPlayer
from utils.defines import YOUHIT, YOUMISS, VICTIMHIT, VICTIMMISS
from utils.defines import ROOMHIT, ROOMMISS, PLAYING, BROWN, WHITE, RED



def doCombatRound(combatqueue):
    """
    Calls doAttack for each player
    in the combat queue.
    """
    
    for attacker in combatqueue.getCombatQueue():
        if attacker not in AllPlayers.keys():
            combatqueue.removeAttack(attacker)
        else:
            player = AllPlayers[attacker]
            if not player.attacking:
                continue
            if player.attacking.name not in AllPlayers.keys():
                endCombat(player)
            else:
                victim = player.attacking
                if player.room == victim.room:
                    doAttack(player, victim)
                else:
                    endCombat(player)
                
                
                
def doAttack(player, victim):
    """
    Executes a players regular attack.
    """
    
    victim.resting = False
    for attk in range(0, player.attacks):
        attackroll = random.randint(1, 100)
        if player.attkSkill >= attackroll:
            dmg = random.randint(player.minDamage, player.maxDamage)
            crit = criticalRoll(player, dmg)
            if crit:
                dmg = crit
                crit = True              
            displayDamage(player, victim, dmg, crit)
            victim.hp = victim.hp - dmg
            if victim.hp < 1:
                clearAttacksPlayerDead(victim)
                playerKilled(victim)
                return
                
            
        else:
            displayDamage(player, victim, None, False)
            

    

def criticalRoll(player, damage):
    """
    Rolls critical chance and returns
    new damage value based on crit.
    """
    critroll = random.randint(1, 100)
    if (100 - player.critical) < critroll:
        return (damage * 2)
    return False




def displayDamage(player, victim, dmg, crit):
    """
    Displays damage or misses to the room.
    """
    def updateForCritical(line):
        """
        Adds critical message to text.
        """
        newtext = ""
        splittext = line.split()
        for x in range(len(splittext)):
            if x == 1:
                newtext += "critically {0} ".format(splittext[x])
            else: 
                newtext += "{0} ".format(splittext[x])
                
        return newtext
        
    if dmg:
        ptext = RED + player.weaponText[YOUHIT].format(victim.name, str(dmg)) 
        vtext = RED + player.weaponText[VICTIMHIT].format(player.name, str(dmg))
        rtext = RED + player.weaponText[ROOMHIT].format(player.name, victim.name, str(dmg))
        if crit:
            ptext = updateForCritical(ptext)
            vtext = updateForCritical(vtext)
            rtext = updateForCritical(rtext)
    else:
        ptext = WHITE + player.weaponText[YOUMISS].format(victim.name)
        vtext = WHITE + player.weaponText[VICTIMMISS].format(player.name)
        rtext = WHITE + player.weaponText[ROOMMISS].format(player.name, victim.name)

    sendToPlayer( player, ptext )
    sendToPlayer( victim, vtext )
    sendToRoomNotPlayerOrVictim( player, victim, rtext )




def endCombat(player):
    """
    Ends combat for user.
    """
    if player.status == PLAYING:
        if player.attacking:
            sendToPlayer( player, "{0}*Combat Off*".format(BROWN) )
        player.factory.combatQueue.removeAttack(player.name)
        player.attacking = None
    else:
        player.factory.combatQueue.removeAttack(player.name)
        player.attacking = None
   
        
        
    
def attack(player, vicName):
    """
    Check to see if the victim is in the room. If
    he is, engage combat.
    """
    curRoom = World.mapGrid[player.room]
    victims = curRoom.findPlayerInRoom(player, vicName)

    if not victims:
        sendToPlayer( player, "You do not see {0} here.".format(vicName) )
    elif len(victims) > 1:
        sendToPlayer( player, "Who do you want to attack?" )
        for name in victims:
            sendToPlayer( player, " - {0}".format(name) )
    else:
        if victims[0].name == player.name:
            sendToPlayer( player, "Why would you want to attack yourself?" )
        else:
            player.attacking = victims[0]
            player.resting = False
            player.attacking.resting = False
            sendToPlayer( player, "{0}*Combat Engaged*".format(BROWN) )
            sendToPlayer( player.attacking, "{0}{1} moves to attack you!".format(BROWN, player.name) )
            sendToRoomNotPlayerOrVictim( player, player.attacking, "{0}{1} moves to attack {0}!".format(BROWN, player.name, player.attacking) )
            player.factory.combatQueue.addAttack(player.name)
        
    

def playerKilled(player):
    """
    Kill the player
    """
    
    sendToRoomNotPlayer( player, "{0} drops to the ground.".format(player.name) )
    del World.mapGrid[player.room].players[player.name]
    tellWorld( player, "You have died.", "{0} was killed.".format(player.name) )
    endCombat( player )
    spawnPlayer( player )
    
    
    
def clearAttacksPlayerDead(victim):
    """
    Remove all attacks against dead
    player.
    """
    
    for player in AllPlayers.values():
        if player.attacking == victim:
            endCombat( player )