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
    place = 1
    for i in cur.fetchall():
        print(f"{place}. {i[1]} {i[2]} ({i[3]}) = {i[4]} pts")
        place += 1
    return


def mvp():
    # to implement
    return