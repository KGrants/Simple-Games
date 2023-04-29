from re import I
from SQL import conn
from SQL import cur
import random
import itertools
from Functions import show_one_team
from Functions import trade_players
from Functions import drop_player
from Functions import sign_player
import statistics_SL as s




def check_team_count():
    cur.execute("""SELECT Count(*) 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1
                   AND id != 999""")
    return cur.fetchone()[0]


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



def game(home_team, away_team):
    # calculating points for both teams based on 30% random chance and offence/defence ratio
    cur.execute("""SELECT Team, AVG(Offence), AVG(Defence)
                   FROM Players
                   WHERE 1 = 1 
                   AND Team in (%s, %s)
                   GROUP BY Team""" % (home_team, away_team))
    power = [i for i in cur.fetchall()]
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
    cur.execute("""SELECT Offence + Defence
                   FROM Players
                   WHERE 1 = 1
                   AND Team = %s
                   ORDER BY Id""" % (team_id))
    ratings = [i[0] for i in cur.fetchall()]
    rat_weight = points/sum(ratings)
    player_points = []

    for i in range(4):
        player_points.append(int(rat_weight*ratings[i]))
    player_points.append(points-sum(player_points))

    cur.execute("""SELECT id
                   FROM Players
                   WHERE 1 = 1
                   AND Team = %s
                   ORDER BY Id""" % (team_id))
    ids = [i[0] for i in cur.fetchall()]

    return {ids[i]: player_points[i] for i in range(5)}


def generate_all_games():
    cur.execute("""SELECT id
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1
                   AND id != 999""")
    team_list = [i[0] for i in cur.fetchall()]
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
    return games



def season_screen():
    ############# Need to implement ###############
    ############# if new season, create new list of permutations ###############
    ############# If continue previous season, don't touch ###############

    games_list = generate_all_games()
    year = 2023
    season_round = 0
    cur.execute("""DELETE FROM Games""")
    cur.execute("""DELETE FROM Player_Score""")
    conn.commit()


    while True:
        print(f"\n{year} season, round {season_round}:")
        options = ["1. Advance one Round", 
                   "2. Trade player", 
                   "3. Cut player", 
                   "4. Sign free agent", 
                   "5. Exit"]
        print("", *options, sep="\n")   # Print menu
        user_input = int(input(">").strip())  # Get user input

        if user_input == 1:

            games_list = play_round(games_list)
            season_round += 1
            s.show_standings()
            s.show_top_scorers()
            

        elif user_input == 2:
            print("First player:")
            show_one_team()
            first_to_trade = int(input("Please provide id of player that needs to be traded : "))
            print("Second player:")
            show_one_team()
            second_to_trade = int(input("Please provide id of player that needs to be traded : "))
            trade_players(first_to_trade, second_to_trade)

        elif user_input == 3:
            drop_player()

        elif user_input == 4:
            sign_player()

        else:
            break