import Functions
from SQL import cur
    

def main():
    # First screen alows the user to choose between actions
    while True:
        user_input = Functions.first_screen()

        if user_input == 1:
            name = input("Please provide team name : ").strip()
            founded = int(input("Please provide year when team was founded : ").strip())
            Functions.create_team(name, founded)

        elif user_input == 2:
            team_id = int(input("Please provide team_id for which to create a player : ").strip())
            Functions.create_player(team_id)

        elif user_input == 3:
            # To start the season we need to have exactly 10 valid teams
            Functions.check_team_count()

            # To start the season each team needs to have 5 valid players
            Functions.check_player_count()

        elif user_input == 4:
            Functions.show_all_teams()

        else:
            Functions.exit_app()


if __name__ == '__main__':
    main()


# Currents To-Do list: 
# create show_teams
# create show_players
# add age column for Players
# at the end of season potential age decreases potential, potential affects offence and defence
# MVP gets a boost to potential at the end of season
# Implement Game system
# Random player has spent a lot of time in training camp
# Regular season and Playoffs
