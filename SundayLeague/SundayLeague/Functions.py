from SQL import conn
from SQL import cur
import names
import random
import sys
import statistics
import sql_queries as sqlq
import pandas as pd


def first_screen():
    """Prints out first screen menu and obtains users choice"""

    print("Welcome to Sunday League NBA:")
    options = ["1. Create a Team", 
               "2. Create a Player", 
               "3. Start the Season", 
               "4. Show all Teams", 
               "5. Show one team", 
               "6. Drop Player from team",
               "7. Sign a free agent",
               "8. Create Custom Player",
               "9. Exit"]
    print("", *options, sep="\n")

    user_input = input(">").strip()
    if user_input in "12345678":
        return int(user_input)
    else:
        return 9


def season_menu():
    """Prints out season screen menu and obtains users choice"""

    options = ["1. Advance one Round", 
               "2. Trade player", 
               "3. Cut player", 
               "4. Sign free agent",
               "5. Show all teams",
               "6. Exit"]
    print("", *options, sep="\n")
    try:
        user_input = input(">")
        return int(user_input) if int(user_input) in [1,2,3,4,5,6] else 6
    except Exception as e:
        print(f"Wrong user input: {e}")


def create_team():
    """Create a new team and write it to DB"""

    try:
        name = input("Please provide team name : ").strip()
        founded = int(input("Please provide year when team was founded (YYYY) : ").strip())

        if name != "Free Agents":
            sqlq.create_team_sql(name, founded)
        else:
            create_team("Free Agents", 9999)
        conn.commit()
        print(f"{name} was created successfully!\n")
    except Exception as e:
        print(f"Error creating team: {e}")


def reset_season():
    """if we start a new game, delete entries in Games and Player_Score"""

    cur.execute("""DELETE FROM Games""")
    cur.execute("""DELETE FROM Player_Score""")
    conn.commit()


def create_player():
    """Creates new random player"""

    team_id     = int(input("Please provide team_id for which to create a player : ").strip())
    first_name  = names.get_first_name(gender="male")
    last_name   = names.get_last_name()
    offence     = random.randint(50, 100)
    defence     = random.randint(50, 100)
    age         = random.randint(16, 32)
    potential   = int(100 - random.randint(0, 50) * ((age**2)/32)/16)
    try:
        cur.execute("""INSERT INTO Players
                       (Name, Surname, Age, Offence, Defence, Potential, Team)
                       VALUES
                       ('%s', '%s', '%s', %s, %s, %s, %s)"""
                       % (first_name, last_name, age, offence, defence, potential, team_id))
        conn.commit()
        print(f"{first_name} {last_name} was created successfully!")
        print(f"Age = {age}\nOffence = {offence}\nDefence = {defence}\nPotential = {potential}\n")
    except Exception as e:
        print(f"Error creating player: {e}")


def create_custom_player():
    """Creates new custom player"""
    try:
        team_id     = int(input("Team id:"))
        first_name  = input("Name:")
        last_name   = input("Surname:")
        offence     = int(input("Offence:"))
        defence     = int(input("Defence:"))
        age         = int(input("Age:"))
        potential   = int(input("Potential:"))
        cur.execute("""INSERT INTO Players
                       (Name, Surname, Age, Offence, Defence, Potential, Team)
                       VALUES
                       ('%s', '%s', '%s', %s, %s, %s, %s)"""
                       % (first_name, last_name, age, offence, defence, potential, team_id))
        conn.commit()
        print(f"{first_name} {last_name} was created successfully!")
        print(f"Age = {age}\nOffence = {offence}\nDefence = {defence}\nPotential = {potential}\n")
    except Exception as e:
        print(f"Error creating player: {e}")


def show_players(team_id):
    """Displays all players for specific team"""

    #players = sqlq.show_players_sql(team_id)
    df = pd.DataFrame(sqlq.show_players_sql(team_id), columns = ['Id', 'Name', 'Surname', 'Age', 'Offence', 'Defence', 'Potential', 'Team'])
    df.index = [i for i in range(1,6)]
    #newdf = df[['Age', 'Offence', 'Defence', 'Potential']]
    print(df[['Name', 'Surname', 'Age', 'Offence', 'Defence', 'Potential']])
    print(f"\n{df[['Age', 'Offence', 'Defence', 'Potential']].mean().to_string()}\n")
    return


def show_all_teams():
    """Displays all teams and players"""

    teams = sqlq.show_all_teams_sql()
    for i in teams:
        print(f"\n{i[1]} (id = {i[0]}) :")
        show_players(i[0])
    print()
    return


def show_one_team():
    """Displays one team and players"""
    teams = sqlq.show_one_team_sql()
    for i in teams:
        print(f"{i[0]} - {i[1]}:")
    try:
        user_input = int(input("Please choose id of team you want to see players for: "))
        team_name = [i[1] for i in teams if i[0] == user_input]
        print(f"\n{team_name[0]} players:")
        show_players(user_input)
    except Exception as e:
        print(f"Error: {e}")


def drop_player():
    """Release one player from any team to free agents"""

    show_one_team()
    try:
        drop_id = int(input("Please provide id of player that you want to drop: "))
        sqlq.drop_player_sql(drop_id)
        conn.commit()
        print("Player has been released to Free Agents")
    except Exception as e:
        print(f"Error: {e}")


def free_agents():
    """Check if Free Agents exists, if not - creates"""

    cur.execute("""SELECT count(*)
                    FROM Teams
                    WHERE id = 999""")
    if cur.fetchone()[0] == 0:
        create_team("Free Agents", 9999)


def trade_players():
    """Exchanges two players between two teams"""
    try:
        print("First player:")
        show_one_team()
        one_id = int(input("Please provide id of player that needs to be traded : "))
        one_team_id = sqlq.get_trade_dets_sql(one_id)

        print("Second player:")
        show_one_team()
        two_id = int(input("Please provide id of player that needs to be traded : "))
        two_team_id = sqlq.get_trade_dets_sql(two_id)

        sqlq.trade_players_sql(two_team_id, one_id)
        sqlq.trade_players_sql(one_team_id, two_id)
        conn.commit()

        print("Trade has been successfully done!")
    except Exception as e:
        print(f"Error: {e}")


def sign_player():
    """Assign a player from free agents to any team"""

    print("Free Agents:")
    show_players(999)
    try:
        to_sign = int(input("Choose a free agent id to sign:"))
        free_agents = sqlq.show_free_agents_sql()

        if to_sign not in free_agents:
            print("You can't sign a player who is not a free agent!")
            return

        teams = sqlq.show_all_teams_sql()
        for i in teams:
            print(f"{i[0]} - {i[1]}")
        print(f"\n")
        to_team = int(input("Choose to which team sign this player:"))

        sqlq.sign_player_sql(to_team, to_sign)
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")


def exit_app():
    """Close connection and exit application"""

    print("\nBye!")
    conn.close()
    sys.exit()