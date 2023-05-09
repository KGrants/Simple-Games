from SQL import cur
from SQL import conn
import sql_queries as sqlq
import pandas as pd

def show_standings(year):
    print("\nCurrent league standings:")
    sqlq.team_stand_sql(year)
    place = 1
    for i in cur.fetchall():
        print(f"{place}. {i[0]} = {i[1]} pts ({i[2]} +/-)")
        place += 1
    return


def show_top_scorers(year):
    print("\nTop Scorers:")
    sqlq.top_scorers_sql(year)
    df = pd.DataFrame(cur.fetchall(), columns = ['id', 'Name', 'Surname', 'Team', 'Points', 'RowNum'])
    df.index = [i for i in range(1,6)]
    print(df[['Name', 'Surname', 'Team', 'Points']])
    return


def mvp(year):
    mvp_winner = ("",0,0)
    winner_teams = sqlq.mvp_query()
    sqlq.top_scorers_sql(year)

    for i in cur.fetchall():
        if i[3] == winner_teams[0] and i[4]*1.2>mvp_winner[1]:
            mvp_winner = (f"{i[1]} {i[2]}", int(i[4]*1.2), int(i[0]))

        elif i[3] == winner_teams[1] and i[4]*1.15>mvp_winner[1]:
            mvp_winner = (f"{i[1]} {i[2]}", int(i[4]*1.15), int(i[0]))

        elif i[3] == winner_teams[2] and i[4]*1.1>mvp_winner[1]:
            mvp_winner = (f"{i[1]} {i[2]}", int(i[4]*1.1), int(i[0]))

        elif i[4]>mvp_winner[1]:
                mvp_winner = (f"{i[1]} {i[2]}", int(i[4]), int(i[0]))

    return mvp_winner
