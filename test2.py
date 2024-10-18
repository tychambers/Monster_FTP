from tkinter import *
import customtkinter as ctk
from FTP import Client
from MessageBox import pop_up
from SFTPKeyBox import ssh_options
from SFTP import SFTPClient


def client_connect_box():
    # declaring global variables for destroying widgets loop later when switching between SFTP/FTP
    # otherwise the widgets will stack on each other
    global ftp_host_label
    global ftp_host_entry
    global ftp_port_label
    global ftp_port_entry
    global ftp_un_label
    global ftp_pw_label
    global ftp_un_entry
    global ftp_pw_entry
    global connect
    global sftp_host_label
    global sftp_host_entry
    global sftp_port_label
    global sftp_port_entry
    global sftp_un_label
    global sftp_pw_label
    global sftp_un_entry
    global sftp_pw_entry
    global key_label
    global key_button

    root = Tk()
    root.title("Connection Profile")
    root.iconbitmap(r"monster2.ico")
    root.geometry("290x235")
    root.configure(background="black")

    title_label = Label(root, text="Create A Connection", font=("Arabic Transparent", 20, "bold"), background="black",
                        padx=5, fg="green")
    title_label.grid(row=0, column=0, columnspan=3, sticky="NEWS", pady=2)

    connection_label = Label(root, text="Connection Type: ", background="black", padx=5, foreground="green")
    connection_label.grid(row=1, column=0, sticky="W", pady=2, padx=2)

    # custom dropdown button using ctk module
    connection_types = ["FTP", "SFTP"]
    connection_type_dropdown = ctk.StringVar()
    connection_type_dropdown.set("Select Value")

    def choose_connection(self):
        global ftp_host_label
        global ftp_host_entry
        global ftp_port_label
        global ftp_port_entry
        global ftp_un_label
        global ftp_pw_label
        global ftp_un_entry
        global ftp_pw_entry
        global connect
        global sftp_host_label
        global sftp_host_entry
        global sftp_port_label
        global sftp_port_entry
        global sftp_un_label
        global sftp_pw_label
        global sftp_un_entry
        global sftp_pw_entry
        global key_label
        global key_button
        # global key_path
        # global key_password

        if self == "FTP":
            try:
                # deletes previous entries if they are there
                sftp_host_label.destroy()
                sftp_host_entry.destroy()
                sftp_port_label.destroy()
                sftp_port_entry.destroy()
                sftp_un_label.destroy()
                sftp_pw_label.destroy()
                sftp_un_entry.destroy()
                sftp_pw_entry.destroy()
                key_label.destroy()
                key_button.destroy()
                connect.destroy()
            except NameError:
                pass

            ftp_host_label = Label(root, text="Host Address: ", background="black", padx=5, foreground="green")
            ftp_host_label.grid(row=2, column=0, sticky="W", pady=2, padx=2)
            ftp_host_entry = Entry(root, width=22)
            ftp_host_entry.insert(0, "localhost")
            ftp_host_entry.grid(row=2, column=1, columnspan=2, sticky="W", pady=2)

            ftp_port_label = Label(root, text="Port: ", background="black", padx=5, foreground="green")
            ftp_port_label.grid(row=3, column=0, sticky="W", pady=2, padx=2)
            ftp_port_entry = Entry(root, width=4)
            ftp_port_entry.insert(0, "21")
            ftp_port_entry.grid(row=3, column=1, columnspan=2, sticky="W", pady=2)

            ftp_un_label = Label(root, text="Username: ", background="black", padx=5, foreground="green")
            ftp_un_label.grid(row=4, column=0, sticky="W", pady=2, padx=2)
            ftp_un_entry = Entry(root, width=22)
            ftp_un_entry.insert(0, "Username")
            ftp_un_entry.grid(row=4, column=1, columnspan=2, sticky="W", pady=2)

            ftp_pw_label = Label(root, text="Password: ", background="black", padx=5, foreground="green")
            ftp_pw_label.grid(row=5, column=0, sticky="W", pady=2, padx=2)
            ftp_pw_entry = Entry(root, width=22)
            ftp_pw_entry.insert(0, "Password")
            ftp_pw_entry.config(show='*')
            ftp_pw_entry.grid(row=5, column=1, columnspan=2, sticky="W", pady=2)

            def ftp_connect():
                client = Client()

                host = ftp_host_entry.get()
                port = int(ftp_port_entry.get())
                username = ftp_un_entry.get()
                password = ftp_pw_entry.get()

                connection_code = client.connect(host, port, username, password)
                pop_up(connection_code)

            connect = Button(root, text="Connect", command=ftp_connect, bg="black", fg="green")
            connect.grid(row=6, column=0, columnspan=3, sticky="NEWS", pady=2, padx=5)

        else:
            try:
                # destroy unused widgets if needed
                ftp_host_label.destroy()
                ftp_host_entry.destroy()
                ftp_port_label.destroy()
                ftp_port_entry.destroy()
                ftp_un_label.destroy()
                ftp_pw_label.destroy()
                ftp_un_entry.destroy()
                ftp_pw_entry.destroy()
                connect.destroy()

            except NameError:
                pass

            sftp_host_label = Label(root, text="Host Address: ", background="black", padx=5, foreground="green")
            sftp_host_label.grid(row=2, column=0, sticky="W", pady=2, padx=2)
            sftp_host_entry = Entry(root, width=22)
            sftp_host_entry.insert(0, "localhost")
            sftp_host_entry.grid(row=2, column=1, columnspan=2, sticky="W", pady=2)

            sftp_port_label = Label(root, text="Port: ", background="black", padx=5, foreground="green")
            sftp_port_label.grid(row=3, column=0, sticky="W", pady=2, padx=2)
            sftp_port_entry = Entry(root, width=4)
            sftp_port_entry.insert(0, "22")
            sftp_port_entry.grid(row=3, column=1, columnspan=2, sticky="W", pady=2)

            sftp_un_label = Label(root, text="Username: ", background="black", padx=5, foreground="green")
            sftp_un_label.grid(row=4, column=0, sticky="W", pady=2, padx=2)
            sftp_un_entry = Entry(root, width=22)
            sftp_un_entry.insert(0, "Username")
            sftp_un_entry.grid(row=4, column=1, columnspan=2, sticky="W", pady=2)

            sftp_pw_label = Label(root, text="Password: ", background="black", padx=5, foreground="green")
            sftp_pw_label.grid(row=5, column=0, sticky="W", pady=2, padx=2)
            sftp_pw_entry = Entry(root, width=22)
            sftp_pw_entry.insert(0, "Password")
            sftp_pw_entry.config(show='*')
            sftp_pw_entry.grid(row=5, column=1, columnspan=2, sticky="W", pady=2)

            key_label = Label(root, text="Key Auth: ", background="black", padx=5, foreground="green")
            key_label.grid(row=6, column=0, sticky="W", pady=2, padx=2)

            sftpclient = SFTPClient()

            def key_box():
                if sftpclient.path == "":
                    ssh_options(sftpclient)
                else:
                    ssh_options(sftpclient)

            key_button = Button(root, text="Configure", command=key_box, bg="green", fg="black")
            key_button.grid(row=6, column=1, columnspan=2, sticky="NEWS", pady=2)

            def sftp_connect():
                client = Client()

                host = ftp_host_entry.get()
                port = int(ftp_port_entry.get())
                username = ftp_un_entry.get()
                password = ftp_pw_entry.get()

                connection_code = client.connect(host, port, username, password)
                pop_up(connection_code)

            connect = Button(root, text="Connect", command=sftp_connect, bg="black", fg="green")
            connect.grid(row=7, column=0, columnspan=3, sticky="NEWS", pady=2, padx=5)

    custom_dropdown = ctk.CTkOptionMenu(root, variable=connection_type_dropdown, values=connection_types, bg_color="black",
                                        fg_color="green", text_color="black", button_color="green",
                                        dropdown_fg_color="green", dropdown_hover_color="cyan", width=50,
                                        command=choose_connection)
    custom_dropdown.grid(row=1, column=2, sticky="NWS", pady=2)

    root.mainloop()
