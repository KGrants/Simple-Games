from SQL import conn
from SQL import cur
import random
import itertools
import statistics_SL as s
import sql_queries as sqlq
import sys


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


def game(home_team, away_team):
    # calculating points for both teams based on 30% random chance and offence/defence ratio
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
                   (Home_Team, Away_Team, Home_Points, Away_Points, Winner)
                   VALUES
                   (%s, %s, %s, %s, %s)""" % (home_team, away_team, home_points, away_points, winner))
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


def play_round(game_list):
    games = game_list
    game_count=0
    teams_played = []
    for i in games:
        if i[0] not in teams_played and i[1] not in teams_played:
            game(int(i[0]), int(i[1]))
            teams_played.append(i[0])
            teams_played.append(i[1])
            game_count += 1
            games.remove(i)
        if game_count == 5:
            break
    s.show_standings()
    s.show_top_scorers()
    return games


def playoffs():
    print("\nRegular Season MVP:")
    s.mvp()

    while True:
        p = sqlq.playoff_teams_sql()

        print()
        print(f"{p[0][1]} - {p[7][1]}")
        print(f"{p[3][1]} - {p[4][1]}")
        print(f"{p[1][1]} - {p[6][1]}")
        print(f"{p[2][1]} - {p[5][1]}")
        
        input("Press any key to simulate next round")

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
        
        print("SEMI-FINALS:")
        print(f"{v[0][1]} - {v[1][1]}")
        print(f"{v[2][1]} - {v[3][1]}")

        print("Press any key to simulate semi-finals")
        int(input(">").strip())

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
        print("Press 1 to simulate finals")
        int(input(">").strip())
        playoff_series(x[0][0],x[1][0])


        return
        

def playoff_series(team_a, team_b):
    wins_a = 0
    wins_b = 0

    while True:
        if wins_a == 4 or wins_b == 4:
            break;

        power = sqlq.team_power(team_a, team_b)
        home_points = int(100*(1+((power[0][1]-power[1][2])/100))*random.uniform(0.85,1.15))
        away_points = int(100*(1-((power[1][1]-power[0][2])/100))*random.uniform(0.85,1.15))

        if home_points == away_points:
            home_points += 1 if random.random() < 0.5 else -1

        winner = team_a if home_points > away_points else team_b

        if winner == team_a:
            wins_a+=1
            continue
        else:
            wins_b+=1
            continue

    team_name = sqlq.get_team_name_sql(winner)
    print(f"{team_name} won the series ({wins_a if wins_a>wins_b else wins_b}:{wins_a if wins_a<wins_b else wins_b})")
    return winner


