import tkinter as tk
from tkinter import ttk # für neuere, adaptive Widgets
import sqlite3

"""
TODOs:
- widgets und events für suche und sortieren erstellen.
  - Prio 1: Suche in Zeitspanne
  - Prio 2: Suche nach Kilometern
- Zusammenfassung anzeigen
  - Total Distanz
  - Total Aufstieg
  - Total Abstieg
"""

## Database ##

database = "Velojournal.db"

con = sqlite3.connect(database)
cur = con.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS fahrten (
            datum TEXT,
            route TEXT NOT NULL,
            distanz REAL,
            aufstieg INTEGER,
            abstieg INTEGER,
            zeit TEXT
            )
            """)


## Events

# Editor öffnen
def open_editor():
    # Fenster Editor öffnen
    editor = tk.Tk()
    editor.title("Bearbeiten")
    editor.geometry("600x250")

    # Labels
    datum_label_editor = ttk.Label(editor, text="Datum")
    datum_label_editor.grid(row=0, column=0, padx=15, pady=5)
    route_label_editor = ttk.Label(editor, text="Route")
    route_label_editor.grid(row=1, column=0, pady=5)
    distanz_label_editor = ttk.Label(editor, text="Distanz")
    distanz_label_editor.grid(row=2, column=0, pady=5)
    aufstieg_label_editor = ttk.Label(editor, text="Aufstieg")
    aufstieg_label_editor.grid(row=3, column=0, pady=5)
    abstieg_label_editor = ttk.Label(editor, text="Abstieg")
    abstieg_label_editor.grid(row=4, column=0, pady=5)
    zeit_label_editor = ttk.Label(editor, text="Zeit")
    zeit_label_editor.grid(row=5, column=0, pady=5)

    # Create global variables (for update-function)
    global datum_editor
    global route_editor
    global distanz_editor
    global aufstieg_editor
    global abstieg_editor
    global zeit_editor

    # Eingabefelder
    datum_editor = ttk.Entry(editor, width=60)
    datum_editor.grid(row=0, column=1, padx=20)
    route_editor = ttk.Entry(editor, width=60)
    route_editor.grid(row=1, column=1)
    distanz_editor = ttk.Entry(editor, width=60)
    distanz_editor.grid(row=2, column=1)
    aufstieg_editor = ttk.Entry(editor, width=60)
    aufstieg_editor.grid(row=3, column=1)
    abstieg_editor = ttk.Entry(editor, width=60)
    abstieg_editor.grid(row=4, column=1)
    zeit_editor = ttk.Entry(editor, width=60)
    zeit_editor.grid(row=5, column=1)

    # close-function
    def safe_and_close():
        update()
        editor.destroy()

    # Save-Button for edited entry
    submit_button_editor = ttk.Button(editor, text="Speichern", command=safe_and_close)
    submit_button_editor.grid(row=6, column=1, padx=20, pady=5, sticky="e")


### neuen eintrag speichern
def submit():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # insert into table
    cur.execute("insert into fahrten values(:datum, :route, :distanz, :aufstieg, :abstieg, :zeit)",
                {
                    'datum': datum.get(),
                    'route': route.get(),
                    'distanz': distanz.get(),
                    'aufstieg': aufstieg.get(),
                    'abstieg': abstieg.get(),
                    'zeit': zeit.get()
                    }
                )

    con.commit()
    con.close()

    # add to treeview
    table.insert('', 0, values=(datum.get(), route.get(),distanz.get(), aufstieg.get(), abstieg.get(), zeit.get(),))

    # clear textboxes
    datum.delete(0, tk.END) # 0, END meint: von Anfang bis Ende
    route.delete(0, tk.END)
    distanz.delete(0, tk.END)
    aufstieg.delete(0, tk.END)
    abstieg.delete(0, tk.END)
    zeit.delete(0, tk.END)

### eintrag updaten ###
def update():
    # update record in database
    con = sqlite3.connect(database)
    cur = con.cursor()

    cur.execute("""UPDATE fahrten SET
                datum = :datum,
                route = :route,
                distanz = :distanz,
                aufstieg = :aufstieg,
                abstieg = :abstieg,
                zeit = :zeit
                WHERE oid = :oid
                """,
                {
                    'datum': datum_editor.get(),
                    'route': route_editor.get(),
                    'distanz': distanz_editor.get(),
                    'aufstieg': aufstieg_editor.get(),
                    'abstieg': abstieg_editor.get(),
                    'zeit': zeit_editor.get(),
                    'oid': oid_edited
                    }
                )
    con.commit()
    con.close()

    # Update record in Treeview
    # grab the record number
    selected = table.focus()
    # update record in treeview
    table.item(selected, text="", values=(datum_editor.get(), route_editor.get(),distanz_editor.get(), aufstieg_editor.get(), abstieg_editor.get(), zeit_editor.get(), oid_edited,))

### Eintrag löschen ###
def delete():
    # get Zeilennummer Treeview
    selected = table.focus() # selected = Zeilennummer Treeview

    # get Werte dieser Zeile
    values = table.item(selected, 'values') # values = Tuple mit Werten aus Treeview (als strings), (value[6] == oid)

    oid_to_delete = values[6] # value[6] == oid

    # Ausgewählten Eintrag aus Datenbank löschen
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("DELETE FROM fahrten WHERE oid=" + oid_to_delete)
    con.commit()
    con.close()

    # Ausgewählten Eintrag aus Treeview löschen
    table.delete(selected)

### editor öffnen und eintrag bearbeiten ###
def edit_in_editor(e):

    # Editor öffnen
    open_editor()

    # get Zeilennummer Treeview
    selected = table.focus() # selected = Zeilennummer Treeview

    # get Werte dieser Zeile
    values = table.item(selected, 'values') # values = Tuple mit Werten aus Treeview (als strings), (value[6] == oid)

    global oid_edited
    oid_edited = values[6]

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM fahrten WHERE oid=" + oid_edited)
    records = cur.fetchall()
    # Loop through result - a bit odd, because it is always one record...
    for record in records:
        datum_editor.insert(0, record[0]) # 0 = Stelle, wo item eingefügt
        route_editor.insert(0, record[1]) # 0 = Stelle, wo item eingefügt
        distanz_editor.insert(0, record[2]) # 0 = Stelle, wo item eingefügt
        aufstieg_editor.insert(0, record[3]) # 0 = Stelle, wo item eingefügt
        abstieg_editor.insert(0, record[4]) # 0 = Stelle, wo item eingefügt
        zeit_editor.insert(0, record[5]) # 0 = Stelle, wo item eingefügt

    con.commit()
    con.close()

### Eintrag bearbeiten
def edit():

    open_editor()

    # get Zeilennummer Treeview
    selected = table.focus() # selected = Zeilennummer Treeview

    # get Werte dieser Zeile
    values = table.item(selected, 'values') # values = Tuple mit Werten aus Treeview (als strings), (value[6] == oid)

    global oid_edited
    oid_edited = values[6]

    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute("SELECT * FROM fahrten WHERE oid=" + oid_edited)
    records = cur.fetchall()
    # Loop through result - a bit odd, because it is always one record...
    for record in records:
        datum_editor.insert(0, record[0]) # 0 = Stelle, wo item eingefügt
        route_editor.insert(0, record[1]) # 0 = Stelle, wo item eingefügt
        distanz_editor.insert(0, record[2]) # 0 = Stelle, wo item eingefügt
        aufstieg_editor.insert(0, record[3]) # 0 = Stelle, wo item eingefügt
        abstieg_editor.insert(0, record[4]) # 0 = Stelle, wo item eingefügt
        zeit_editor.insert(0, record[5]) # 0 = Stelle, wo item eingefügt

    con.commit()
    con.close()

### Einträge anzeigen
def query():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # Alles anzeigen
    cur.execute("SELECT rowid, * FROM fahrten")
    fahrten = cur.fetchall()

    for fahrt in fahrten:
        table.insert(parent='', index='end', text='', values=(fahrt[1], fahrt[2], fahrt[3], fahrt[4], fahrt[5], fahrt[6], fahrt[0]))

        #print_fahrten += fahrt[0] + ": " + fahrt[1] + " | " + str(fahrt[2]) + " km, " + str(fahrt[3]) + " m Aufstieg, " + str(fahrt[4]) + " m Abfahrt, " + str(fahrt[5]) + " Fahrzeit (" + str(fahrt[6]) +")\n"

    con.commit()
    con.close()


#####################
##       Gui       ##
#####################


## Root-Window
root = tk.Tk()
root.title("Velojournal")
root.geometry("800x650")

## Treeview-Table ##

### Create the Frame ###
tree_frame = ttk.Frame(root, borderwidth=10)
tree_frame.pack()

### Create the Scrollbar ###
tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

### Create the Treeview-Table ###
table = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
table.pack()

### Configure Scrollbar ###
tree_scroll.config(command=table.yview)

### Define Columns ###
table['columns'] = ("Datum", "Route", "Distanz", "Aufstieg", "Abstieg", "Zeit")

### Format Columns ###
table.column("#0", width=0, stretch=tk.NO)
table.column("Datum", anchor=tk.W, width=80)
table.column("Route", anchor=tk.W, width=390)
table.column("Distanz", anchor=tk.E, width=70)
table.column("Aufstieg", anchor=tk.E, width=70)
table.column("Abstieg", anchor=tk.E, width=70)
table.column("Zeit", anchor=tk.E, width=50)

### Create Headings ###
table.heading("#0", text = "")
table.heading("Datum", text = "Datum", anchor=tk.W)
table.heading("Route", text = "Route", anchor=tk.W)
table.heading("Distanz", text = "Distanz", anchor=tk.CENTER)
table.heading("Aufstieg", text = "Aufstieg", anchor=tk.CENTER)
table.heading("Abstieg", text = "Abstieg", anchor=tk.CENTER)
table.heading("Zeit", text = "Zeit", anchor=tk.CENTER)

### Frame Menu ###
menu = ttk.Frame(root, borderwidth=10)

### Delete-Button ###
delete_button = ttk.Button(menu, text="Fahrt löschen", command=delete)
delete_button.grid(row=0, column=0, padx=15, pady=5, sticky="w")

### Update-Button ###
edit_button = ttk.Button(menu, text="Fahrt bearbeiten", command=edit)
edit_button.grid(row=0, column=1, padx=9, pady=5, sticky="w")

### Menu anzeigen
menu.pack()

### Frame newEntry ###
newEntry = ttk.Frame(root, padding=10, borderwidth=1, relief="ridge")

### labels newEnty ###
datum_label = ttk.Label(newEntry, text="Datum")
datum_label.grid(row=0, column=0, pady=5)
route_label = ttk.Label(newEntry, text="Route")
route_label.grid(row=0, column=2, pady=5)
distanz_label = ttk.Label(newEntry, text="Distanz")
distanz_label.grid(row=1, column=0, pady=5)
aufstieg_label = ttk.Label(newEntry, text="Aufstieg")
aufstieg_label.grid(row=1, column=2, padx=5, pady=5)
abstieg_label = ttk.Label(newEntry, text="Abstieg")
abstieg_label.grid(row=1, column=4, padx=5, pady=5)
zeit_label = ttk.Label(newEntry, text="Zeit")
zeit_label.grid(row=1, column=6, padx=5, pady=5)

### eingabefelder ###
datum = ttk.Entry(newEntry, width=10)
datum.grid(row=0, column=1, padx=10)
route = ttk.Entry(newEntry, width=45)
route.grid(row=0, column=3, columnspan=5)
distanz = ttk.Entry(newEntry, width=10)
distanz.grid(row=1, column=1)
aufstieg = ttk.Entry(newEntry, width=10)
aufstieg.grid(row=1, column=3)
abstieg = ttk.Entry(newEntry, width=10)
abstieg.grid(row=1, column=5)
zeit = ttk.Entry(newEntry, width=10)
zeit.grid(row=1, column=7)

### submit-button ###
submit_button = ttk.Button(newEntry, text="Fahrt hinzufügen", command=submit)
submit_button.grid(row=2, column=0, columnspan=2, padx=9, pady=10)

### newEntry anzeigen
newEntry.pack()

## Alle Änderungen übernehmen und Verbindung schliessen
con.commit()
con.close()

# Bind the treeview
table.bind("<Double-Button-1>", edit_in_editor) # Doppelklick für Editor

# Anzeige der Daten aus Datenbank beim Start
query()

## Loop ##
root.mainloop()
