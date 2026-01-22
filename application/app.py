from tkinter import *
from api import ApiClient


class App :

    def __init__(self, root):
        self.root = root
        self.root.title("Nom de l'application")

        # Backend
        self.api = ApiClient()

        # Données de l'application
        self.response_text = None
        self.status_code = None

        # Interface
        self.build_ui()

    def build_ui(self):
        # Titre de l'application
        self.app_title = Label( self.root , text = "Nom de l'application" , fg = "white", bg="#595657", font = ("Arial", 30))
        self.app_title.pack(side=TOP)

        # Frame pour les requêtes
        self.frame_requete = Frame( self.root, bg = "#FFFFFF" )
        self.frame_requete.pack()

        # Choix de la requête
        self.request_scrollbar = Scrollbar(self.frame_requete,bg="#FFFFFF")
        self.request_scrollbar.pack( side=LEFT, fill=Y )
        self.request_listbox = Listbox( self.frame_requete, fg = "black", bg="#FFFFFF", font = ("Arial", 14), width=10, height=5, yscrollcommand=self.request_scrollbar.set )
        self.request_listbox.pack( side=LEFT, fill=BOTH, padx=10, pady=10 )
        self.request_listbox.insert(END, "GET")
        self.request_listbox.insert(END, "POST")
        self.request_listbox.insert(END, "PUT")
        self.request_listbox.insert(END, "DELETE")


        # Champ d'entrée pour l'URL
        self.url_entry = Entry( self.frame_requete , fg = "black", bg="#B13636", font = ("Arial", 20), width=40 )
        self.url_entry.pack( side=LEFT, padx=10, pady=10 )

        self.send_button = Button(self.frame_requete , text = "send" , fg = "black", bg="#D3D3D3", font = ("Arial", 20), command=lambda: self.send_request())
        self.send_button.pack( side=LEFT, padx=10, pady=10 )



    def send_request(self):
        method = self.request_listbox.get(ACTIVE)
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
        status_code, response_text = self.api.get(url)
        print(f"Status Code: {status_code}")

    def send_post_request(self):
        print("metode POST")

    def send_put_request(self):
        print("metode PUT")

    def send_delete_request(self):
        print("metode DELETE")