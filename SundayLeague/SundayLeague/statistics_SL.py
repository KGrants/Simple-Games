from SQL import cur
import sql_queries as sqlq
import pandas as pd

def show_standings(year):
    print("\nCurrent league standings:")
    sqlq.team_stand_sql(year)
    df = pd.DataFrame(cur.fetchall(), columns = ['Id', 'Team', 'Points', '+/-'])
    df.index = [i for i in range(1,df.shape[0]+1)]
    print(df[['Team', 'Points', '+/-']])
    return


def show_top_scorers(year):
    print("\nTop Scorers:")
    sqlq.top_scorers_sql(year)
    df = pd.DataFrame(cur.fetchall(), columns = ['id', 'Name', 'Surname', 'Team', 'Points', 'RowNum'])
    df.index = [i for i in range(1,df.shape[0]+1)]
    print(df[['Name', 'Surname', 'Team', 'Points']])
    return


def mvp(year):
    mvp_winner = ("",0,0)
    sqlq.team_stand_sql(year)
    winner_teams = [i[1] for i in cur.fetchmany(3)]

    sqlq.top_scorers_sql(year)
    high_scorers = cur.fetchall()
    
    for i in high_scorers:
        if i[3] in winner_teams:
            if i[4]*(1.2-0.05*winner_teams.index(i[3]))>mvp_winner[1]:
                mvp_winner = (f"{i[1]} {i[2]}", int(i[4]*(1.2-0.05*winner_teams.index(i[3]))), int(i[0]))
        elif i[4]>mvp_winner[1]:
                mvp_winner = (f"{i[1]} {i[2]}", int(i[4]), int(i[0]))
    
    print("\nRegular Season MVP:")
    print(mvp_winner[0])
    return mvp_winner

def mip(year):
    print(f"\n{year} Most Improved Player:")
    sqlq.most_improved_sql(year)
    print(cur.fetchone()[1])
    return


#This function prints out the draft order for a given year. It takes in the year as an argument and uses an SQL query to retrieve the data from the database. The data
# is then stored in a pandas DataFrame and the relevant columns are printed out. The index of the DataFrame is set to the range of 1 to 11 to represent the draft order
#. The function then returns the DataFrame.
def show_draft_order(year):
    print("\nDraft Order:")
    sqlq.draft_order_sql(year)
    df = pd.DataFrame(cur.fetchall(), columns = ['Id', 'Team', 'Points', '+/-'])
    df.index = [i for i in range(1,11)]
    print(df[['Team', 'Points', '+/-']])
    return df