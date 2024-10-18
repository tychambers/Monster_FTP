from tkinter import *

import pandas as pd


class PathBox:
    def __init__(self):
        self.path = ''

    def path_box(self, sql_box):
        message_box = Tk()
        message_box.title("Monster FTP")
        message_box.iconbitmap(r"monster2.ico")
        message_box.geometry("280x60")
        message_box.configure(background="black")
        message_box.focus_force()

        location_label = Label(message_box, text="Enter Location for File:", background="black", padx=5,
                               foreground="green")
        location_label.grid(row=0, column=0, sticky="W", pady=2, padx=2)
        location_entry = Entry(message_box, width=22)
        location_entry.insert(0, "C:/test/transactions.csv")
        location_entry.grid(row=0, column=1, columnspan=2, sticky="W", pady=2)

        def destroy():
            sqlbox = sql_box
            sqlbox.cur.execute("SELECT * FROM transactions")
            results = sqlbox.cur.fetchall()
            df = pd.DataFrame(results, columns=[desc[0] for desc in sql_box.cur.description])
            df.to_csv(location_entry.get(), index=False)
            message_box.withdraw()

        generate = Button(message_box, text="Generate CSV", command=destroy, bg="green", fg="black")
        generate.grid(row=1, column=0, columnspan=2, sticky="NEWS", pady=2, padx=5)