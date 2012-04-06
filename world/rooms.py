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

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()




class Room:
    """
    Room class
    """
    
    def __init__(self):
        __tablename__ = "Rooms"
        
        id          = Column(String, unique=True)
                
        name        = Column(String(50), nullable=False)
        nospawn     = Column(bool, nullable=False)
        nw          = Column(Integer, nullable=True)
        n           = Column(Integer, nullable=True)
        ne          = Column(Integer, nullable=True)
        e           = Column(Integer, nullable=True)
        se          = Column(Integer, nullable=True)
        s           = Column(Integer, nullable=True)
        sw          = Column(Integer, nullable=True)
        w           = Column(Integer, nullable=True)
        u           = Column(Integer, nullable=True)
        w           = Column(Integer, nullable=True)
        
        spell       = Column(Integer, nullable=True)
        light       = Column(Integer, nullable=False)
        
        
        players     = {}
        pSpells     = []
        items       = {}
        
        
        
    def __repr__(self):
        """
        Gets room name
        """
        
        return self.name
    
    


        
        
    def getNortWesthxit(self):
        if self.nw is not None:
            return self.nw.exitRoom(self.id)

        
    def getNorthExit(self):
        if self.n is not None:
            return self.n.exitRoom(self.id)

        
    def getNorthEastExit(self):
        if self.ne is not None:
            return self.ne.exitRoom(self.id)

        
    def getEastExit(self):
        if self.e is not None:
            return self.e.exitRoom(self.id)
        

    def getSouthEastExit(self):
        if self.se is not None:
            return self.se.exitRoom(self.id)
        
        
    def getSouthExit(self):
        if self.s is not None:
            return self.s.exitRoom(self.id)
        
        
    def getSouthWestExit(self):
        if self.sw is not None:
            return self.sw.exitRoom(self.id)
        
        
    def getWestExit(self):
        if self.w is not None:
            return self.w.xitRoom(self.id)
        
        
    def getUpExit(self):
        if self.u is not None:
            return self.u.exitRoom(self.id)
        
        
    def getDownExit(self):
        if self.d is not None:
            return self.d.exitRoom(self.id)
                
                
        