import sqlite3

conn = sqlite3.connect('SundayLeague.s3db')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Teams
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Valid INTEGER DEFAULT 1,
            Founded INTEGER DEFAULT 0)''')

cur.execute('''CREATE TABLE IF NOT EXISTS Players
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT,
            Surname TEXT,
            Age INTEGER,
            Offence INTEGER DEFAULT 0,
            Defence INTEGER DEFAULT 0,
            Potential INTEGER DEFAULT 0,
            Team INTEGER,
            CONSTRAINT FK_Team FOREIGN KEY (Team)
            REFERENCES Teams(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS Games
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
            Home_Team INTEGER,
            Away_Team INTEGER,
            Home_Points INTEGER DEFAULT 0,
            Away_Points INTEGER DEFAULT 0,
            Winner INTEGER,
            CONSTRAINT FK_Home_Team FOREIGN KEY (Home_Team) REFERENCES Teams(id),
            CONSTRAINT FK_Away_Team FOREIGN KEY (Away_Team) REFERENCES Teams(id),
            CONSTRAINT FK_Winner FOREIGN KEY (Winner) REFERENCES Teams(id))''')

cur.execute('''CREATE TABLE IF NOT EXISTS Player_Score
            (Player_id INTEGER,
            Team_id INTEGER,
            Game_id INTEGER,
            Points INTEGER DEFAULT 0,
            CONSTRAINT FK_Player_id FOREIGN KEY (Player_id) REFERENCES Players(id),
            CONSTRAINT FK_Team_id FOREIGN KEY (Team_id) REFERENCES Teams(id),
            CONSTRAINT FK_Game_id FOREIGN KEY (Game_id) REFERENCES Games(id))''')

conn.commit()

