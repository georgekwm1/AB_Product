from engine import SQLiteEngine
import sqlite3 as sql
import tkinter as tk
import pandas as pd

YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
#--------------DATABASE CONNECTION------------------------------
db_name = "jireh_database.db"
connection = sql.connect(db_name)
db = SQLiteEngine(db_name)
#db.update_rate(3000)
db.recreate_table()
#(db.listtables())
#db.search()
#--------------FUNCTIONS----------------------------------------
def search_item():
    search_query = search_entry.get()
    results = db.search(search_query) 
    #Convert to  DataFrame and display in table
    df = pd.DataFrame(results, columns=["ID","Product Name", "resolution", "model", "specification", "usd_per_set", "Unit Cost in Naira", "Unit Shipment Cost", "Total Cost in Naira", "Reseller Markup 15%", "TSI Markup 15%", "End User Markup 35%", "T-19rs", "T-21rs", "T-23rs", "Sunday Onu Silver", "Silver DP","Bronze DP", "Platinum DP", "Reseller Price", "TSI Price", "7.4% ns RP", "EU Price"])
    if not results:
        return
    else:
        text_area.insert(tk.END, f"{df}\n")
        #search_output["text"] = f"{df}"

def convert_rate():
    rate = rate_entry.get()
    db.update_rate(rate, connection)
    output_label["text"] = "Check the export folder for the file with updated rates"
#-------------UI SETUP----------------------------------------
#Window
window = tk.Tk()
window.title('JiReH')
window.config(padx=20, pady=20, bg = YELLOW)
window.minsize(width=800, height=300)
window.iconbitmap('./jireh_logo.ico')

#Canvas
canvas = tk.Canvas(width=713, height=88, bg=YELLOW, highlightthickness=0)
picture = tk.PhotoImage(file="./jireh_resize.png")
canvas.create_image(356, 44, image=picture)
canvas.grid(column=0, row=0, columnspan=4)

#Labels
title_label = tk.Label(text="Search Table", font=(FONT_NAME, 14, "bold"), bg=YELLOW)
title_label.grid(column=1, row=1)
output_label = tk.Label(text="", font=(FONT_NAME, 14, "bold"), bg=YELLOW)
output_label.grid(column=1, row=6)
#search_output = tk.Label(text="", font=(FONT_NAME, 14, "bold"), bg=YELLOW)
#search_output.grid(column=1, row=3)

#Entry
search_entry = tk.Entry(width=20, font=(FONT_NAME, 14), bg="white")
search_entry.grid(column=1, row=2)

rate_entry = tk.Entry(width=20, font=(FONT_NAME, 14), bg="white")
rate_entry.grid(column=1, row=5)
#Button
search_button = tk.Button(text="Search", width=5, height=0, font=(FONT_NAME, 14), bg="white", command= search_item)
search_button.grid(column=2, row=2)

convert_button = tk.Button(text="Covert", width=5, height=0, font=(FONT_NAME, 14), bg="white", command= convert_rate)
convert_button.grid(column=2, row=5)

#Text Area
text_area = tk.Text()
text_area.grid(column=1, row=3)


window.mainloop()