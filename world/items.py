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

import character.functions

class Item:
    """
    Item class
    """

    def __init__(self):
        """
        Initialize item object
        """

        self.id = None
        self.name = ""
        # Action is usually a spell
        self.action = None
        self.useText = None
        self.actionText = None
        self.desc = ""

    def __repr__(self):
        """
        String representation.
        """
        return self.name


    def displayDescription(self, player):
        """
        Displays a discription.
        """

        character.functions.sendToPlayer( player, self.desc )


def loadItems():
    """
    Load items from the database.
    """

    from logger.gamelogger import logger    
    try:
        conn = sqlite3.connect(os.path.join("data", "ArenaMUD2.db"))
        cursor = conn.cursor()
        cursor.execute("""SELECT id,
                                 name,
                                 itemaction,
                                 usetext,
                                 actiontext,
                                 description FROM items;""")    
        results = cursor.fetchall()

    except:
        logger.log.critical( "Database errors using: ArenaMUD2.db" )


    items = {}
    logger.log.debug("Loading items.")
    for row in results:
        itemid = row[0]

        items[itemid]                           = Item()
        items[itemid].id                        = itemid
        items[itemid].name                      = str(row[1])
        items[itemid].action                    = row[2]
        items[itemid].useText                   = str(row[3])
        items[itemid].actionText                = str(row[4])
        items[itemid].desc                      = str(row[5])

    logger.log.debug("{0} items loaded.".format(len(items)))
    return items