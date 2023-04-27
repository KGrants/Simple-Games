from SQL import conn
from SQL import cur
import names
import random
import sys
import statistics


def create_player(team_id):
    full_name = names.get_full_name(gender="male").split(" ")
    offence = random.randint(50, 100)
    defence = random.randint(50, 100)
    age = random.randint(16, 32)
    potential = int(100 - random.randint(0, 50) * ((age**2)/32)/16)

    cur.execute("""INSERT INTO Players
                   (Name, Surname, Age, Offence, Defence, Potential, Team)
                   VALUES
                   ('%s', '%s', '%s', %s, %s, %s, %s)"""
                   % (full_name[0], full_name[1], age, offence, defence, potential, team_id))
    conn.commit()
    print(f"{full_name[0]} {full_name[1]} was created successfully!")
    print(f"Age = {age}\nOffence = {offence}\nDefence = {defence}\nPotential = {potential}\n")


def create_team(name, founded):
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


def check_team_count():
    cur.execute("""SELECT Count(*) 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1""")
    team_count = cur.fetchone()[0]
    if team_count != 10:
        print("You have to have 10 teams to start the season,")
        print(f"Currently there are {team_count} valid teams!")


def check_player_count():
    cur.execute("""SELECT id 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1""")
    team_count = [i for i in cur.fetchall()]
    for i in team_count:
        cur.execute("""SELECT Count(*) 
                       FROM Players
                       WHERE 1 = 1
                       AND Team = %s""" % (i))
        player_count = cur.fetchone()[0]
        if player_count != 5:
            cur.execute("""SELECT name 
                       FROM Teams
                       WHERE 1 = 1
                       AND id = %s""" %(i))
            team_name = cur.fetchone()[0]
            print(team_name,f"currently has {player_count} players.")
            print("To start the season it needs to have 5 players.")


def show_all_teams():
    cur.execute("""SELECT id, name 
                   FROM Teams
                   WHERE 1 = 1
                   AND valid = 1""")
    teams = [i for i in cur.fetchall()]
    for i in teams:
        print(f"\n{i[1]}:")
        show_players(i[0])
    print(f"\n")

def show_one_team():
    cur.execute("""SELECT id, name 
                   FROM Teams""")
    teams = [i for i in cur.fetchall()]
    for i in teams:
        print(f"\n{i[0]} - {i[1]}:")

    user_input = int(input("Please choose one team : "))
    cur.execute("""SELECT id, name 
                   FROM Teams
                   WHERE id = %s""" % (user_input))
    team_name = cur.fetchone()[1]
    print(f"{team_name} players:")
    show_players(user_input)


def show_players(team_id):
    cur.execute("""SELECT * 
                   FROM Players
                   WHERE 1 = 1
                   AND Team = %s""" % (team_id))
    players = [i for i in cur.fetchall()]
    for j in players:
        print(f"{j[1]} {j[2]} (id:{j[0]}) - age: {j[3]} off: {j[4]} def: {j[5]} pot: {j[6]}")
    off_avg = statistics.mean([x[4] for x in players])
    def_avg = statistics.mean([x[5] for x in players])
    pot_avg = statistics.mean([x[6] for x in players])
    print(f"Team avg = off:{round(off_avg,2)} def:{round(def_avg,2)} pot: {round(pot_avg,2)}\n")


def first_screen():
    print("Welcome to Sunday League NBA:")
    options = ["1. Create a Team", 
               "2. Create a Player", 
               "3. Start the Season", 
               "4. Show all Teams", 
               "5. Show one team", 
               "6. Drop Player from team",
               "7. Exit"]
    print("", *options, sep="\n")  # Print menu
    return int(input(">").strip())  # Get user input


def exit_app():
    print("\nBye!")
    conn.close()
    sys.exit()


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