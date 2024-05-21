#Les modules utilisés
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from Class_Films import Movie, Movie_Essential
from Interface2 import Fenetre_Secondaire
import requests
import sqlite3
import json


#La Base de données
BDD = sqlite3.connect("Films.db")
Requete = BDD.cursor()

#Table films
Requete.execute("""
                CREATE TABLE IF NOT EXISTS `movies`( 
                        `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `id_film_movies` INTEGER, 
                        `titre_original` TEXT, 
                        `genre` TEXT, 
                        `langue_originale` TEXT, 
                        `date_de_publication` TEXT, 
                        `snypnosis` TEXT,
                        `titre` TEXT, 
                        `video` TEXT, 
                        `adulte` TEXT, 
                        `backdrop_path` TEXT, 
                        `poster_path` TEXT, 
                        `popularite` FLOAT,
                        `vote_moyenne` FLOAT, 
                        `nombre_vote` FLOAT)
                    	                    """)

#Table acteurs
Requete.execute("""
                CREATE TABLE IF NOT EXISTS`character`( 
                        `id_film_character` INTEGER, 
                        `nom_complet` TEXT 
                         )
                """)


class Fenetre_Principale(Tk):
    def __init__(self):
        super().__init__()
        self.title("The_Movie_Database")
        self.iconbitmap("images/icon.ico")
        self.geometry("1200x500")
        self.config(bg="#3C3C3C")

        self.Encadrement = Frame(self)
        self.Remplissage_Table_film()
        self.Remplissage_Table_Acteur()
        self.Titre = Label(self.Encadrement, text="Most_Popular Movies_", font=("Arial bold", 24)).pack()
        
        #Style pour l'en-tête et le corps de notre treeview
        self.style = ttk.Style()
        self.style.theme_use("winnative")
        self.style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=35,
                font=("Helvetica", 17),
                fieldbackground="black")
        
        self.style.configure("Treeview.Heading",
                background="lightblue",
                foreground="black",
                font=("Helvetica", 16, "bold"))
        
        self.style.map("Treeview",
          background=[("selected", "blue")],
          foreground=[("selected", "white")])


        self.Boite_tableau = Frame(self.Encadrement, width=60, padx=5)
        self.Tableau = ttk.Treeview(self.Boite_tableau, columns=("ID_Film","Titre","Date de publication",),show="headings")
        self.Tableau.heading("ID_Film",text="ID_Film")
        self.Tableau.heading("Titre",text="Titre")
        self.Tableau.heading("Date de publication",text="Date de publication")
        self.Tableau.config(height=20)
        self.Tableau.pack()
        self.Boite_tableau.pack()
        
        self.Tableau.column("ID_Film", width=300, anchor="center")
        self.Tableau.column("Titre", width=500, anchor="center")
        self.Tableau.column("Date de publication", width=300, anchor="center")
        
        self.Encadrement.pack(expand=YES)

        # self.Titre = Label()

        self.Filling_Treeview()
        self.Tableau.bind("<<TreeviewSelect>>", self.Selection)
        messagebox.showinfo(title="Présentation", message="Vous avez devant vous une liste succinte de 20 films parmi les films les plus populaires de cette semaine. Pour en savoir sur eux, veuillez les sélectionnés l'un après l'autre. \n\n NB: Pour une utilisation optimale il va vous falloir une bonne connexion internet.")


    Position = 0
    def Filling_Treeview(self):
        Requete.execute("SELECT `id_film_movies`, `titre_original`, `date_de_publication` FROM `movies`")
        for Film in Requete:
            self.Tableau.insert(parent = "",index = Fenetre_Principale.Position,values=(Film[0], Film[1], Film[2]))
            Fenetre_Principale.Position += 1

    
    def Remplissage_Table_film(self):
        try:
            Requete.execute("SELECT COUNT(*) FROM `movies`")
            Nombre_Occurence = Requete.fetchall()
            if Nombre_Occurence[0][0] == 0:
                url = "https://api.themoviedb.org/3/movie/popular?language=fr-US&page=1"

                headers = {
                    "accept": "application/json",
                     "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYjVmNjg0YzZjNjZhNjg0NzAyYmE0YTk2ZGYxZDUxYiIsInN1YiI6IjY2MzdiNjcyOTRkOGE4MDEyMzMzMjNjNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1B30wJuFHGC4eo2Picus3imkS-EpRxeMx0qbbsqukdE"
                        }

                response = requests.get(url, headers=headers)
                Donnee = response.text
                Data = json.loads(Donnee)["results"]

                for i in  range(len(Data)):
                    instruction = "INSERT INTO `movies` (`id_film_movies`, `titre_original`, `genre`, `langue_originale`, `date_de_publication`, `snypnosis`, `titre`, `video`, `adulte`, `backdrop_path`, `poster_path`, `popularite`, `vote_moyenne`, `nombre_vote`) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                    id = Data[i]["id"]
                    genre_ids = Data[i]["genre_ids"]
                    original_language = Data[i]["original_language"]
                    original_title = Data[i]["original_title"]
                    overview = Data[i]["overview"]
                    release_date = Data[i]["release_date"]
                    title = Data[i]["title"]
                    video = Data[i]["video"]
                    adult = Data[i]["adult"]
                    popularity = Data[i]["popularity"]
                    poster_path = Data[i]["poster_path"]
                    vote_average = Data[i]["vote_average"]
                    vote_count = Data[i]["vote_count"]
                    backdrop_path = Data[i]["backdrop_path"]

                    Film = Movie(id, original_title, genre_ids, original_language, release_date, overview, title, video, adult, backdrop_path, poster_path, popularity,vote_average, vote_count)
                    print(Film)
                    Valeur = (Film.id, Film.original_title, Film.genre_ids, Film.original_language, Film.release_date, Film.overview, Film.title, Film.video, Film.adult, Film.backdrop_path, Film.poster_path, Film.popularity, Film.vote_average, Film.vote_count)
                    print(Valeur)
                    Requete.execute(instruction, Valeur)
                
                    BDD.commit()
        except:
            messagebox.showerror(title="Erreur", message="Votre connexion internet fait défaut")
        

    def Remplissage_Table_Acteur(self):
        try:
            Requete.execute("SELECT COUNT(*) FROM `character`")
            Nombre_Occurence = Requete.fetchone()
            if Nombre_Occurence[0] == 0:
                Requete.execute("SELECT `id_film_movies` FROM `movies`")
                id_Acteur = Requete.fetchall()

                for id in id_Acteur:
                    url_api_acteur = f"https://api.themoviedb.org/3/movie/{id[0]}/credits?language=en-US"

                    headers = {
                         "accept": "application/json",
                    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYjVmNjg0YzZjNjZhNjg0NzAyYmE0YTk2ZGYxZDUxYiIsInN1YiI6IjY2MzdiNjcyOTRkOGE4MDEyMzMzMjNjNCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.1B30wJuFHGC4eo2Picus3imkS-EpRxeMx0qbbsqukdE"
                        }

                    response = requests.get(url_api_acteur, headers=headers)
                    Donnee = response.text
                    Data = json.loads(Donnee)["cast"]

                    for nombre_acteur in range(len(Data)):
                        Requete.execute("INSERT INTO `character` (`id_film_character`, `nom_complet`) VALUES (?, ?)", (id[0], 
                        Data[nombre_acteur]["name"]))
                        BDD.commit()
        except:
            messagebox.showinfo(title="Erreur",message="Votre connexion internet fait défaut")

        
    def Selection(self, event):
        try:
            Enregistrement_Ciblee = self.Tableau.selection()
            Donnees = self.Tableau.item(Enregistrement_Ciblee, 'values')
            Instruction = "SELECT `poster_path`, `id`, `id_film_movies`, `titre`, `genre`, `date_de_publication`, `snypnosis` FROM `movies` WHERE `id_film_movies` = ?"
            Valeurs = (Donnees[0], )
            Requete.execute(Instruction, Valeurs)
            self.g = Requete.fetchone()
            Fenetre_Secondaire(self.g[0], self.g[1], self.g[2], self.g[3], self.g[4], self.g[5], self.g[6])
        except:
            messagebox.showerror(title="Erreur", message="Votre connexion internet fait défaut")