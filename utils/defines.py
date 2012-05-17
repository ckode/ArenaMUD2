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

# Server Version, should be maybe the commit number? something
# besides NoDamnVersion anyhow.
SERVERVERSION      = '0.5.7'

# Directions
NORTH              = 1
NE                 = 2
EAST               = 3
SE                 = 4
SOUTH              = 5
SW                 = 6
WEST               = 7
NW                 = 8
UP                 = 9
DOWN               = 10


OPPOSITEDIRS   =  { NORTH: SOUTH,
                    NE: SW,
                    EAST: WEST,
                    SE: NW,
                    SOUTH: NORTH,
                    SW: NE,
                    WEST: EAST,
                    NW: SE,
                    UP: DOWN,
                    DOWN: UP
                  }

# Direction text matrix
DIRS         = { NORTH: 'north', NE: 'northeast', EAST: 'east', SE: 'southeast', SOUTH: 'south',
                 SW: 'southwest', WEST: 'west', NW: 'northwest', UP: 'up', DOWN: 'down' }

				 
DIRLOOKUP      = { "n":    1,
                   "ne":   2,
                   "e":    3,
                   "se":   4,
                   "s":    5,
                   "sw":   6,
                   "w":    7,
                   "nw":   8,
                   "u":    9,
                   "d":   10
                 }

#  Player status defines
LOGIN = 0
PLAYING = 1 
GETCLASS = 2

PURGATORY = 10


# Magic types

DIRECTDAMAGE           = 0
DIRECTHEAL             = 1
DURATIONDAMAGE         = 2
DURATIONHEAL           = 3

AREADAMAGE             = 4
AREAHEAL               = 5
AREADURATIONDAMAGE     = 6
AREADURATIONHEAL       = 7

DISPELL                = 8
AREADISSPELL           = 9

ROOMSPELL              = 10

SPELLID         = 0
STYPE           = 1
SCLASS          = 2
SPELLNAME       = 3
TARGET          = 4
GESTURE         = 5
S_END_TEXT      = 6
TEXTEFFECTS     = 7
DURATIONEFFECT  = 8
CASTER          = 9
SPELLVICTIM     = 10
COOLDOWN        = 11
DURATION        = 12
MNEMONIC        = 13
SPELLEFFECTS    = 14


# Magic stat effects
HP                = 0
MAXHP             = 1
POWER             = 2
MAXPOWER          = 3
BLIND             = 4
HELD              = 5
STEALTH           = 6
VISION            = 7
ATTACKS           = 8
ATTKSKILL         = 9
CRITICAL          = 10
BONUSDAMAGE       = 11
DAMAGEABSORB      = 12
KILLS             = 13
DEATHS            = 14
SNEAKING          = 15
MAXDAMAGE         = 16
MINDAMAGE         = 17
RESTING           = 18
MOVING            = 19
KILLSTREAK        = 20
STUN              = 21
DODGE             = 22
BS_MULTIPLIER     = 23

# Spell text identifiers
YOU              = 0
VICTIM           = 1
ROOM             = 2


# weaponText text identifiers
YOUHIT            = 0
YOUMISS           = 1
VICTIMHIT         = 2
VICTIMMISS        = 3
ROOMHIT           = 4
ROOMMISS          = 5
BS_HIT_YOU        = 6
BS_HIT_VICTIM     = 7
BS_HIT_ROOM       = 8

#############ANSI defines################
#          Foreground Colors
RESET              = chr(27) + "[0m"
BOLD               = chr(27) + "[1m"
ITALIC             = chr(27) + "[3m"
UNDERLINE          = chr(27) + "[4m"
INVERSE            = chr(27) + "[7m"
STRIKE             = chr(27) + "[9m"
BOLD_OFF           = chr(27) + "[22m"
ITALIC_OFF         = chr(27) + "[23m"
UNDERLINE_OFF      = chr(27) + "[24m"
INVERSE_OFF        = chr(27) + "[27m"
STRIKE_OFF         = chr(27) + "[29m"
BLACK              = chr(27) + "[30m"
RED                = chr(27) + "[31m"
GREEN              = chr(27) + "[32m"
BROWN              = chr(27) + "[33m"
YELLOW             = chr(27) + "[1;33m"
BLUE               = chr(27) + "[34m"
MAGENTA            = chr(27) + "[35m"
CYAN               = chr(27) + "[36m"
WHITE              = chr(27) + "[37m"
DEFAULT            = chr(27) + "[39m"
#        Light Foreground Colors
LRED               = chr(27) + "[1;31m"
LGREEN             = chr(27) + "[1;32m"
LBLUE              = chr(27) + "[1;34m"
LMAGENTA           = chr(27) + "[1;35m"
LCYAN              = chr(27) + "[1;36m"
#          Background Colors
B_BLACK            = chr(27) + "[40m"
B_RED              = chr(27) + "[41m"
B_GREEN            = chr(27) + "[42m"
B_YELLOW           = chr(27) + "[43m"
B_BLUE             = chr(27) + "[44m"
B_MAGENTA          = chr(27) + "[45m"
B_CYAN             = chr(27) + "[46m"
B_WHITE            = chr(27) + "[47m"
B_DEFAULT          = chr(27) + "[49m"

#          Cursor and delete line
DELETELINE         = chr(27) + "[2K"
FIRSTCOL           = chr(27) + "[80D"
CURPOS             = chr(27) + "6n"
SAVECUR            = chr(27) + "s"
RESTORECUR         = chr(27) + "u"
DELETELEFT         = chr(27) + "[1K"
CLEARSCREEN        = chr(27) + "[2J"
