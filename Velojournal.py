from tkinter import *
from tkinter import ttk # für neuere, adaptive Widgets
import sqlite3

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

## Events

### Neuen Eintrag speichern
def submit():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # Insert into table
    cur.execute("INSERT INTO fahrten VALUES(:datum, :route, :kilometer, :aufstieg, :abstieg, :zeit)",
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

    # Clear Textboxes
    datum.delete(0, END)
    route.delete(0, END)
    kilometer.delete(0, END)
    aufstieg.delete(0, END)
    abstieg.delete(0, END)
    zeit.delete(0, END)

### Eintrag löschen
def delete():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # Ausgewählten Eintrag löschen
    cur.execute("DELETE FROM fahrten WHERE oid=" + delete_box.get())

    con.commit()
    con.close()

    # Clear Delete-Box
    delete_box.delete(0, END)

### Einträge anzeigen
def query():
    con = sqlite3.connect(database)
    cur = con.cursor()
    # Alles anzeigen
    cur.execute("SELECT *, oid FROM fahrten")
    fahrten = cur.fetchall()

    # Loop durch alle Fahrten, dabei alle zusammenschliessen zu 
    # einer String print_fahrten. fahrt[6] ist die oid
    print_fahrten = ""
    for fahrt in fahrten:
        print_fahrten += fahrt[0] + ": " + fahrt[1] + " | " + str(fahrt[2]) + " km, " + str(fahrt[3]) + " m Aufstieg, " + str(fahrt[4]) + " m Abfahrt, " + str(fahrt[5]) + " Fahrzeit (" + str(fahrt[6]) +")\n"

    query_label = ttk.Label(root, text=print_fahrten)
    query_label.grid(row=10, column=0, columnspan=2, padx=10, pady=5, sticky="w")
    con.commit()
    con.close()


## Gui ##

root = Tk()
root.title("Velojournal")
root.geometry("800x650")

### Labels ###

datum_label = ttk.Label(root, text="Datum")
datum_label.grid(row=0, column=0, padx=15, pady=5)

route_label = ttk.Label(root, text="Route")
route_label.grid(row=1, column=0, pady=5)

kilometer_label = ttk.Label(root, text="Kilometer")
kilometer_label.grid(row=2, column=0, pady=5)

aufstieg_label = ttk.Label(root, text="Aufstieg")
aufstieg_label.grid(row=3, column=0, pady=5)

abstieg_label = ttk.Label(root, text="Abstieg")
abstieg_label.grid(row=4, column=0, pady=5)

zeit_label = ttk.Label(root, text="Zeit")
zeit_label.grid(row=5, column=0, pady=5)

delete_label = ttk.Label(root, text="ID")
delete_label.grid(row=7, column=0, pady=5)

### Eingabefelder ###

datum = ttk.Entry(root, width=80)
datum.grid(row=0, column=1, padx=10)

route = ttk.Entry(root, width=80)
route.grid(row=1, column=1)

kilometer = ttk.Entry(root, width=80)
kilometer.grid(row=2, column=1)

aufstieg = ttk.Entry(root, width=80)
aufstieg.grid(row=3, column=1)

abstieg = ttk.Entry(root, width=80)
abstieg.grid(row=4, column=1)

zeit = ttk.Entry(root, width=80)
zeit.grid(row=5, column=1)

delete_box = ttk.Entry(root, width=80)
delete_box.grid(row=7, column=1)

### Submit-Button ###
submit_button = ttk.Button(root, text="Fahrt hinzufügen", command=submit)
submit_button.grid(row=6, column=1, padx=9, pady=5, sticky="w")

### Delete-Button ###

delete_button = ttk.Button(root, text="Fahrt löschen", command=delete)
delete_button.grid(row=8, column=1, padx=9, pady=5, sticky="w")

### Query-Button ###
query_button = ttk.Button(root, text="Fahrten anzeigen", command=query)
query_button.grid(row=9, column=1, padx=9, pady=5, sticky="w")

## Alle Änderungen übernehmen und Verbindung schliessen
con.commit()
con.close()

## Loop ##
root.mainloop()
