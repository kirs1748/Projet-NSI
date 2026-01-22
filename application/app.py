from tkinter import *
from api import ApiClient


class App :

    def __init__(self, root):
        self.root = root
        self.root.title("Nom de l'application")
        self.root.state('zoomed')

        # Backend
        self.api = ApiClient()

        # Données de l'application
        self.response_text = None
        self.status_code = None

        # Interface
        self.build_ui()

    def build_ui(self):
        # Configuration de la grille générale
        self.root.grid_rowconfigure(0, weight=0)  # header
        self.root.grid_rowconfigure(1, weight=0)  # requete
        self.root.grid_rowconfigure(2, weight=0)  # paramètres
        self.root.grid_rowconfigure(3, weight=0)  # réponse
        self.root.grid_columnconfigure(0, weight=1)

        # Frame pour l'en-tête
        self.header_frame = Frame( self.root, bg = "#FFFFFF" )
        self.header_frame.grid(row=0, column=0, sticky="nsew")
        self.menubar = Menu( self.header_frame )
        self.menubar.add_command( label = "Automatisation", command= lambda: print("Automatisation clicked"))
        self.root.config( menu = self.menubar )
        self.app_title = Label( self.header_frame , text = "Nom de l'application" , fg = "black", bg="#FFFFFF", font = ("Impact", 30))
        self.app_title.pack( side=TOP, padx=20, pady=20 )

        # Frame pour les requêtes
        self.frame_requete = Frame( self.root, bg = "#00FF22", pady=10 )
        self.frame_requete.grid(row=1, column=0, sticky="nsew")
        #Configuration de la grille de la frame requête
        self.frame_requete.grid_columnconfigure(0, weight=1)
        self.frame_requete.grid_columnconfigure(1, weight=1)
        self.frame_requete.grid_columnconfigure(2, weight=1)

        # Choix de la requête
        self.choix_requete = StringVar(value="GET")
        self.request_menu = OptionMenu( self.frame_requete , self.choix_requete , "GET" , "POST" , "PUT" , "DELETE" )
        self.request_menu.grid(row=0, column=0, padx=3, pady=10, sticky="e")
        # Champ d'entrée pour l'URL
        self.url_entry = Entry( self.frame_requete , fg = "black", bg="#B13636", font = ("Arial", 20), width=40 )
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        # Bouton pour envoyer la requête
        self.send_button = Button(self.frame_requete , text = "send" , fg = "black", bg="#D3D3D3", font = ("Arial", 20), command=lambda: self.send_request())
        self.send_button.grid(row=0, column=2, padx=10, pady=10,sticky="w")


        #Frame pour les paramètres
        self.frame_params = Frame( self.root, bg = "#FF00D9" )
        self.frame_params.grid(row=2, column=0, sticky="nsew")

        params_label = Label( self.frame_params , text = "Parameters:" , fg = "black", bg="#005EFF", font = ("Arial", 20))
        params_label.pack(side=TOP, padx=10, pady=10 )



        #Frame pour la réponse
        self.frame_reponse = Frame( self.root, bg = "#7C6363" )
        self.frame_reponse.grid(row=3, column=0, sticky="nsew")


        response_label = Label( self.frame_reponse , text = "Response:" , fg = "black", bg="#FFFFFF", font = ("Arial", 20))
        response_label.pack( side=TOP, padx=10, pady=10 )
        self.response_text = Message( self.frame_reponse , text = "" , fg = "black", bg="#FFFFFF", font = ("Arial", 14), width=1000 )
        self.response_text.pack( side=TOP, padx=10, pady=10 )



    def send_request(self):
        method = self.choix_requete.get()
        if method == "GET":
            self.send_get_request()
        elif method == "POST":
            self.send_post_request()
        elif method == "PUT":
            self.send_put_request()
        elif method == "DELETE":
            self.send_delete_request()
        

    def send_get_request(self):
        url = self.url_entry.get()
        print("metode GET")
        status_code, response_content , response_headers, response_cookies = self.api.get(url)
        print(f"Status Code: {status_code}")
        #print(f"Response Text: {response_content}")
        print(f"Response Headers: {response_headers}")
        #print(f"Response JSON: {response_json}")
        #print(f"Response Cookies: {response_cookies}")


    def send_post_request(self):
        print("metode POST")

    def send_put_request(self):
        print("metode PUT")

    def send_delete_request(self):
        print("metode DELETE")