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
        self.app_title = Label( self.root , text = "Nom de l'application" , fg = "white", bg="#595657", font = ("Arial", 30))
        self.app_title.pack(side=TOP)

        self.frame_requete = Frame( self.root, bg = "#FFFFFF" )
        self.frame_requete.pack()

        self.request_scrollbar = Scrollbar(self.frame_requete,bg="#FFFFFF")
        self.request_scrollbar.pack( side=LEFT, fill=Y )
        self.request_listbox = Listbox( self.frame_requete, fg = "black", bg="#FFFFFF", font = ("Arial", 14), width=10, height=5, yscrollcommand=self.request_scrollbar.set )
        self.request_listbox.pack( side=LEFT, fill=BOTH, padx=10, pady=10 )
