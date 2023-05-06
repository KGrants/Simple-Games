import Functions as f
import statistics_SL as s
import season as se
import sql_queries as sqlq

def main():
    while True:
        user_input = f.first_screen()                     # First screen alows the user to choose between actions

        function_dictionary = {1:f.create_team,           # Create a new team and write it to DB
                               2:f.create_player,         # Create a new player and write it to DB
                               3:season_screen,           # Start new season
                               4:f.show_all_teams,        # Shows all valid teams and players
                               5:f.show_one_team,         # Shows menu of all teams and then players of one team
                               6:f.drop_player,           # User can drop any player from any team
                               7:f.sign_player,           # User can sign any player from free agents to any team
                               8:f.create_custom_player,  # User can sign any player from free agents to any team
                               9:f.exit_app               # Exits application
                               }

        function_dictionary[user_input]()                 # Calls action that user added as input


def season_screen():

    start_new_season = True
    games_list = se.generate_all_games()
    year = 2023
    season_round = 1

    if sqlq.check_team_count() != 10:                     # To start the season we need to have exactly 10 valid teams
        se.wrong_team_count()
        return

    if sqlq.check_player_count():                         # To start the season each team needs to have 5 valid players
        se.show_teams_above()
        return

    if start_new_season:                                  # If we need to start new game with clear DB, clear down Games and Player_scores
        f.reset_season()

    function_dictionary = {2:f.trade_players,             # Trade players between teams
                           3:f.drop_player,               # Drops player from team to free agents
                           4:f.sign_player,               # Sign player from free agents to team
                           5:f.show_all_teams             # Shows all teams and players
                           }

    while True:

        if season_round == 19:                            # If 18 rounds are done, let's go to playoffs
            print("\nRegular Season MVP:")
            s.mvp(year)
            print(f"\n{year} playoffs!")
            se.playoffs()
            # se.mvp_growth()                             # Need to implement
            # se.player_development()                     # Need to implement
            # se.random_development()                     # Need to implement
            season_round = 1
            year += 1
            start_new_season = False

        print(f"\n{year} season, round {season_round}:")
        user_input = f.season_menu()                      # season screen alows the user to choose between actions

        if user_input == 1:                               # Simulates games of one round and displays results
            games_list = se.play_round(games_list, year)  #
            season_round += 1                             # 

        elif user_input == 6:                             # break back to main screen
            break

        else:
            function_dictionary[user_input]()             # Action from function dictionary


if __name__ == '__main__':
    main()




# Current To-Do list: 

# Review game engine (From testing seams that one team always wins, but another team that is pretty much the same strenght, looses)

# Playoffs (need to make it not that ugly)
# Create new table where to store historical regular season and playoff results (now I need to add some data to it)
# New Season

# Start a new game or continue previous one (new game would drop data in Games and Player_Score tables) - test start_new_season
# Random player has spent a lot of time in training camp - implement random_development()
# At the end of season potential age decreases potential, potential affects offence and defence - implement player_development()
# MVP gets a boost to potential at the end of season - implement mvp_growth()  