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

#  Player status defines
LOGIN = 0
PLAYING = 1 

PURGATORY = 10


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