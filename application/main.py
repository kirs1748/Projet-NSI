from tkinter import *
from fonctions import *

app  = Tk()
app.title("Application name")
app.geometry("800x600")
#app.attributes( "-fullscreen" , True )
app.config( bg = "#595657" )

# Barre de menu

menubar = Menu(app)
automatisation = Menu(menubar, tearoff=0)
automatisation.add_command(label="1er auto", command=lambda: print("Option 1 selected"))
menubar.add_cascade(label="Automatisation", menu=automatisation)
app.config(menu=menubar)

app_title = Label( app , text = "Application name" , fg = "white", bg="#595657", font = ("Arial", 30))
app_title.pack(side=TOP)

frame_requete = Frame( app, bg = "#FFFFFF" )
frame_requete.pack()

request_scrollbar = Scrollbar(frame_requete,bg="#FFFFFF")
request_scrollbar.pack( side=LEFT, fill=Y )
request_listbox = Listbox( frame_requete, fg = "black", bg="#FFFFFF", font = ("Arial", 14), width=10, height=5, yscrollcommand=request_scrollbar.set )
request_listbox.pack( side=LEFT, fill=BOTH, padx=10, pady=10 )


url = Entry( frame_requete , fg = "black", bg="#B13636", font = ("Arial", 20), width=40 )
url.pack( side=LEFT, padx=10, pady=10 )

send_button = Button(frame_requete , text = "Send" , fg = "black", bg="#D3D3D3", font = ("Arial", 20), command=send_request )
send_button.pack( side=LEFT, padx=10, pady=10 )

frame_requete.pack(fill=X)


app.mainloop()