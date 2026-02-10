from tkinter import *
from tkinter import messagebox
#from tkinter import scrolledtext
from tkinter import ttk
from api import ApiClient
from fonctions import *
import os


class App :

    def __init__(self, root):
        self.root = root
        self.root.title("Nom de l'application")
        self.root.state('zoomed')

        # Backend
        self.api = ApiClient()

        self.style = ttk.Style(self.root)
        #importer un thème
        theme_path = os.path.join(os.path.dirname(__file__), "black.tcl")
        root.tk.call("source", theme_path)
        self.style.theme_use('vista')
        #self.style.configure('TButton', font=('Arial', 12), padding=6)





        self.current_param_type = "query"
        # Stockage des paramètres de la requête
        self.params = {
            "query": {},    # params=...
            "headers": {},  # headers=...
            "body": {}      # data=... ou json=...
        }


         # Données de l'application
        self.response_text = ""
        self.status_code = ""
        

        # Stockage des différentes parties de la réponse à la requête
        self.response_data = {
            "html": "",
            "headers": "",
            "cookies": ""
        }

        # Interface
        self.build_ui()











    def build_ui(self):
        # Configuration de la grille générale
        self.root.grid_rowconfigure(0, weight=0)  # header
        self.root.grid_rowconfigure(1, weight=0)  # requete
        self.root.grid_rowconfigure(2, weight=1)  # paramètres
        self.root.grid_rowconfigure(3, weight=0)  # réponse
        self.root.grid_columnconfigure(0, weight=1)

        # Frame pour l'en-tête
        self.header_frame = Frame( self.root, bg = "#909090" )
        self.header_frame.grid(row=0, column=0, sticky="nsew")
        self.menubar = Menu( self.header_frame )
        self.menubar.add_command( label = "Requetes", command= lambda: print("Requete clicked"))
        self.menubar.add_command( label = "Automatisation", command= lambda: self.open_automatisation_window() )
        self.root.config( menu = self.menubar )
        self.app_title = Label( self.header_frame , text = "Nom de l'application" , fg = "black", bg="#909090", font = ("Impact", 30))
        self.app_title.pack( side=TOP, padx=20, pady=20 )

        # Frame pour les requêtes
        self.frame_requete = Frame( self.root, bg = "#909090", pady=10 )
        self.frame_requete.grid(row=1, column=0, sticky="nsew")
        #Configuration de la grille de la frame requête
        self.frame_requete.grid_columnconfigure(0, weight=1)
        self.frame_requete.grid_columnconfigure(1, weight=1)
        self.frame_requete.grid_columnconfigure(2, weight=1)

        # Choix de la requête
        self.choix_requete = StringVar(value="GET")
        self.option_menu = ttk.OptionMenu( self.frame_requete , self.choix_requete , "GET" ,"GET", "POST" , "PUT" , "DELETE" )
        self.option_menu.grid(row=0, column=0, padx=3, pady=10, sticky="e")
        # Champ d'entrée pour l'URL

        #self.url_entry_var = StringVar()
        #self.url_entry_var.set("https://api.example.com/resource")
        self.url_entry = Entry( self.frame_requete , fg = "black", bg="#FFFFFF", font = ("Arial", 20), width=40)
        self.url_entry.grid(row=0, column=1, padx=10, pady=10)
        # Bouton pour envoyer la requête
        self.send_button = ttk.Button(self.frame_requete , text = "send",style="TButton",  command=lambda: self.send_request())
        self.send_button.grid(row=0, column=2, padx=10, pady=10,sticky="w")






        #Frame pour les paramètres
        self.frame_params = Frame( self.root, bg = "#909090" )
        self.frame_params.grid(row=2, column=0, sticky="nsew")

        self.frame_params.grid_rowconfigure(1, weight=1)
        self.frame_params.grid_columnconfigure(0, weight=1)

        params_label = Label( self.frame_params , text = "Parameters:" , fg = "black", bg="#909090", font = ("Arial", 20))
        params_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")


        self.choix_param = StringVar(value="Query")
        self.menu_param = ttk.OptionMenu( self.frame_params , self.choix_param , "Query" ,"Query", "Body" , "Headers", command=lambda value: self.change_param_type(value) )
        self.menu_param.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        self.params_table = ScrollableKeyValueFrame(self.frame_params, height=220)
        self.params_table.grid(row=1, column=0, sticky="nsew", padx=10)

        ttk.Button(self.frame_params, text="Ajouter un paramètre",command=self.params_table.add_row).grid(row=2, column=0, pady=5)
        #Frame pour la réponse
        self.frame_reponse = Frame( self.root, bg = "#909090", borderwidth=5, relief="groove" )
        self.frame_reponse.grid(row=3, column=0, sticky="sew")
        self.response_label = Label( self.frame_reponse , text = f"Response: {self.status_code}" , fg = "black", bg="#FFFFFF", font = ("Arial", 20))
        self.response_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")





        # Configuration de la grille de la frame réponse
        self.frame_reponse.grid_rowconfigure(0, weight=0)
        self.frame_reponse.grid_rowconfigure(1, weight=1)
        self.frame_reponse.grid_rowconfigure(2, weight=1)
        self.frame_reponse.grid_columnconfigure(0, weight=1)
        self.frame_reponse.grid_columnconfigure(1, weight=1)
        self.frame_reponse.grid_columnconfigure(2, weight=1)


        # Menu pour choisir l'affichage de la réponse
        self.view_mode = StringVar(value="HTML")
        self.view_menu = ttk.OptionMenu( self.frame_reponse , self.view_mode , "HTML" ,"HTML", "Headers" , "Cookies" , command=self.update_response_view )
        self.view_menu.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.response_text = Text( self.frame_reponse , fg = "black", bg="#C0C0C0", font = ("Arial", 12), height=8)
        self.response_text.grid(row=0, column=1, columnspan=2,rowspan=2,  padx=10, pady=10, sticky="nsew")

    




    def change_param_type(self , value):

        new_type = value.lower()

        # 1️⃣ Sauvegarder l'ancien
        self.params[self.current_param_type] = self.params_table.get_data()

        # 2️⃣ Changer le type courant
        self.current_param_type = new_type

        # 3️⃣ Charger le nouveau
        self.params_table.load_data(self.params[new_type])
    
    
    def prepare_request_data(self):
        """
        Prépare les données à envoyer à l'API
        en fonction des paramètres saisis
        """
        return {
            "query": self.params["query"],
            "headers": self.params["headers"],
            "body": self.params["body"]
        }
    




    
    # Gestion des requêtes
    def send_request(self):
        self.params[self.current_param_type] = self.params_table.get_data()
        method = self.choix_requete.get()
        url = self.url_entry.get()
        data = self.prepare_request_data()
        if method == "GET":
            self.send_get_request(url, data)
        elif method == "POST":
            self.send_post_request(url, data)
        elif method == "PUT":
            self.send_put_request(url, data)
        elif method == "DELETE":
            self.send_delete_request(url, data)
        


    # Gestion des requêtes GET
    def send_get_request(self, url, data=None):

        status_code, response_content , response_headers, response_cookies = self.api.get(url, params=data["query"], headers=data["headers"])
        response_content = parse_html( response_content )
        

        self.response_data["html"] = response_content
        self.response_data["headers"] = "\n".join(f"{k}: {v}" for k, v in response_headers.items())
        self.response_data["cookies"] = "\n".join(f"{k}: {v}" for k, v in response_cookies.items())
        self.response_data["status"] = status_code
        self.update_response_view(self.view_mode.get())








    # Gestion des requêtes POST
    def send_post_request(self, url, data=None):
        status_code, response_content , response_headers, response_cookies, longueur = self.api.post(url, params=data["query"], headers=data["headers"], query=data["body"])

        self.response_data["status"] = status_code
        self.response_data["html"] = response_content
        self.response_data["headers"] = "\n".join(f"{k}: {v}" for k, v in response_headers.items())
        self.response_data["cookies"] = "\n".join(f"{k}: {v}" for k, v in response_cookies.items())

        self.update_response_view(self.view_mode.get())

    




    def send_put_request(self, url, data=None):
        status_code, response_content , response_headers, response_cookies = self.api.put(url, params=data["query"], headers=data["headers"], query=data["body"])

        self.response_data["status"] = status_code
        self.response_data["html"] = response_content
        self.response_data["headers"] = "\n".join(f"{k}: {v}" for k, v in response_headers.items())
        self.response_data["cookies"] = "\n".join(f"{k}: {v}" for k, v in response_cookies.items())

        self.update_response_view(self.view_mode.get())




    # Gestion des requêtes DELETE, aucune valeur n'est demandée dans l'application, juste besoin de key
    def send_delete_request(self, url, data=None):
        status_code, response_content , response_headers, response_cookies = self.api.delete(url, params=data["query"], headers=data["headers"], query=data["body"])

        self.response_data["status"] = status_code
        self.response_data["html"] = response_content
        self.response_data["headers"] = "\n".join(f"{k}: {v}" for k, v in response_headers.items())
        self.response_data["cookies"] = "\n".join(f"{k}: {v}" for k, v in response_cookies.items())

        self.update_response_view(self.view_mode.get())
        






    # Mise à jour de l'affichage de la réponse
    def update_response_view(self , mode):
        self.response_text.config(state="normal")# 🔓 déverrouille
        self.response_label.config(text=f"Response : {self.response_data['status']}") # Met à jour le code de statut
        
        
        if mode == "HTML":
            self.response_text.delete("1.0", END)
            self.response_text.insert(END, self.response_data["html"])
            self.response_text.config(state="disabled")
        
        elif mode == "Headers":
            self.response_text.delete("1.0", END)
            self.response_text.insert(END, self.response_data["headers"])
            self.response_text.config(state="disabled")

        elif mode == "Cookies":
            self.response_text.delete("1.0", END)
            self.response_text.insert(END, self.response_data["cookies"])
            self.response_text.config(state="disabled")


    













    # Gestion de la fenêtre d'automatisation
    def open_automatisation_window(self):
        self.automatisationWindow(self.root, self.api)







    def automatisationWindow(self, parent, api):
        self.top = Toplevel(parent)
        self.top.title("Automatisation")
        self.top.state('zoomed')
        self.api = api

        self.top.grid_rowconfigure(0, weight=0)
        self.top.grid_rowconfigure(1, weight=0)
        self.top.grid_rowconfigure(2, weight=1)

        # Frame pour l'en-tête de la fenêtre d'automatisation
        self.bruteforce_header_frame = Frame(self.top, bg="#909090")
        self.bruteforce_header_frame.grid(row=0, column=0, sticky="nsew")
        self.label = Label(self.bruteforce_header_frame, text="Automatisation des requêtes", font=("Arial", 16))
        self.label.pack(pady=20)


        # Frame pour les champs d'entrée de la fenêtre d'automatisation
        self.bruteforce_main_frame = Frame(self.top, bg="#909090")
        self.bruteforce_main_frame.grid(row=1, column=0, sticky="nsew")

        self.bruteforce_main_frame.grid_rowconfigure(0, weight=0)
        self.bruteforce_main_frame.grid_rowconfigure(1, weight=1)
        self.bruteforce_main_frame.grid_rowconfigure(2, weight=0)
        self.bruteforce_main_frame.grid_rowconfigure(3, weight=0)
        self.bruteforce_main_frame.grid_rowconfigure(4, weight=0)
        self.bruteforce_main_frame.grid_columnconfigure(0, weight=1)
        self.bruteforce_main_frame.grid_columnconfigure(1, weight=1)


        self.label_bruteforce_url = Label(self.bruteforce_main_frame, text="Url", font=("Arial", 14))
        self.label_bruteforce_url.grid(row=3,column=1, pady=10, sticky="w")

        self.bruteforce_url = Entry(self.bruteforce_main_frame, fg = "black", bg="#FFFFFF", font = ("Arial", 14), width=50)
        self.bruteforce_url.grid(row=4,column=1, pady=10, sticky="w")


        self.list_password = Text(self.bruteforce_main_frame, fg = "black", bg="#C0C0C0", font = ("Arial", 12), width=80, height=20)
        self.list_password.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")

        def nb_mdp(self):
            lines = self.list_password.get("1.0", "end-1c").splitlines()
            nb_password = [line for line in lines if line.strip()]
            return len(nb_password)

        

        self.label_bruteforce_key = Label(self.bruteforce_main_frame, text="Clé de bruteforce", font=("Arial", 14))
        self.label_bruteforce_key.grid(row=0, column=1, pady=10, sticky="w")

        

        self.bruteforce_key = Entry(self.bruteforce_main_frame, fg = "black", bg="#FFFFFF", font = ("Arial", 14), width=50)
        self.bruteforce_key.grid(row=1, column=1, pady=10)


        self.execute_button = ttk.Button(self.bruteforce_main_frame, text="Exécuter", command=lambda: bruteforce(self))
        self.execute_button.grid(row=2, column=1, pady=10)

        

        #boucle pour executer le bruteforce
        def bruteforce(self):
            self.key = self.bruteforce_key.get()
            self.key2_obligatoire = self.bruteforce_key2.get()
            self.url = self.bruteforce_url.get()
            self.nb_password = str(nb_mdp(self))
            print(f"Nombre de mots de passe à tester : {self.nb_password}")
            print(f"Clé de bruteforce : {self.key}")
            passwords = [line.strip()for line in self.list_password.get("1.0", "end-1c").splitlines()if line.strip()]
            print(f"Test des mots de passe : {passwords}")
            
            
                
            for password in passwords:
                data = {self.key: password, self.key2_obligatoire: "application"}
                status_code, response_content , response_headers, response_cookies, longueur = self.api.post(self.url, query=data)
                print(f"Test du mot de passe : {password} - Longueur de la réponse : {longueur}")
                #print(response_content)


        
        self.footer_frame = Frame(self.top, bg="#909090")
        self.footer_frame.grid(row=2, column=0, sticky="nsew")


        self.footer_frame.grid_rowconfigure(0, weight=1)
        self.footer_frame.grid_rowconfigure(1, weight=0)
        self.footer_frame.grid_rowconfigure(2, weight=0)

        self.label_bruteforce_key2 = Label(self.footer_frame, text="Clé de bruteforce 2 (optionnelle)", font=("Arial", 14))
        self.label_bruteforce_key2.grid(row=0, column=0, pady=10, sticky="w")

        self.bruteforce_key2 = Entry(self.footer_frame, fg = "black", bg="#FFFFFF", font = ("Arial", 14), width=50)
        self.bruteforce_key2.grid(row=1, column=0, pady=10)
        
        close_button = ttk.Button(self.footer_frame, text="Fermer", command=self.top.destroy)
        close_button.grid(row=2, pady=10)