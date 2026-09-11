import tkinter as tk
from tkinter import ttk # für neuere, adaptive Widgets
import sqlite3


## Database ##

database = "Velojournal.db"

con = sqlite3.connect(database)
cur = con.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS fahrten (
            datum TEXT,
            route TEXT NOT NULL,
            kilometer REAL,
            aufstieg INTEGER,
            abstieg INTEGER,
            zeit TEXT
            )
            """)

## Root-Window Gui ##

root = tk.Tk()
root.title("Velojournal")
root.geometry("800x650")

## Events

### neuen eintrag speichern
def submit():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # insert into table
    cur.execute("insert into fahrten values(:datum, :route, :kilometer, :aufstieg, :abstieg, :zeit)",
                {
                    'datum': datum.get(),
                    'route': route.get(),
                    'kilometer': kilometer.get(),
                    'aufstieg': aufstieg.get(),
                    'abstieg': abstieg.get(),
                    'zeit': zeit.get()
                    }
                )

    con.commit()
    con.close()

    # clear textboxes
    datum.delete(0, END) # 0, END meint: von Anfang bis Ende
    route.delete(0, END)
    kilometer.delete(0, END)
    aufstieg.delete(0, END)
    abstieg.delete(0, END)
    zeit.delete(0, END)

### Eintrag updaten ###
def update():
    pass
    #TODO: Funktion update record in database

### Eintrag löschen ###
def delete():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # Ausgewählten Eintrag löschen
    cur.execute("DELETE FROM fahrten WHERE oid=" + select_box.get())

    con.commit()
    con.close()

    # Clear Select-Box
    select_box.delete(0, END)

### Eintrag bearbeiten
def edit():
    editor = tk.Tk()
    editor.title("Bearbeiten")
    editor.geometry("800x650")

    ### Labels ###
    datum_label_editor = ttk.Label(editor, text="Datum")
    datum_label_editor.grid(row=0, column=0, padx=15, pady=5)
    route_label_editor = ttk.Label(editor, text="Route")
    route_label_editor.grid(row=1, column=0, pady=5)
    kilometer_label_editor = ttk.Label(editor, text="Kilometer")
    kilometer_label_editor.grid(row=2, column=0, pady=5)
    aufstieg_label_editor = ttk.Label(editor, text="Aufstieg")
    aufstieg_label_editor.grid(row=3, column=0, pady=5)
    abstieg_label_editor = ttk.Label(editor, text="Abstieg")
    abstieg_label_editor.grid(row=4, column=0, pady=5)
    zeit_label_editor = ttk.Label(editor, text="Zeit")
    zeit_label_editor.grid(row=5, column=0, pady=5)

    ### Eingabefelder ###
    datum_editor = ttk.Entry(editor, width=80)
    datum_editor.grid(row=0, column=1, padx=10)
    route_editor = ttk.Entry(editor, width=80)
    route_editor.grid(row=1, column=1)
    kilometer_editor = ttk.Entry(editor, width=80)
    kilometer_editor.grid(row=2, column=1)
    aufstieg_editor = ttk.Entry(editor, width=80)
    aufstieg_editor.grid(row=3, column=1)
    abstieg_editor = ttk.Entry(editor, width=80)
    abstieg_editor.grid(row=4, column=1)
    zeit_editor = ttk.Entry(editor, width=80)
    zeit_editor.grid(row=5, column=1)

    ### Save-Button for edited entry ###
    submit_button_editor = ttk.Button(editor, text="Speichern", command=update)
    submit_button_editor.grid(row=6, column=1, padx=9, pady=5, sticky="w")

    con = sqlite3.connect(database)
    cur = con.cursor()
    record_id = select_box.get()
    cur.execute("SELECT * FROM fahrten WHERE oid=" + record_id)
    records = cur.fetchall()
    # Loop through result - a bit odd, because it is always one record...
    for record in records:
        datum_editor.insert(0, record[0]) # 0 = Stelle, wo item eingefügt
        route_editor.insert(0, record[1]) # 0 = Stelle, wo item eingefügt
        kilometer_editor.insert(0, record[2]) # 0 = Stelle, wo item eingefügt
        aufstieg_editor.insert(0, record[3]) # 0 = Stelle, wo item eingefügt
        abstieg_editor.insert(0, record[4]) # 0 = Stelle, wo item eingefügt
        zeit_editor.insert(0, record[5]) # 0 = Stelle, wo item eingefügt

    con.commit()
    con.close()

    # clear select-box
    select_box.delete(0, END)

### Einträge anzeigen
def query():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # Alles anzeigen
    cur.execute("SELECT *, oid FROM fahrten")
    fahrten = cur.fetchall()
    print(fahrten)

    # Loop durch alle Fahrten, dabei alle zusammenschliessen zu 
    # einer String print_fahrten. fahrt[6] ist die oid
    print_fahrten = ""
    for fahrt in fahrten:
        print_fahrten += fahrt[0] + ": " + fahrt[1] + " | " + str(fahrt[2]) + " km, " + str(fahrt[3]) + " m Aufstieg, " + str(fahrt[4]) + " m Abfahrt, " + str(fahrt[5]) + " Fahrzeit (" + str(fahrt[6]) +")\n"

    query_label = ttk.Label(menu, text=print_fahrten)
    query_label.grid(row=11, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    con.commit()
    con.close()

### Treeview-Table ###
records = ttk.Frame(root)
table = ttk.Treeview(records, columns = ("Datum", "Route", "Km", "Aufstieg", "Abstieg", "Zeit"), show = "headings")
table.heading("Datum", text = "Datum")
table.heading("Route", text = "Route")
table.heading("Km", text = "Km")
table.heading("Aufstieg", text = "Aufstieg")
table.heading("Abstieg", text = "Abstieg")
table.heading("Zeit", text = "Zeit")
table.pack()
records.pack()

### Labels ###
menu = ttk.Frame(root)
datum_label = ttk.Label(menu, text="Datum")
datum_label.grid(row=0, column=0, padx=15, pady=5)
route_label = ttk.Label(menu, text="Route")
route_label.grid(row=1, column=0, pady=5)
kilometer_label = ttk.Label(menu, text="Kilometer")
kilometer_label.grid(row=2, column=0, pady=5)
aufstieg_label = ttk.Label(menu, text="Aufstieg")
aufstieg_label.grid(row=3, column=0, pady=5)
abstieg_label = ttk.Label(menu, text="Abstieg")
abstieg_label.grid(row=4, column=0, pady=5)
zeit_label = ttk.Label(menu, text="Zeit")
zeit_label.grid(row=5, column=0, pady=5)
select_label = ttk.Label(menu, text="ID")
select_label.grid(row=7, column=0, pady=5)

### Eingabefelder ###
datum = ttk.Entry(menu, width=80)
datum.grid(row=0, column=1, padx=10)
route = ttk.Entry(menu, width=80)
route.grid(row=1, column=1)
kilometer = ttk.Entry(menu, width=80)
kilometer.grid(row=2, column=1)
aufstieg = ttk.Entry(menu, width=80)
aufstieg.grid(row=3, column=1)
abstieg = ttk.Entry(menu, width=80)
abstieg.grid(row=4, column=1)
zeit = ttk.Entry(menu, width=80)
zeit.grid(row=5, column=1)
select_box = ttk.Entry(menu, width=80)
select_box.grid(row=7, column=1)

### Submit-Button ###
submit_button = ttk.Button(menu, text="Fahrt hinzufügen", command=submit)
submit_button.grid(row=6, column=1, padx=9, pady=5, sticky="w")

### Delete-Button ###
delete_button = ttk.Button(menu, text="Fahrt löschen", command=delete)
delete_button.grid(row=8, column=1, padx=9, pady=5, sticky="w")

### Update-Button ###
edit_button = ttk.Button(menu, text="Fahrt bearbeiten", command=edit)
edit_button.grid(row=9, column=1, padx=9, pady=5, sticky="w")

### Query-Button ###
query_button = ttk.Button(menu, text="Fahrten anzeigen", command=query)
query_button.grid(row=10, column=1, padx=9, pady=5, sticky="w")

menu.pack()

## Alle Änderungen übernehmen und Verbindung schliessen
con.commit()
con.close()

## Loop ##
root.mainloop()
