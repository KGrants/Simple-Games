import Functions as f
import statistics_SL as s
import season as se

def main():
    while True:
        user_input = f.first_screen()                     # First screen alows the user to choose between actions

        function_dictionary = {1:f.create_team,           # Create a new team and write it to DB
                               2:f.create_player,         # Create a new player and write it to DB
                               3:season_screen,            # Start new season
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
    games_list = f.generate_all_games()
    year = 2023
    season_round = 1

    if f.check_team_count() != 10:                        # To start the season we need to have exactly 10 valid teams
        f.wrong_team_count()
        return

    if f.check_player_count():                            # To start the season each team needs to have 5 valid players
        f.show_teams_above()
        return

    if start_new_season:                                  # If we need to start new game with clear DB, clear down Games and Player_scores
        f.reset_season()


    while True:

        if season_round == 19:                            # If 18 rounds are done, let's go to playoffs
            print(f"\n{year} playoffs!")
            se.playoffs()

        print(f"\n{year} season, round {season_round}:")
        user_input = f.season_menu()

        if user_input == 1:
            games_list = se.play_round(games_list)
            season_round += 1
            s.show_standings()
            s.show_top_scorers()

        elif user_input == 2:
            f.trade_players()

        elif user_input == 3:
            f.drop_player()

        elif user_input == 4:
            f.sign_player()

        elif user_input == 5:
            f.show_all_teams()

        else:
            break


if __name__ == '__main__':
    main()




# Current To-Do list: 

# Playoffs (need to make it not that ugly)
# Create new table where to store historical regular season and playoff results (now I need to add some data to it)
# New Season

# Start a new game or continue previous one (new game would drop data in Games and Player_Score tables)
# Random player has spent a lot of time in training camp
# At the end of season potential age decreases potential, potential affects offence and defence
# MVP gets a boost to potential at the end of season