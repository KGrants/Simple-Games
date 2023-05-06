from SQL import conn
from SQL import cur
import random
import itertools
import statistics_SL as s
import sql_queries as sqlq


def wrong_team_count():
    print(f"\nYou have to have 10 teams to start the season,")
    print(f"Currently there are {sqlq.check_team_count()} valid teams!")
    return


def show_teams_above():
    sqlq.player_count_sql()
    for i in cur.fetchall():
        print(f"{i[1]} currently has {i[2]} players.")
        print(f"To start the season it needs to have 5 players.")
    return


def game(home_team, away_team, year, g_type):
    """Simulating a single game, distributing points between players, writting to DB"""

    power = sqlq.team_power(home_team, away_team)
    home_points = int(100*(1+((power[0][1]-power[1][2])/100))*random.uniform(0.88,1.18))
    away_points = int(100*(1-((power[1][1]-power[0][2])/100))*random.uniform(0.85,1.15))

    # If there is a tie randomly add or remove one point from home team
    if home_points == away_points:
        home_points += 1 if random.random() < 0.5 else -1

    # Declaring winner
    winner = home_team if home_points > away_points else away_team

    # Inserting teams results in Games table
    cur.execute("""INSERT INTO Games 
                   (Year, Game_Type, Home_Team, Away_Team, Home_Points, Away_Points, Winner)
                   VALUES
                   (%s, '%s', %s, %s, %s, %s, %s)""" % (year, g_type, home_team, away_team, home_points, away_points, winner))
    conn.commit()

    # Extracting game_id so that we can link player stats from Player_Score table
    cur.execute("""SELECT * 
                   FROM Games
                   ORDER BY 1 DESC""")
    game_id = cur.fetchone()[0]

    # Generating individual points for all players and inserting them in Player_Score table.
    h_player_points = point_distribution(home_points,home_team)
    a_player_points = point_distribution(away_points,away_team)

    for key in h_player_points:
        cur.execute("""INSERT INTO Player_Score
                       VALUES
                       (%s, %s, %s, %s)""" % (key,home_team,game_id,h_player_points[key]))

    for key in a_player_points:
        cur.execute("""INSERT INTO Player_Score
                       VALUES
                       (%s, %s, %s, %s)""" % (key,away_team,game_id,a_player_points[key]))
    return


def point_distribution(points, team_id):
    ratings = sqlq.player_power_sql(team_id)
    rat_weight = points/sum(ratings)
    player_points = []

    for i in range(4):
        player_points.append(int(rat_weight*ratings[i]))
    player_points.append(points-sum(player_points))

    ids = sqlq.player_id_sql(team_id)

    return {ids[i]: player_points[i] for i in range(5)}


def generate_all_games():
    team_list = sqlq.gen_all_games_sql()
    return list(itertools.permutations(team_list,2))


def play_round(game_list, year):
    for i in game_list:
        game(i[0], i[1], year, "R")
    s.show_standings(year)
    s.show_top_scorers(year)
    return 


def make_day(num_teams, day):
    lst = list(range(1, num_teams + 1))
    day %= (num_teams - 1) 
    if day:                
        lst = lst[:1] + lst[-day:] + lst[1:-day]
    half = num_teams // 2
    return list(zip(lst[:half], lst[half:][::-1]))


def make_schedule(num_teams):
    schedule = [make_day(num_teams, day) for day in range(num_teams - 1)]
    swapped = [[(away, home) for home, away in day] for day in schedule]
    return schedule + swapped


def playoffs():

    while True:
        p = sqlq.playoff_teams_sql()

        print()
        print(f"{p[0][1]} - {p[7][1]}")
        print(f"{p[3][1]} - {p[4][1]}")
        print(f"{p[1][1]} - {p[6][1]}")
        print(f"{p[2][1]} - {p[5][1]}")
        
        input(f"\nPress Enter to simulate next round\n")

        second_round = []
        second_round.append(playoff_series(p[0][0],p[7][0]))
        second_round.append(playoff_series(p[3][0],p[4][0]))
        second_round.append(playoff_series(p[1][0],p[6][0]))
        second_round.append(playoff_series(p[2][0],p[5][0]))
        
        v = []
        for i in second_round:
            for j in p:
                if i == j[0]:
                    v.append(j)
                    continue
        
        print(f"\nSEMI-FINALS:")
        print(f"{v[0][1]} - {v[1][1]}")
        print(f"{v[2][1]} - {v[3][1]}")

        input(f"\nPress Enter to simulate next round\n")

        third_round = []
        third_round.append(playoff_series(v[0][0],v[1][0]))
        third_round.append(playoff_series(v[2][0],v[3][0]))

        x = []

        for i in third_round:
            for j in v:
                if i == j[0]:
                    x.append(j)
                    continue
        
        print("FINALS:")
        print(f"{x[0][1]} - {x[1][1]}")

        input(f"\nPress Enter to simulate next round\n")
        playoff_series(x[0][0],x[1][0])

        return
        

def playoff_series(team_a, team_b):
    """Simulates series till 4 wins and returns winner team id"""
    wins_a = 0
    wins_b = 0
    year = cur.execute("""SELECT MAX(Year) FROM Games""").fetchone()[0]
    game_count = 0
    series = "1100101"

    while True:
        game(team_a if series[game_count] == '1' else team_b, team_b if series[game_count] == '1' else team_a, year, "P")
        winner = cur.execute("""SELECT Winner from Games ORDER BY id DESC LIMIT 1""").fetchone()[0]

        wins_a += (winner == team_a)
        wins_b += (winner == team_b)
        game_count += 1

        if wins_a == 4 or wins_b == 4:
            break

    team_name = sqlq.get_team_name_sql(winner)
    print(f"{team_name} won the series ({wins_a if wins_a>wins_b else wins_b}:{wins_a if wins_a<wins_b else wins_b})")
    return winner


