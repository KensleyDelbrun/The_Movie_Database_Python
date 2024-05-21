from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
import requests
from Class_Films import Movie_Essential
from io import BytesIO
from PIL import Image, ImageTk


#La Base de données
BDD = sqlite3.connect("Films.db")
Requete = BDD.cursor()



class Fenetre_Secondaire(Toplevel):
    def __init__(self, poster_path, id, id_film, titre, genre, date_de_publication, snypnosis):
        super().__init__()
        self.title("Informations Supplémentaires")
        self.geometry("1200x500")
        self.iconbitmap("images/icon.ico")
        self.config(bg="#3C3C3C")

        # Ajout d'une variable pour suivre l'index actuel du film
        self.current_index = id

        self.Boite = Frame(self, padx=30, border=10, borderwidth=10, relief=SUNKEN)

        self.Boite_Image = Frame(self.Boite, width=250)
        # Appel de la fonction pour mettre à jour l'image avec le poster_path fourni
        self.update_image(poster_path)
        self.Boite_Image.grid(row=0, column=0, padx=30)

        self.Boite_Info = Frame(self.Boite, border=5, relief=RAISED)
        self.titre_original = Label(self.Boite_Info, text=f"Titre :  ' {titre} '", font=("helvetica", 18))
        self.titre_original.grid(row=0, column=1)
        self.genre_Label = Label(self.Boite_Info, text=f"Genre :  {genre}", font=("helvetica", 18))
        self.genre_Label.grid(row=1, column=1, pady=20)
        self.Date_de_publication_Label = Label(self.Boite_Info, text=f"Date de Publication :  {date_de_publication}", font=("helvetica", 18))
        self.Date_de_publication_Label.grid(row=2, column=1)

        self.Snypnosis_Label = Label(self.Boite_Info, text="Snypnosis : ", font=("helvetica", 18)).grid(row=3, column=1, pady=20)
        self.Snypnosis = Text(self.Boite_Info, font=("helvetica", 14), bg="black", foreground="white")
        self.Snypnosis.insert(END, f"{snypnosis}")
        self.Snypnosis.grid(row=4, column=1)
        self.Snypnosis.config(width=70, height=10)

        self.Label_Liste_Acteur = Label(self.Boite_Info, text="Liste des acteurs : ", font=("helvetica", 18))
        self.Label_Liste_Acteur.grid(row=5, column=1, pady=20)

        Requete.execute("SELECT `nom_complet`, `id` FROM `movies` JOIN `character` ON `character`.id_film_character = id_film_movies WHERE (id_film_character = ?)", (id_film,))
        self.Resultat_Acteur_id = Requete.fetchall()

        self.Liste_Acteur = ttk.Combobox(self.Boite_Info, font=("helvetica", 14))
        self.Liste_Tuple = tuple([acteur[0] for acteur in self.Resultat_Acteur_id])
        self.Liste_Acteur["values"] = self.Liste_Tuple
        self.Liste_Acteur.grid(row=6, column=1, pady=20)

        self.Boite_Info.grid(row=0, column=1)
        self.Boite.pack(pady=30)

        self.Indicateur = Label(self, text=f"{self.Resultat_Acteur_id[0][1]}/20", font=("helvetica", 18), bg="#3C3C3C", foreground="white")
        self.Indicateur.pack(pady=10)

        self.Boite_Bouton = Frame(self)
        self.Fleche_gauche = PhotoImage(file="images/gauche_d.png")
        self.Fleche_doite = PhotoImage(file="images/droite_g.png")
        self.Precedent = ttk.Button(self.Boite_Bouton, image=self.Fleche_gauche, command=self.Previous)
        self.Precedent.grid(row=0, column=0)
        self.Suivant = ttk.Button(self.Boite_Bouton, image=self.Fleche_doite, command=self.Next)
        self.Suivant.grid(row=0, column=2)
        self.Boite_Bouton.pack()
        self.Boite.pack()

        # Appel de la fonction pour mettre à jour l'état des boutons de navigation
        self.update_navigation_buttons()

    # Fonction pour mettre à jour l'image du film
    def update_image(self, poster_path):
        self.response = requests.get(f"https://image.tmdb.org/t/p/w500{poster_path}")
        self.image_data = self.response.content
        self.image = Image.open(BytesIO(self.image_data))
        self.image2 = self.image.resize((550, 600))
        self.image_tk = ImageTk.PhotoImage(self.image2)
        if hasattr(self, 'Poster'):
            self.Poster.configure(image=self.image_tk)
        else:
            self.Poster = Label(self.Boite_Image, image=self.image_tk)
            self.Poster.pack()

    # Fonction pour mettre à jour les informations du film
    def update_movie_info(self, movie):
        self.titre_original.configure(text=f"Titre :  ' {movie.original_title} '")
        self.genre_Label.configure(text=f"Genre :  {movie.genre_ids}")
        self.Date_de_publication_Label.configure(text=f"Date de Publication :  {movie.release_date}")
        self.Snypnosis.delete("1.0", END)
        self.Snypnosis.insert(END, movie.overview)
        Requete.execute("SELECT `nom_complet` FROM `movies` JOIN `character` ON `character`.id_film_character = id_film_movies WHERE (id_film_character = ?)", (movie.id_film,))
        self.Resultat_Acteur = Requete.fetchall()
        self.Liste_Acteur["values"] = tuple([acteur[0] for acteur in self.Resultat_Acteur])

    # Fonction pour mettre à jour l'état des boutons de navigation
    def update_navigation_buttons(self):
        self.Precedent.config(state=NORMAL if self.current_index > 0 else DISABLED)
        self.Suivant.config(state=NORMAL if self.current_index < 19 else DISABLED)
        self.Indicateur.config(text=f"{self.current_index + 1}/20")

    # Fonction pour aller au film suivant
    def Next(self):
        try:
            Requete.execute("SELECT `poster_path`, `id`, `id_film_movies`, `titre_original`, `genre`, `date_de_publication`, `snypnosis` FROM `movies`")
            Resultat = Requete.fetchall()
            self.current_index += 1
            movie = Resultat[self.current_index]
            self.update_image(movie[0])
            self.update_movie_info(Movie_Essential(*movie))
            self.update_navigation_buttons()
        except IndexError:
            self.current_index -= 1
            messagebox.showerror(title="Erreur", message="Vous êtes déjà au dernier film.")
        except Exception as e:
            messagebox.showerror(title="Erreur", message=f"Votre connexion internet fait défaut : {e}")


    # Fonction pour aller au film précédent
    def Previous(self):
        try:
            Requete.execute("SELECT `poster_path`, `id`, `id_film_movies`, `titre_original`, `genre`, `date_de_publication`, `snypnosis` FROM `movies`")
            Resultat = Requete.fetchall()
            self.current_index -= 1
            movie = Resultat[self.current_index]
            self.update_image(movie[0])
            self.update_movie_info(Movie_Essential(*movie))
            self.update_navigation_buttons()
        except IndexError:
            self.current_index += 1
            messagebox.showerror(title="Erreur", message="Vous êtes déjà au premier film.")
        except Exception as e:
            messagebox.showerror(title="Erreur", message=f"Votre connexion internet fait défaut : {e}")