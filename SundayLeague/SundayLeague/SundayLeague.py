import Functions
import season

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
            if season.check_team_count() != 10:
                season.wrong_team_count()
                continue

            # To start the season each team needs to have 5 valid players
            if season.check_player_count():
                season.show_teams_above()
                continue

            # Move to season screen
            season.season_screen()
        
        # Shows all valid teams and players 
        elif user_input == 4:
            Functions.show_all_teams()

        # Shows menu of all teams and then players of one team
        elif user_input == 5:
            Functions.show_one_team()

        # User can drop any player from any team
        elif user_input == 6:
            Functions.drop_player()

        # User can sign any player from free agents to any team
        elif user_input == 7:
            Functions.sign_player()

        # User can sign any player from free agents to any team
        elif user_input == 8:
            Functions.create_custom_player()

        # Exits application
        else:
            Functions.exit_app()


if __name__ == '__main__':
    main()


# Current To-Do list: 

# Playoffs
# Create statistics after season
# Create new table where to store historical regular season and playoff results
# New Season

# Start a new game or continue previous one (new game would drop data in Games and Player_Score tables)
# Random player has spent a lot of time in training camp
# at the end of season potential age decreases potential, potential affects offence and defence
# MVP gets a boost to potential at the end of season