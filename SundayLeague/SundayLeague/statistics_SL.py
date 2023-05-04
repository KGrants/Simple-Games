from SQL import cur

def show_standings():
    print("\nCurrent league standings:")
    cur.execute("""SELECT T.Name, COUNT(G.id)*3
                   FROM Teams T
                   LEFT JOIN Games G ON G.Winner = T.id
                   GROUP BY T.Name
                   ORDER BY 2 DESC""")
    place = 1
    for i in cur.fetchall():
        print(f"{place}. {i[0]} = {i[1]} pts")
        place += 1
    return

def show_top_scorers():
    print("\nTop Scorers:")
    top_scorers_sql()
    place = 1
    for i in cur.fetchall():
        print(f"{place}. {i[1]} {i[2]} ({i[3]}) = {i[4]} pts")
        place += 1
    return


def mvp():
    cur.execute("""SELECT T.Name, COUNT(G.id)*3
                   FROM Teams T
                   LEFT JOIN Games G ON G.Winner = T.id
                   GROUP BY T.Name
                   ORDER BY 2 DESC
                   LIMIT 3""")
    winner_teams = [i[0] for i in cur.fetchall()]
    top_scorers_sql()
    mvp_winner = ("",0)
    for i in cur.fetchall():
        if i[3] == winner_teams[0]:
            if i[4]*1.2>mvp_winner[1]:
                mvp_winner = (f"{i[1]} {i[2]}", int(i[4]*1.2))
        elif i[3] == winner_teams[1]:
            if i[4]*1.15>mvp_winner[1]:
                mvp_winner = (f"{i[1]} {i[2]}", int(i[4]*1.15))
        elif i[3] == winner_teams[2]:
            if i[4]*1.1>mvp_winner[1]:
                mvp_winner = (f"{i[1]} {i[2]}", int(i[4]*1.1))
        else:
            if i[4]>mvp_winner[1]:
                mvp_winner = (f"{i[1]} {i[2]}", int(i[4]))

    print(f"{mvp_winner[0]}")

    return

def top_scorers_sql():
    cur.execute("""WITH HighScorers AS
                   (
                   SELECT 
                   P.id, 
                   P.Name, 
                   P.Surname, 
                   T.Name,
                   SUM(PS.Points) OVER(PARTITION BY P.id) AS TotalPoints,
                   ROW_NUMBER() OVER(PARTITION BY P.id) as RowNum
                   FROM Players P
                   LEFT JOIN Player_Score PS ON PS.Player_id = P.id
                   LEFT JOIN Teams T ON T.id = P.Team
                   ORDER BY 5 DESC
                   )
                   SELECT * 
                   FROM HighScorers
                   WHERE RowNum = 1
                   LIMIT 5
                   """)
    return