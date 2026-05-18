IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='player' AND xtype='U')
BEGIN
    CREATE TABLE player (
        id   INT IDENTITY(1,1) PRIMARY KEY,
        nome VARCHAR(100) NOT NULL
    );
END;

IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='partida' AND xtype='U')
BEGIN
    CREATE TABLE partida (
        id        INT IDENTITY(1,1) PRIMARY KEY,
        resultado VARCHAR(50),
        player_id INT,
        FOREIGN KEY (player_id) REFERENCES player(id)
    );
END;