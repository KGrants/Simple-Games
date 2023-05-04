from SQL import conn
from SQL import cur
import names
import random
import sys
import statistics


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


def create_team():
    """Create a new team and write it to DB"""
    name = input("Please provide team name : ").strip()
    founded = input("Please provide year when team was founded (YYYY) : ").strip()
    if founded.isnumeric():
        founded = int(founded)
    else:
        print("You did not add a valid year.")
        return
    if name != "Free Agents":
        cur.execute("""INSERT INTO Teams (Name, Founded)
                       VALUES ('%s', %s);"""
                       % (name, founded))
    else:
        cur.execute("""INSERT INTO Teams (Id, Name, Founded)
                       VALUES (999, '%s', %s);"""
                       % (name, founded))
    conn.commit()
    print(f"{name} was created successfully!\n")
    return


def create_player():
    team_id = int(input("Please provide team_id for which to create a player : ").strip())
    first_name = names.get_first_name(gender="male")
    last_name = names.get_last_name()
    offence = random.randint(50, 100)
    defence = random.randint(50, 100)
    age = random.randint(16, 32)
    potential = int(100 - random.randint(0, 50) * ((age**2)/32)/16)

    cur.execute("""INSERT INTO Players
                   (Name, Surname, Age, Offence, Defence, Potential, Team)
                   VALUES
                   ('%s', '%s', '%s', %s, %s, %s, %s)"""
                   % (first_name, last_name, age, offence, defence, potential, team_id))
    conn.commit()
    print(f"{first_name} {last_name} was created successfully!")
    print(f"Age = {age}\nOffence = {offence}\nDefence = {defence}\nPotential = {potential}\n")
    return


def create_custom_player():
    team_id = int(input("Team id:"))
    first_name = input("Name:")
    last_name = input("Surname:")
    offence = int(input("Offence:"))
    defence = int(input("Defence:"))
    age = int(input("Age:"))
    potential = int(input("Potential:"))

    cur.execute("""INSERT INTO Players
                   (Name, Surname, Age, Offence, Defence, Potential, Team)
                   VALUES
                   ('%s', '%s', '%s', %s, %s, %s, %s)"""
                   % (first_name, last_name, age, offence, defence, potential, team_id))
    conn.commit()
    print(f"{first_name} {last_name} was created successfully!")
    print(f"Age = {age}\nOffence = {offence}\nDefence = {defence}\nPotential = {potential}\n")
    return


def show_players(team_id):
    cur.execute("""SELECT * 
                   FROM Players
                   WHERE 1 = 1
                   AND Team = %s""" % (team_id))
    players = [i for i in cur.fetchall()]
    for j in players:
        print(f"{j[1]} {j[2]} (id:{j[0]}) - age: {j[3]} off: {j[4]} def: {j[5]} pot: {j[6]}")
    if len(players) > 0:
        off_avg = statistics.mean([x[4] for x in players])
        def_avg = statistics.mean([x[5] for x in players])
        pot_avg = statistics.mean([x[6] for x in players])
        print(f"Team avg = off:{round(off_avg,2)} def:{round(def_avg,2)} pot: {round(pot_avg,2)}")
    return


def show_all_teams():
    cur.execute("""SELECT id, name 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1""")
    teams = [i for i in cur.fetchall()]
    for i in teams:
        print(f"\n{i[1]} (id = {i[0]}) :")
        show_players(i[0])
    print(f"\n")
    return


def show_one_team():
    cur.execute("""SELECT id, name 
                   FROM Teams""")
    teams = [i for i in cur.fetchall()]
    for i in teams:
        print(f"{i[0]} - {i[1]}:")

    user_input = int(input("Please choose id of team you want to see players for: "))
    team_name = [i[1] for i in teams if i[0] == user_input]
    print(f"\n{team_name[0]} players:")
    show_players(user_input)
    return


def drop_player():
    show_one_team()
    drop_id = int(input("Please provide id of player that you want to drop: "))
    # Make sure that there are team "Free Agents"
    cur.execute("""SELECT count(*)
                   FROM Teams
                   WHERE id = 999""")
    free_agents = cur.fetchone()[0]
    if free_agents == 0:
        create_team("Free Agents", 9999)
    cur.execute("""UPDATE Players
                   SET Team = 999
                   WHERE id = %s""" % (drop_id))
    conn.commit()
    print(f"Player has been released to Free Agents")
    return


def trade_players(one_id, two_id):
    cur.execute("""SELECT id, Team
                   FROM Players 
                   WHERE 1 = 1
                   AND id = %s""" % (one_id))
    one_team_id = cur.fetchone()[1]

    cur.execute("""SELECT id, Team
                   FROM Players 
                   WHERE 1 = 1
                   AND id = %s""" % (two_id))
    two_team_id = cur.fetchone()[1]


    cur.execute("""UPDATE Players
                   SET Team = %s
                   WHERE id = %s""" % (two_team_id, one_id))
    conn.commit()
    cur.execute("""UPDATE Players
                   SET Team = %s
                   WHERE id = %s""" % (one_team_id, two_id))
    conn.commit()
    print(f"Trade has been successfully done!")
    return


def sign_player():
    print("Free Agents:")
    show_players(999)

    to_sign = int(input("Choose a free agent id to sign:"))
    cur.execute("""SELECT id 
                   FROM Players
                   WHERE 1 = 1
                   AND team = 999""")
    free_agents = [i[0] for i in cur.fetchall()]
    if to_sign not in free_agents:
        print("You can't sign a player who is not a free agent!")
        return

    cur.execute("""SELECT id, name 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1
                   AND id != 999""")
    teams = [i for i in cur.fetchall()]
    for i in teams:
        print(f"\n{i[0]} - {i[1]}:")
    print(f"\n")
    to_team = int(input("Choose to which team sign this player:"))

    cur.execute("""UPDATE Players
                   SET team = %s 
                   WHERE id = %s""" % (to_team, to_sign))
    conn.commit()
    return


def exit_app():
    print("\nBye!")
    conn.close()
    sys.exit()