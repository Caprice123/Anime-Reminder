import sqlite3

mydb = sqlite3.connect("anime.db")

cursor = mydb.cursor()


#cursor.execute('CREATE TABLE anime (full_name text, anime_title text,episodes text, updated_time text, days integer, status integer)')


#cursor.execute("DELETE FROM anime")
#cursor.execute ("DROP TABLE anime")
cursor.execute("SELECT rowid, * FROM anime")
animes = cursor.fetchall()
for anime in animes:
    print(anime)
mydb.commit()




