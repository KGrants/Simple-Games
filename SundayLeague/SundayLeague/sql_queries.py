from SQL import cur


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
    cur.execute("""SELECT T.Id, T.Name, COUNT(G.id)*3, POINTS.DIFF
                   FROM Teams T
                   LEFT JOIN Games G ON G.Winner = T.id AND G.Year = %s AND G.Game_Type = 'R'
                   LEFT JOIN (select T.id as ID, 
				                      sum(CASE 
				 	                      WHEN T.id = G.Home_Team 
					                      THEN G.Home_Points-G.Away_Points 
					                      ELSE 
						                    CASE 
						                    WHEN T.id = G.Away_Team 
						                    THEN G.Away_Points-G.Home_Points 
						                    ELSE 0 
						                    END 
					                      END) as DIFF 
		                       FROM Teams T 
		                       Left Join Games G on (G.Home_Team = T.id or G.Away_Team = T.id) and G.Year = %s and G.Game_Type = 'R'
		                       Group By T.id) as POINTS on POINTS.ID = T.id
                   WHERE 1 = 1
                   AND T.id != 999
                   GROUP BY T.Name
                   ORDER BY COUNT(G.id)*3 DESC, POINTS.DIFF DESC
				   """ % (year,year))
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


def team_power(team):
    cur.execute("""SELECT Team, AVG(Offence), AVG(Defence)
                   FROM Players
                   WHERE 1 = 1 
                   AND Team =  %s
				   order by Offence + Defence DESC
				   LIMIT 5""" % (team))
    return cur.fetchone()


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


def show_invalid_teams_sql():
    cur.execute("""SELECT id, name 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid != 1
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


def most_improved_sql(year):
    cur.execute("""with 
                   last_year as (						 
	                   select g.Year
		                     ,ps.Player_id
		                     ,sum(ps.Points) as Pts 
	                   from Player_Score ps
	                   inner join Games g on g.Id = ps.Game_id and g.Year = %s
	                   group by G.year
			                   ,ps.Player_id)
                   ,this_year as (
	                   select g.Year
		                     ,ps.Player_id
		                     ,sum(ps.Points) as Pts
	                   from Player_Score ps
	                   inner join Games g on g.Id = ps.Game_id and g.Year = %s
	                   group by G.year
			                   ,ps.Player_id)
                   select ty.Player_id, p.Name||' '||p.Surname as Player
	                     ,ty.Pts - ly.Pts 
                   from last_year ly
                   inner join this_year ty on ty.Player_id = ly.Player_id
                   inner join Players p on p.id = ty.Player_id
                   order by 3 desc
                   limit 1""" % (year-1, year))
    return


def draft_order_sql(year):
    cur.execute("""SELECT T.Id, T.Name, COUNT(G.id)*3, POINTS.DIFF
                   FROM Teams T
                   LEFT JOIN Games G ON G.Winner = T.id AND G.Year = %s AND G.Game_Type = 'R'
                   LEFT JOIN (select T.id as ID, 
				                      sum(CASE 
				 	                      WHEN T.id = G.Home_Team 
					                      THEN G.Home_Points-G.Away_Points 
					                      ELSE 
						                    CASE 
						                    WHEN T.id = G.Away_Team 
						                    THEN G.Away_Points-G.Home_Points 
						                    ELSE 0 
						                    END 
					                      END) as DIFF 
		                       FROM Teams T 
		                       Left Join Games G on (G.Home_Team = T.id or G.Away_Team = T.id) and G.Year = %s and G.Game_Type = 'R'
		                       Group By T.id) as POINTS on POINTS.ID = T.id
                   WHERE 1 = 1
                   AND T.id != 999
                   GROUP BY T.Name
                   ORDER BY COUNT(G.id)*3, POINTS.DIFF
				   """ % (year,year))
    return


def inactivate_team_sql(id):
    cur.execute("""UPADTE Teams
                   SET valid = 0 
                   WHERE Id = %s""" % id)


def release_all_players(id):
    cur.execute("""UPADTE Players
                   SET Team = 999 
                   WHERE Team = %s""" % id)