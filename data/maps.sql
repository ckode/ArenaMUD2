CREATE TABLE rooms ( 
    id    INT            PRIMARY KEY
                         CHECK ( id > -1 
                             AND
                         id < 1000 ),
    name  VARCHAR( 25 )  NOT NULL
                         DEFAULT 'Room',
    n     INT            DEFAULT ( NULL ),
    ne    INT            DEFAULT ( NULL ),
    e     INT            DEFAULT ( NULL ),
    se    INT            DEFAULT ( NULL ),
    s     INT            DEFAULT ( NULL ),
    sw    INT            DEFAULT ( NULL ),
    w     INT            DEFAULT ( NULL ),
    nw    INT            DEFAULT ( NULL ),
    u     INT            DEFAULT ( NULL ),
    d     INT            DEFAULT ( NULL ),
    spell INT            DEFAULT ( NULL ),
    light INT            NOT NULL
                         DEFAULT ( 3 ) 
);


CREATE TABLE doors ( 
    id    INTEGER   PRIMARY KEY AUTOINCREMENT
                    UNIQUE ON CONFLICT ROLLBACK,
    exit1 INT( 0 )  NOT NULL
                    CHECK ( exit1 > -1 
                        AND
                    exit1 < 1000 ),
    exit2 INT( 0 )  NOT NULL
                    CHECK ( exit2 > -1 
                        AND
                    exit2 < 1000 ) 
);



-- Table: maplevelnames
CREATE TABLE maplevelnames ( 
    levelid INT            PRIMARY KEY
                           UNIQUE,
    name    VARCHAR( 50 )  NOT NULL 
);
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (9, 'Level 9');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (0, 'Level 0');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (1, 'Level 1');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (2, 'Level 2');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (3, 'Level 3');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (4, 'Level 4');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (5, 'Level 5');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (6, 'Level 6');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (7, 'Level 7');
INSERT INTO [maplevelnames] ([levelid], [name]) VALUES (8, 'Level 8');