import Functions
from SQL import cur
    

def main():
    while True:
        # First screen alows the user to choose between actions
        user_input = Functions.first_screen()

        # Create a new team and write it to DB
        if user_input == 1:
            name = input("Please provide team name : ").strip()
            founded = int(input("Please provide year when team was founded : ").strip())
            Functions.create_team(name, founded)

        # Create a new player and write it to DB
        elif user_input == 2:
            team_id = int(input("Please provide team_id for which to create a player : ").strip())
            Functions.create_player(team_id)

        # Start new season
        elif user_input == 3:
            # To start the season we need to have exactly 10 valid teams
            Functions.check_team_count()

            # To start the season each team needs to have 5 valid players
            Functions.check_player_count()
        
        # Shows all valid teams and players 
        elif user_input == 4:
            Functions.show_all_teams()

        # Shows menu of all teams and then players of one team
        elif user_input == 5:
            Functions.show_one_team()

        # User can drop any player from any team
        elif user_input == 6:
            Functions.drop_player()

        # Exits application
        else:
            Functions.exit_app()


if __name__ == '__main__':
    main()


# Current To-Do list: 
# Cut/drop player
# at the end of season potential age decreases potential, potential affects offence and defence
# MVP gets a boost to potential at the end of season
# Implement Game system
# Random player has spent a lot of time in training camp
# Regular season and Playoffs
