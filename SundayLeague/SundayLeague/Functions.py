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
    potential = random.randint(50, 100)
    cur.execute("""INSERT INTO Players
                   (Name, Surname, Offence, Defence, Potential, Team)
                   VALUES
                   ('%s', '%s', %s, %s, %s, %s)"""
                   % (full_name[0], full_name[1], offence, defence, potential, team_id))
    conn.commit()
    print(f"{full_name[0]} {full_name[1]} was created successfully!")
    print(f"Offence = {offence}\nDefence = {defence}\nPotential = {potential}\n")


def create_team(name, founded):
    cur.execute("""INSERT INTO Teams (Name, Founded)
                   VALUES ('%s', %s);"""
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
        print(f"\n{i[1]}")
        cur.execute("""SELECT * 
                       FROM Players
                       WHERE 1 = 1
                       AND Team = %s""" % (i[0]))
        players = [i for i in cur.fetchall()]
        for j in players:
            print(f"{j[1]} {j[2]} - off: {j[3]} def: {j[4]} pot: {j[5]}")
        off_avg = statistics.mean([x[3] for x in players])
        def_avg = statistics.mean([x[4] for x in players])
        pot_avg = statistics.mean([x[5] for x in players])
        print(f"Team avg = off:{round(off_avg,2)} def:{round(def_avg,2)} pot: {round(pot_avg,2)}")
    print(f"\n")



def first_screen():
    print("Welcome to Sunday League NBA:")
    options = ["1. Create a Team", "2. Create a Player", "3. Start the Season", "4. Show all Teams", "5. Exit"]
    print("", *options, sep="\n")  # Print menu
    return int(input(">").strip())  # Get user input


def exit_app():
    print("\nBye!")
    conn.close()
    sys.exit()