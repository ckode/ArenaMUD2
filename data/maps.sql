CREATE TABLE rooms (
    id    INT            PRIMARY KEY
                         CHECK ( id > -1 
                             AND
                         id < 1000 ),
    name  VARCHAR( 25 ) NOT NULL DEFAULT 'Room',
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
    light INT   NOT NULL DEFAULT ( 3 )
);


CREATE TABLE doors (
    id         INT            PRIMARY KEY,
    exit1      INT            NOT NULL
                              CHECK ( exit1 > -1
                                   AND
                              exit1 < 1000 ),
    exit2      INT            NOT NULL
                              CHECK ( exit2 > -1
                                   AND
                              exit2 < 1000 )
);