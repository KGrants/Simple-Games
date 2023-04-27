from SQL import conn
from SQL import cur
import random


def check_team_count():
    cur.execute("""SELECT Count(*) 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1
                   AND id != 999""")
    return False if cur.fetchone()[0] == 5 else True


def wrong_team_count():
    print("You have to have 10 teams to start the season,")
    print(f"Currently there are {check_team_count()} valid teams!")
    return


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


def show_teams_above():
    cur.execute("""SELECT t.id, t.name, COUNT(*)
                   FROM Players p
                   INNER JOIN Teams t ON t.id = p.Team
                   WHERE 1 = 1 
                   AND t.valid = 1
                   AND t.id != 999
                   GROUP by t.Name
                   HAVING COUNT(*) != 5""")
    for i in cur.fetchall():
        print(i[1],f"currently has {i[2]} players.")
        print("To start the season it needs to have 5 players.")
    return


def season_screen():
    year = 2023
    season_round = 0
    print(f"\n{year} season, round {season_round}:")
    options = ["1. Advance one Round", 
               "2. Trade player", 
               "3. Cut player", 
               "4. Sign free agent", 
               "5. Exit"]
    print("", *options, sep="\n")   # Print menu
    return int(input(">").strip())  # Get user input


def game(home_team, away_team):
    cur.execute("""SELECT Team, AVG(Offence), AVG(Defence)
                   FROM Players
                   WHERE 1 = 1 
                   AND Team in (%s, %s)
                   GROUP BY Team""" % (home_team, away_team))
    power = [i for i in cur.fetchall()]
    coef = power[0][1]-power[1][1]+power[0][2]-power[1][2]
    home_points = int(100*(1+(coef/100))*random.uniform(0.85,1.15))
    away_points = int(100*(1-(coef/100))*random.uniform(0.85,1.15))
    if home_points == away_points:
        home_points += 1 if random.random() < 0.5 else -1
    winner = home_team if home_points > away_points else away_team

    cur.execute("""INSERT INTO Games 
                   (Home_Team, Away_Team, Home_Points, Away_Points, Winner)
                   VALUES
                   (%s, %s, %s, %s, %s)""" % (home_team, away_team, home_points, away_points, winner))
    conn.commit()

    cur.execute("""SELECT * 
                   FROM Games
                   ORDER BY 1 DESC""")

    print(cur.fetchone())
    print(home_points)
    print(away_points)

    return