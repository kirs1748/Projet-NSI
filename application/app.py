import platform
import threading
from tkinter import *
from tkinter import ttk, messagebox
from api import ApiClient
from fonctions import parse_html, ScrollableKeyValueFrame


class App:
    """
    Application principale permettant :
    - d'envoyer des requêtes HTTP (GET, POST, PUT, DELETE)
    - de gérer Query / Headers / Body
    - d'afficher la réponse
    - d'exécuter une automatisation type bruteforce
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Nom de l'application")

        # Maximisation automatique selon OS
        try:
            if platform.system() == "Windows":
                self.root.state("zoomed")
            else:
                self.root.attributes("-zoomed", True)
        except:
            pass

        # Backend API
        self.api = ApiClient()

        # Type de paramètre actif
        self.current_param_type = "query"

        # Stockage des paramètres
        self.params = {
            "query": {},
            "headers": {},
            "body": {}
        }

        # Stockage des réponses
        self.response_data = {
            "html": "",
            "headers": "",
            "cookies": "",
            "status": ""
        }

        self._build_ui()

    # ================= INTERFACE =================

    def _build_ui(self):

        # MENU
        self.menubar = Menu(self.root)
        self.menubar.add_command(label="Requetes",
                                 command=lambda: print("Requete clicked"))
        self.menubar.add_command(label="Automatisation",
                                 command=self.open_automatisation_window)
        self.root.config(menu=self.menubar)

        # TOOLBAR
        toolbar = ttk.Frame(self.root, padding=(8, 6))
        toolbar.pack(side=TOP, fill=X)

        ttk.Label(toolbar,
                  text="Nom de l'application",
                  font=("Segoe UI", 14, "bold")).pack(side=LEFT, padx=(0, 12))

        self.method_var = StringVar(value="GET")
        method_cb = ttk.Combobox(toolbar,
                                 textvariable=self.method_var,
                                 values=["GET", "POST", "PUT", "DELETE"],
                                 width=8,
                                 state="readonly")
        method_cb.pack(side=LEFT, padx=(0, 8))

        self.url_entry = ttk.Entry(toolbar, width=80)
        self.url_entry.pack(side=LEFT, fill=X, expand=True, padx=(0, 8))
        #self.url_entry.insert(0, "https://")

        self.send_btn = ttk.Button(toolbar,
                                   text="Send",
                                   command=self.send_request)
        self.send_btn.pack(side=LEFT)

        # ZONE PRINCIPALE
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill=BOTH, expand=True)

        # PARAMS
        left = ttk.Labelframe(main,
                              text="Parameters / Headers / Body",
                              padding=8)
        left.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 8))

        top = ttk.Frame(left)
        top.pack(fill=X)

        self.param_type_var = StringVar(value="Query")

        param_menu = ttk.Combobox(top,
                                  textvariable=self.param_type_var,
                                  values=["Query", "Headers", "Body"],
                                  state="readonly",
                                  width=12)
        param_menu.pack(side=LEFT)

        param_menu.bind(
            "<<ComboboxSelected>>",
            lambda e: self.change_param_type(self.param_type_var.get())
        )

        ttk.Button(top,
                   text="Add",
                   command=lambda: self.params_table.add_row()).pack(side=RIGHT)

        self.params_table = ScrollableKeyValueFrame(left, height=300)
        self.params_table.pack(fill=BOTH, expand=True, pady=(8, 0))

        # RESPONSE
        right = ttk.Labelframe(main, text="Response", padding=8)
        right.pack(side=LEFT, fill=BOTH, expand=True)

        self.status_label = ttk.Label(right, text="Status: -")
        self.status_label.pack(anchor="w")

        self.response_text = Text(right, height=25)
        self.response_text.pack(fill=BOTH, expand=True, pady=(8, 0))

    # ================= PARAMÈTRES =================

    def change_param_type(self, value):
        new_type = value.lower()
        self.params[self.current_param_type] = \
            self.params_table.get_data()
        self.current_param_type = new_type
        self.params_table.load_data(self.params[new_type])

    def prepare_request_data(self):
        return {
            "query": self.params["query"],
            "headers": self.params["headers"],
            "body": self.params["body"]
        }

    # ================= REQUÊTES =================

    def send_request(self):

        self.params[self.current_param_type] = \
            self.params_table.get_data()

        method = self.method_var.get()
        url = self.url_entry.get().strip()
        data = self.prepare_request_data()

        if not url:
            messagebox.showerror("URL missing",
                                 "Please provide a URL.")
            return

        thread = threading.Thread(
            target=self._execute_request,
            args=(method, url, data),
            daemon=True
        )
        thread.start()

    def _execute_request(self, method, url, data):

        try:
            if method == "GET":
                result = self.api.get(
                    url,
                    params=data["query"],
                    headers=data["headers"]
                )

            elif method == "POST":
                result = self.api.post(
                    url,
                    params=data["query"],
                    headers=data["headers"],
                    query=data["body"]
                )

            elif method == "PUT":
                result = self.api.put(
                    url,
                    params=data["query"],
                    headers=data["headers"],
                    query=data["body"]
                )

            elif method == "DELETE":
                result = self.api.delete(
                    url,
                    params=data["query"],
                    headers=data["headers"],
                    query=data["body"]
                )
            else:
                return

            status_code = result[0]
            response_content = result[1]
            response_headers = result[2]
            response_cookies = result[3]

            content = parse_html(response_content)

            self.response_data["status"] = status_code
            self.response_data["html"] = content
            self.response_data["headers"] = \
                "\n".join(f"{k}: {v}" for k, v in response_headers.items())
            self.response_data["cookies"] = \
                "\n".join(f"{k}: {v}" for k, v in response_cookies.items())

        except Exception as e:
            self.response_data["html"] = str(e)

        self.root.after(0, self.update_response_view)

    # ================= RÉPONSE =================

    def update_response_view(self):

        self.response_text.config(state="normal")
        self.response_text.delete("1.0", END)
        self.response_text.insert("1.0",
                                  self.response_data["html"])
        self.response_text.config(state="disabled")

        self.status_label.config(
            text=f"Status: {self.response_data['status']}"
        )

    # ================= AUTOMATISATION =================

    def open_automatisation_window(self):
        self.automatisationWindow(self.root, self.api)

    def automatisationWindow(self, parent, api):

        self.top = Toplevel(parent)
        self.top.title("Automatisation")
        self.top.state('zoomed')

        Label(self.top,
            text="Automatisation des requêtes",
            font=("Arial", 16)).pack(pady=20)

        # ===== LABEL EXPLICATIF =====
        Label(
            self.top,
            text="⚠ Ce bruteforce fonctionne uniquement lorsque le message "
                "d'erreur change si le bon username est trouvé.\n"
                "Cela se remarque généralement via une différence de longueur "
                "dans la réponse HTTP.\n"
                "Les résultats de l'attaque sont affichés dans la console.",
            fg="red",
            justify=LEFT,
            font=("Arial", 11)
        ).pack(pady=10)

        self.main_frame = Frame(self.top)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Liste des mots de passe
        self.list_password = Text(self.main_frame, width=80, height=20)
        self.list_password.pack(side=LEFT, padx=10, pady=10)

        self.right_frame = Frame(self.main_frame)
        self.right_frame.pack(side=LEFT, padx=10)

        # URL
        Label(self.right_frame, text="URL").pack()
        self.bruteforce_url = Entry(self.right_frame, width=50)
        self.bruteforce_url.pack()

        # Clé principale
        Label(self.right_frame, text="Clé bruteforce 1").pack()
        self.bruteforce_key1 = Entry(self.right_frame, width=50)
        self.bruteforce_key1.pack()

        # Clé secondaire
        Label(self.right_frame, text="Clé bruteforce 2 (mettre la valeur de la clé à ne pas tester)").pack()
        self.bruteforce_key2 = Entry(self.right_frame, width=50)
        self.bruteforce_key2.pack()

        # Valeur clé secondaire
        Label(self.right_frame, text="Valeur clé 2 (a complété par l'username trouvé)").pack()
        self.bruteforce_value2 = Entry(self.right_frame, width=50)
        self.bruteforce_value2.insert(0, "test")
        self.bruteforce_value2.pack()

        def bruteforce():

            url = self.bruteforce_url.get()
            key1 = self.bruteforce_key1.get()
            key2 = self.bruteforce_key2.get()
            value2 = self.bruteforce_value2.get()

            passwords = [
                line.strip()
                for line in self.list_password.get("1.0", "end-1c").splitlines()
                if line.strip()
            ]

            for password in passwords:

                data = {key1: password}

                if key2:
                    data[key2] = value2

                result = self.api.post(url, query=data)

                if len(result) == 5:
                    status_code, content, headers, cookies, longueur = result
                    print(f"{password} -> longueur: {longueur}")
                else:
                    print(f"{password} testé")

        ttk.Button(self.right_frame,
                text="Exécuter",
                command=bruteforce).pack(pady=10)

        ttk.Button(self.right_frame,
                text="Fermer",
                command=self.top.destroy).pack(pady=10)




if __name__ == "__main__":
    root = Tk()
    App(root)
    root.mainloop()
