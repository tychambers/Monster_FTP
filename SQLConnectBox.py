from tkinter import *
import psycopg2
from MessageBox import pop_up
import customtkinter as ctk


class ConnectBox:
    def __init__(self):
        self.is_enabled = False
        self.cur = ""
        self.conn = ""
        self.host = ""
        self.dbname = ""
        self.user = ""
        self.password = ""
        self.port = ""

    def box(self):
        root = Tk()
        root.title("Connect to DB")
        root.iconbitmap(r"monster2.ico")
        root.geometry("290x260")
        root.configure(background="black")

        title_label = Label(root, text="Connect to Database", font=("Arabic Transparent", 20, "bold"), background="black",
                            padx=5, fg="green")
        title_label.grid(row=0, column=0, columnspan=3, sticky="NEWS", pady=2)

        db_settings_label = Label(root, text="Choose DB logging: ", background="black", padx=5, foreground="green")
        db_settings_label.grid(row=1, column=0, sticky="W", pady=2, padx=2)

        def choose_db(choice):
            if choice == "PostgreSQL":
                host_label = Label(root, text="Host Address: ", background="black", padx=5, foreground="green")
                host_label.grid(row=2, column=0, sticky="W", pady=2, padx=2)
                host_entry = Entry(root, width=22)
                if self.is_enabled:
                    host_entry.insert(0, self.host)
                else:
                    host_entry.insert(0, "localhost")
                host_entry.grid(row=2, column=1, columnspan=2, sticky="W", pady=2)

                port_label = Label(root, text="Port: ", background="black", padx=5, foreground="green")
                port_label.grid(row=3, column=0, sticky="W", pady=2, padx=2)
                port_entry = Entry(root, width=22)
                if self.is_enabled:
                    port_entry.insert(0, self.port)
                else:
                    port_entry.insert(0, "5432")
                port_entry.grid(row=3, column=1, columnspan=2, sticky="W", pady=2)

                db_label = Label(root, text="Database Name: ", background="black", padx=5, foreground="green")
                db_label.grid(row=4, column=0, sticky="W", pady=2, padx=2)
                db_entry = Entry(root, width=22)
                if self.is_enabled:
                    db_entry.insert(0, self.dbname)
                else:
                    db_entry.insert(0, "ftpdb")
                db_entry.grid(row=4, column=1, columnspan=2, sticky="W", pady=2)

                un_label = Label(root, text="Username: ", background="black", padx=5, foreground="green")
                un_label.grid(row=5, column=0, sticky="W", pady=2, padx=2)
                un_entry = Entry(root, width=22)
                if self.is_enabled:
                    un_entry.insert(0, self.user)
                else:
                    un_entry.insert(0, "postgres")
                un_entry.grid(row=5, column=1, columnspan=2, sticky="W", pady=2)

                pw_label = Label(root, text="Password: ", background="black", padx=5, foreground="green")
                pw_label.grid(row=6, column=0, sticky="W", pady=2, padx=2)
                pw_entry = Entry(root, width=22)
                if self.is_enabled:
                    pw_entry.insert(0, self.password)
                else:
                    pw_entry.insert(0, "Admin123!!!")
                pw_entry.config(show='*')
                pw_entry.grid(row=6, column=1, columnspan=2, sticky="W", pady=2)

                status_label = Label(root, text="Status: ", background="black", padx=5, foreground="green")
                status_label.grid(row=7, column=0, sticky="W", pady=2, padx=2)
                if self.is_enabled:
                    status = Label(root, text="Connected", background="black", padx=5, foreground="green")
                else:
                    status = Label(root, text="Not Connected ", background="black", padx=5, foreground="red")
                status.grid(row=7, column=1, columnspan=2, sticky="W", pady=2)

                def connect_to_db():
                    try:
                        conn = psycopg2.connect(host=host_entry.get(), dbname=db_entry.get(), user=un_entry.get(),
                                                password=pw_entry.get(), port=port_entry.get())
                        pop_up("Successfully Connected to DB")
                        cur = conn.cursor()
                        self.host = host_entry.get()
                        self.dbname = db_entry.get()
                        self.user = un_entry.get()
                        self.password = pw_entry.get()
                        self.port = port_entry.get()
                        self.cur = cur
                        self.conn = conn
                        self.is_enabled = True
                        query = '''
                                CREATE TABLE IF NOT EXISTS transactions (
                                protocol VARCHAR(255) NOT NULL,
                                transaction_type VARCHAR(255) NOT NULL,
                                source_path VARCHAR(255) NOT NULL,
                                dest_path VARCHAR(255) NOT NULL,
                                time VARCHAR(255) NOT NULL
                                )'''

                        cur.execute(query)
                        conn.commit()
                        root.withdraw()
                        root.quit()
                    except psycopg2.OperationalError as error:
                        error_message = str(error)
                        pop_up(error_message)
                connect = Button(root, text="Connect", command=connect_to_db, bg="green", fg="black")
                connect.grid(row=8, column=0, columnspan=3, sticky="NEWS", pady=2, padx=5)
            else:
                pass

        db_settings = ["off", "PostgreSQL"]
        db_settings_dropdown = ctk.StringVar()

        if self.is_enabled:
            db_settings_dropdown.set("PostgreSQL")
            choose_db("PostgreSQL")
        else:
            db_settings_dropdown.set("off")
        custom_dropdown = ctk.CTkOptionMenu(root, variable=db_settings_dropdown, values=db_settings,
                                            bg_color="black",
                                            fg_color="green", text_color="black", button_color="green",
                                            dropdown_fg_color="green", dropdown_hover_color="cyan", width=50,
                                            command=choose_db)
        custom_dropdown.grid(row=1, column=1, sticky="NWS", pady=2)

        root.mainloop()



