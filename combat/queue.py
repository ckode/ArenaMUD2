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





class CombatQueue():
    """
    Combat Queue
    """
    def __init__(self):
        """
        Initialize CombatQueue object.
        """
        self.QueueIndex = {}
        self.combatQueue = []


    def addAttack(self, playerid):
        """
        Adds a new attack to the combat queue
        """

        self.RemoveAttack(playerid)
        # add new attack and update index.
        self.combatQueue.append(playerid)
        self.UpdateIndex()


    def removeAttack(self, playerid):
        """
        Remove an attack from the combat queue.
        """
        if playerid in self.QueueIndex.keys():
            del self.combatQueue[self.QueueIndex[playerid]]
            self.UpdateIndex()


    def updateIndex(self):
        """
        Rebuild combat queue index.
        """

        self.QueueIndex.clear()
        x = 0
        for playerid in self.combatQueue:
            self.QueueIndex[playerid] = x
            x += 1


    def getCombatQueue(self):
        """
        Returns the combat queue
        """
        return self.combatQueue[:]

    
    def clearCombatQueue(self):
        """
        Removes all combat from the
        combat queue.
        """
        self.QueueIndex.clear()
        del self.combatQueue[:]