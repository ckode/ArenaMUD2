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

import unittest
import string

from utils.text import cleanPlayerInput
from character.communicate import LGREEN, WHITE, YELLOW, BLACK


class test_text(unittest.TestCase):
    """
    Tests utils.text.cleanPlayerInput()
    """
    
    def setUp(self):
        self.unprintable = "This {0}has {1}unprintables {2}in it.".format(LGREEN, WHITE, BLACK)
        self.backspace = "This has a back space{0}".format( chr(0x08) )
        self.unprintableLen = len(self.unprintable)  
        self.backspaceLen = len(self.backspace)
        
        
    def testRemoveUnprintables(self):
        # Remove three ANSI color codes
        cleaned = cleanPlayerInput(self.unprintable)
        assert( (self.unprintableLen - len(cleaned)) is 3 )
        
        # Not sure why this is comes out as 2 since backspace is 1 character?
        cleaned = cleanPlayerInput(self.backspace)
        assert( (self.backspaceLen - len(cleaned)) is 2)
        
    def testAllCharsPrintable(self):
        cleaned = cleanPlayerInput(self.unprintable) + cleanPlayerInput(self.backspace)
        for each in cleaned:
            assert(each in string.printable)
            
            
if __name__ is "__main__":
    unittest.main()
            
        
    