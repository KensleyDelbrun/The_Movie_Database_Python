#Fomatage de toutes les informations, sans distinction
class Movie:
    def __init__(self, id, orginal_title, genre_ids, orginal_language, release_date, overview, title, video, adult, backdrop_path, poster_path, popularity, vote_average, vote_count):
        self.id = id
        self.original_title = orginal_title
        Type_Movies = {
                        28:"Action", 
                        12 : "Aventure", 
                        16:"Animation", 
                        35:"Comédie", 
                        80 : "Crime",
                        99 : "Documentaire",
                        18 : "Drame",
                        10751 : "Famille",
                        36 : "Histoire",
                        27 : "Horreur",
                        10402 : "Musique",
                        9648 : "Mystère",
                        10749: "Romantique",
                        878 : "Science fiction",
                        10770 : "TV et Films",
                        10752 : "Guerre",
                        37 : "Occidental",
                        53 : "Thriller",
                        }
        Genre_Film = [Type_Movies[number_code] for number_code in Type_Movies.keys() if number_code in genre_ids]
        self.genre_ids = ", ".join(Genre_Film)
        self.original_language = orginal_language
        self.release_date = release_date
        if overview == "":
            self.overview = "Aucune déscription"
        else:
            self.overview = overview
        self.title = title
        if video:
            self.video = "Vidéo disponoible"
        else:
            self.video = "Vidéo non disponible"
        
        if adult:
            self.adult = "Interdit aux enfants"
        else:
            self.adult = "Accésible à tous les tranches d'âge"
        self.backdrop_path = backdrop_path
        self.poster_path = poster_path
        self.popularity = popularity
        self.vote_average = vote_average
        self.vote_count = vote_count


#Formatage des informations éssentielles
class Movie_Essential:
    def __init__(self, poster_path, id, id_film, orginal_title, genre, release_date, overview):
        self.poster_path = poster_path
        self.id = id
        self.id_film = id_film
        self.original_title = orginal_title
        self.genre_ids = genre
        self.release_date = release_date
        self.overview = overview