import mysql.connector
import os
from dotenv import find_dotenv, load_dotenv 
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)
envuser = os.getenv("user")
envpassword = os.getenv("password")
envhost = os.getenv("host")

mydb = mysql.connector.connect(
    host = envhost,
    user = envuser,
    password = envpassword,
    database = "musikk"
)

mycursor = mydb.cursor()




mycursor.execute("""
CREATE TABLE IF NOT EXISTS artist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    navn VARCHAR(100) NOT NULL
)
""")

mycursor.execute("""
CREATE TABLE IF NOT EXISTS sang (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tittel VARCHAR(100) NOT NULL,
    artist_id INT,
    FOREIGN KEY (artist_id) REFERENCES artist(id)
)
""")

mydb.commit()





def legg_til_artist():
    navn = input("Skriv inn artistnavn: ")
    mycursor.execute("INSERT INTO artist (navn) VALUES (%s)", (navn,))
    mydb.commit()
    print("Artist lagt til!\n")



def legg_til_sang():
    tittel = input("Skriv inn sangtittel: ")
    artist_id = input("Skriv inn artist ID: ")
    mycursor.execute("INSERT INTO sang (tittel, artist_id) VALUES (%s, %s)", (tittel, artist_id))
    mydb.commit()
    print("Sang lagt til!\n")



def vis_artister():
    mycursor.execute("SELECT * FROM artist")
    result = mycursor.fetchall()
    print("\n--- ARTISTER ---")
    for x in result:
        print(f"{x[0]}: {x[1]}")
    print("")



def vis_sanger():
    mycursor.execute("""
    SELECT s.id, s.tittel, a.navn 
    FROM sang s 
    JOIN artist a ON s.artist_id = a.id
    """)
    result = mycursor.fetchall()
    print("\n--- SANGER ---")
    for x in result:
        print(f"{x[0]}: {x[1]} ({x[2]})")
    print("")



def oppdater_artist():
    artist_id = input("Skriv ID til artisten du vil endre: ")
    nytt_navn = input("Skriv nytt navn: ")
    mycursor.execute("UPDATE artist SET navn=%s WHERE id=%s", (nytt_navn, artist_id))
    mydb.commit()
    print("Artist oppdatert!\n")



def oppdater_sang():
    sang_id = input("Skriv ID til sangen du vil endre: ")
    ny_tittel = input("Skriv ny tittel: ")
    mycursor.execute("UPDATE sang SET tittel=%s WHERE id=%s", (ny_tittel, sang_id))
    mydb.commit()
    print("Sang oppdatert!\n")





while True:
    print("""
----- MUSIKKREGISTER -----
1. Legg til artist
2. Legg til sang
3. Vis artister
4. Vis sanger
5. Oppdater artist
6. Oppdater sang
7. Avslutt
""")

    valg = input("Velg et tall 1-7: ")

    if valg == "1":
        legg_til_artist()
    elif valg == "2":
        legg_til_sang()
    elif valg == "3":
        vis_artister()
    elif valg == "4":
        vis_sanger()
    elif valg == "5":
        oppdater_artist()
    elif valg == "6":
        oppdater_sang()
    elif valg == "7":
        print("Programmet avsluttes...")
        break
    else:
        print("Feil valg, prøv igjen!\n")

mydb.close()

