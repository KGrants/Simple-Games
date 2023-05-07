from SQL import cur

def mvp_query():
    cur.execute("""SELECT T.Name, COUNT(G.id)*3
                   FROM Teams T
                   LEFT JOIN Games G ON G.Winner = T.id
                   GROUP BY T.Name
                   ORDER BY 2 DESC
                   LIMIT 3""")
    return [i[0] for i in cur.fetchall()]


def top_scorers_sql(year):
    cur.execute("""WITH HighScorers AS
                   (
                   SELECT 
                   P.id, 
                   P.Name, 
                   P.Surname, 
                   T.Name,
                   SUM(PS.Points) OVER(PARTITION BY P.id) AS TotalPoints,
                   ROW_NUMBER() OVER(PARTITION BY P.id) as RowNum
                   FROM Players P
                   LEFT JOIN Player_Score PS ON PS.Player_id = P.id
                   INNER JOIN Games G on G.id = PS.Game_id AND G.Year = %s
                   LEFT JOIN Teams T ON T.id = P.Team
                   ORDER BY 5 DESC
                   )
                   SELECT * 
                   FROM HighScorers
                   WHERE RowNum = 1
                   LIMIT 5""" % (year))
    return


def team_stand_sql(year):
    cur.execute("""SELECT T.Name, COUNT(G.id)*3
                   FROM Teams T
                   LEFT JOIN Games G ON G.Winner = T.id AND G.Year = %s
                   WHERE T.id != 999
                   GROUP BY T.Name
                   ORDER BY 2 DESC""" % (year))
    return


def check_team_count():
    cur.execute("""SELECT Count(*) 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1
                   AND id != 999""")
    return cur.fetchone()[0]


def check_player_count():
    cur.execute("""SELECT t.Name, COUNT(*)
                   FROM Players p
                   INNER JOIN Teams t ON t.id = p.Team
                   WHERE 1 = 1 
                   AND t.valid = 1
                   AND t.id != 999
                   GROUP by t.Name
                   HAVING COUNT(*) != 5""")
    return False if cur.fetchone() == None else True


def player_count_sql():
    cur.execute("""SELECT t.id, t.name, COUNT(*)
                   FROM Players p
                   INNER JOIN Teams t ON t.id = p.Team
                   WHERE 1 = 1 
                   AND t.valid = 1
                   AND t.id != 999
                   GROUP by t.Name
                   HAVING COUNT(*) != 5""")
    return


def team_power(home_team, away_team):
    cur.execute("""SELECT Team, AVG(Offence), AVG(Defence)
                   FROM Players
                   WHERE 1 = 1 
                   AND Team in (%s, %s)
                   GROUP BY Team""" % (home_team, away_team))
    return [i for i in cur.fetchall()]


def player_power_sql(team_id):
    cur.execute("""SELECT Offence + Defence
                   FROM Players
                   WHERE 1 = 1
                   AND Team = %s
                   ORDER BY Id""" % (team_id))
    return [i[0] for i in cur.fetchall()]


def player_id_sql(team_id):
    cur.execute("""SELECT id
                   FROM Players
                   WHERE 1 = 1
                   AND Team = %s
                   ORDER BY Id""" % (team_id))
    return [i[0] for i in cur.fetchall()]


def gen_all_games_sql():
    cur.execute("""SELECT id
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1
                   AND id != 999""")
    return [i[0] for i in cur.fetchall()]


def get_team_name_sql(team):
    cur.execute("""SELECT Name
                   FROM Teams
                   WHERE 1 = 1
                   AND id = %s""" % (team))
    return cur.fetchone()[0]


def playoff_teams_sql():
    cur.execute("""SELECT T.id, T.Name, COUNT(G.id)*3
                   FROM Teams T
                   LEFT JOIN Games G ON G.Winner = T.id
                   GROUP BY T.Name
                   ORDER BY 3 DESC
                   LIMIT 8""")
    return [i for i in cur.fetchall()]


def show_players_sql(team_id):
    cur.execute("""SELECT * 
                   FROM Players
                   WHERE 1 = 1
                   AND Team = %s""" % (team_id))
    return [i for i in cur.fetchall()]


def show_all_teams_sql():
    cur.execute("""SELECT id, name 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1
                   AND id != 999""")
    return [i for i in cur.fetchall()]


def show_one_team_sql():
    cur.execute("""SELECT id, name 
                   FROM Teams""")
    return [i for i in cur.fetchall()]


def drop_player_sql(drop_id):
    cur.execute("""UPDATE Players
                    SET Team = 999
                    WHERE id = %s""" % (drop_id))
    return


def sign_player_sql(to_team, to_sign):
    cur.execute("""UPDATE Players
                   SET team = %s 
                   WHERE id = %s""" % (to_team, to_sign))
    return


def get_trade_dets_sql(one_id):
    cur.execute("""SELECT id, Team
                   FROM Players 
                   WHERE 1 = 1
                   AND id = %s""" % (one_id))
    return cur.fetchone()[1]


def trade_players_sql(team_id, player_id):
    cur.execute("""UPDATE Players
                   SET Team = %s
                   WHERE id = %s""" % (team_id, player_id))
    return


def show_free_agents_sql():
    cur.execute("""SELECT id 
                    FROM Players
                    WHERE 1 = 1
                    AND team = 999""")
    return [i[0] for i in cur.fetchall()]


def create_team_sql(name, founded):
    cur.execute("""INSERT INTO Teams (Name, Founded)
                   VALUES ('%s', %s);"""
                   % (name, founded))
    return


def get_last_game_id_sql():
    cur.execute("""SELECT * 
                   FROM Games
                   ORDER BY 1 DESC""")
    return cur.fetchone()[0]