from SQL import conn
from SQL import cur
import random
import itertools
import statistics_SL as s
import sql_queries as sqlq
import pandas as pd
import Functions as f


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

    home_power = sqlq.team_power(home_team)
    away_power = sqlq.team_power(away_team)
    home_points = int(100*(1+((home_power[1]-away_power[2])/100))*random.uniform(0.88,1.18))
    away_points = int(100*(1+((away_power[1]-home_power[2])/100))*random.uniform(0.85,1.15))

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
    game_id = sqlq.get_last_game_id_sql()

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


def playoffs(year):

    while True:
        sqlq.team_stand_sql(year)
        playoff_tree = [i for i in cur.fetchmany(8)]

        for i in range(4):
            print(f"{playoff_tree[(0,3,1,2)[i]][1]} - {playoff_tree[(7,4,6,5)[i]][1]}")

        input(f"\nPress Enter to simulate next round\n")

        second_round = []
        for i in range(4):
            second_round.append(playoff_series(playoff_tree[(0,3,1,2)[i]][0],playoff_tree[(7,4,6,5)[i]][0]))
        
        playoff_tree = next_round(playoff_tree, second_round)
        
        print(f"\nSEMI-FINALS:")
        print(f"{playoff_tree[0][1]} - {playoff_tree[1][1]}")
        print(f"{playoff_tree[2][1]} - {playoff_tree[3][1]}")

        input(f"\nPress Enter to simulate next round\n")

        third_round = []
        third_round.append(playoff_series(playoff_tree[0][0],playoff_tree[1][0]))
        third_round.append(playoff_series(playoff_tree[2][0],playoff_tree[3][0]))

        playoff_tree = next_round(playoff_tree, third_round)
        
        print("FINALS:")
        print(f"{playoff_tree[0][1]} - {playoff_tree[1][1]}")

        input(f"\nPress Enter to simulate next round\n")
        playoff_series(playoff_tree[0][0],playoff_tree[1][0])

        return


def next_round(full_list, winner_list):
    next_round_list = []
    for winner in winner_list: #i
            for team in full_list: #j
                if winner == team[0]:
                    next_round_list.append(team)
                    continue
    return next_round_list
        

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


def mvp_growth(year):
    mvp = s.mvp(year)[2]

    cur.execute("""UPDATE Players 
                   SET 
                   Offence = CASE WHEN Offence + 5 > 100 THEN 100 ELSE Offence +5 END,
	               Defence = CASE WHEN Defence + 5 > 100 THEN 100 ELSE Defence +5 END
                   WHERE id = %s""" % (mvp))
    conn.commit()
    return


def player_development():
    cur.execute("""UPDATE Players 
                   SET
                   Offence   = Offence + cast((cast(abs((random() % 100)) as float)/100)*(Potential-70) as INTEGER),
                   Defence   = Defence + cast((cast(abs((random() % 100)) as float)/100)*(Potential-70) as INTEGER),
                   Potential = CASE WHEN Age < 23 THEN Potential ELSE CASE WHEN Age < 27 THEN Potential - 5 ELSE Potential - 10 END END,
                   Age = Age + 1""")
    conn.commit()
    cur.execute("""UPDATE Players 
                   SET
                   Offence   = CASE WHEN Offence > 100 THEN 100 ELSE Offence END,
                   Defence   = CASE WHEN Defence > 100 THEN 100 ELSE Defence END,
                   Potential = CASE WHEN Potential < 0 THEN 0 ELSE Potential END""")
    conn.commit()
    return


def random_development():
    cur.execute("""UPDATE PLayers
                   SET
                   Offence = CASE WHEN Offence + 10 > 100 THEN 100 ELSE Offence +10 END,
	               Defence = CASE WHEN Defence + 10 > 100 THEN 100 ELSE Defence +10 END,
                   Potential = CASE WHEN Potential + 10 > 100 THEN 100 ELSE Potential +10 END
                   WHERE 1 = 1
                   AND Id in (
                        select Id from Players
                        order by RANDOM()
                        limit 1)""")
    conn.commit()
    return

def draft(year):
    f.draft_team()
    for i in range(10): f.create_player(limit = 24, team_id = 998)
    f.show_players(998)

    df = s.show_draft_order(year)
    for team in df['Team'].values:
        print(f"In {year} draft {team} selects:")
        to_sign = int(input())
        to_team = df.loc[df['Team'] == team, 'Id'].iloc[0]
        sqlq.sign_player_sql(to_team, to_sign)


