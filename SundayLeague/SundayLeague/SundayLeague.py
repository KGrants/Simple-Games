import Functions
import season

def main():
    while True:
        user_input = Functions.first_screen()                     # First screen alows the user to choose between actions

        function_dictionary = {1:Functions.create_team,           # Create a new team and write it to DB
                               2:Functions.create_player,         # Create a new player and write it to DB
                               3:season.season_screen,            # Start new season
                               4:Functions.show_all_teams,        # Shows all valid teams and players
                               5:Functions.show_one_team,         # Shows menu of all teams and then players of one team
                               6:Functions.drop_player,           # User can drop any player from any team
                               7:Functions.sign_player,           # User can sign any player from free agents to any team
                               8:Functions.create_custom_player,  # User can sign any player from free agents to any team
                               9:Functions.exit_app               # Exits application
                               }

        function_dictionary[user_input]()                         # Calls action that user added as input

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