--  ArenaMUD2 - A multiplayer combat game - http://arenamud.david-c-brown.com
--  Copyright (C) 2012 - David C Brown & Mark Richardson
--
--  This program is free software: you can redistribute it and/or modify
--  it under the terms of the GNU General Public License as published by
--  the Free Software Foundation, either version 3 of the License, or
--  (at your option) any later version.
--
--  This program is distributed in the hope that it will be useful,
--  but WITHOUT ANY WARRANTY; without even the implied warranty of
--  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
--  GNU General Public License for more details.
--
--  You should have received a copy of the GNU General Public License
--  along with this program.  If not, see <http://www.gnu.org/licenses/>.


CREATE TABLE classes ( 
    name                 VARCHAR( 15 )   PRIMARY KEY
                                         NOT NULL,
    attacks              INTEGER         NOT NULL,
    attackskill          INTEGER         NOT NULL
                                         CHECK ( attackskill > 0 
                                             AND
                                         attackskill < 100 ) 
                                         DEFAULT ( 50 ),
    maxdamage            INT             NOT NULL,
    mindamage            INT             NOT NULL,
    powerdesc            VARCHAR( 10 )   NOT NULL,
    maxhp                INTEGER         NOT NULL,
    stealth              BOOLEAN         NOT NULL
                                         DEFAULT ( 0 ),
    weapontextyouhit     VARCHAR( 100 )  NOT NULL,
    weapontextvictimhit  VARCHAR( 100 )  NOT NULL,
    weapontextroomhit    VARCHAR( 100 )  NOT NULL,
    classdesc            VARCHAR( 512 )  NOT NULL,
    weapontextyoumiss    VARCHAR( 100 )  NOT NULL,
    weapontextvictimmiss VARCHAR( 100 )  NOT NULL,
    weapontextroommiss   VARCHAR( 100 )  NOT NULL 
);


CREATE TABLE items ( 
    id            INTEGER         PRIMARY KEY AUTOINCREMENT
                               NOT NULL
                               UNIQUE,
    name          VARCHAR( 25 )   NOT NULL,
    itemaction    INTEGER         DEFAULT ( NULL ),
    usetext       VARCHAR( 25 )   DEFAULT ( NULL ),
    actiontext    VARCHAR( 256 )  DEFAULT ( NULL ),
    description   VARCHAR( 512)   NOT NULL 
                                  DEFAULT 'An Item.'
);