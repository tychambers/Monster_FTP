from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from SQLConnectBox import ConnectBox
from ClientConnectionBox import client_connect_box
import os
from SFTP import SFTPClient
from FTP import Client
import datetime
from MessageBox import pop_up
import pandas as pd

# get time
time = datetime.datetime.now()

# SFTP, FTP and PostgreSQL objects
sftpclient = SFTPClient()
ftpclient = Client()
sql_box = ConnectBox()

root = Tk()
root.title("MonsterFTP")
root.iconbitmap(r"monster2.ico")
root.geometry("850x380")
root.configure(background="black")

title_label = Label(root, text="Monster FTP", font=("Arabic Transparent", 20, "bold"), background="black",
                    padx=5, fg="green")
title_label.grid(row=0, column=2, columnspan=3, sticky="NWS", pady=2)


def show_transactions():
    if sql_box.is_enabled:
        sql_box.cur.execute("SELECT * FROM transactions")
        results = sql_box.cur.fetchall()
        df = pd.DataFrame(results, columns=[desc[0] for desc in cur.description])
        df.to_csv("transactions.csv", index=False)
    else:
        pop_up("Not Connected to a DB, check DB settings")


saved_connections_button = Button(root, text="Export Transactions", command=show_transactions, bg="green", fg="black")
saved_connections_button.grid(row=3, column=5, sticky="NEWS", pady=2)

local_label = Label(root, text="Local Browser:", font=("Arabic Transparent", 16, "bold"), background="black",
                    padx=5, fg="green")
local_label.grid(row=2, column=0, sticky="NEWS", pady=2)

remote_label = Label(root, text="Remote Browser:", font=("Arabic Transparent", 16, "bold"), background="black",
                     padx=5, fg="green")
remote_label.grid(row=2, column=4, columnspan=2, sticky="W", pady=2)

# Local Browser TreeView
local_browser_tree = ttk.Treeview(root, columns=('Column 1', 'Column 2'),
                                  show='headings')
# Add column headings
local_browser_tree.heading('Column 1', text='Name')
local_browser_tree.heading('Column 2', text='Type')
local_browser_tree.column("Column 1")
local_browser_tree.column("Column 2")
# Pack the widget
local_browser_tree.grid(row=4, column=0, columnspan=3, sticky="NEWS", pady=2, padx=2)
# Treeview Vertical Scrollbar
local_browser_tree_scroll = ttk.Scrollbar(root, orient="vertical", command=local_browser_tree.yview)
local_browser_tree.configure(yscrollcommand=local_browser_tree_scroll.set)
local_browser_tree_scroll.grid(row=4, column=3, sticky="WNS", pady=2)

view_path_label = Label(root, text="Current Folder Path: ", background="black", padx=5, foreground="green")
view_path_label.grid(row=3, column=0, sticky="W", pady=2, padx=2)
view_path_entry = Entry(root, width=22)
view_path_entry.insert(0, "C:/")
view_path_entry.grid(row=3, column=1, sticky="W", pady=2)


def view_folder():
    local_browser_tree.delete(*local_browser_tree.get_children())
    listing = os.listdir(view_path_entry.get())
    folder_list = []
    file_list = []

    for item in listing:
        if "." not in item:
            folder_list.append(item)
        else:
            file_list.append(item)

    for folder in folder_list:
        local_browser_tree.insert('', 'end', values=(folder, "folder"))

    for file in file_list:
        local_browser_tree.insert('', 'end', values=(file, "file"))


view_folder()
view_path_button = Button(root, text="Update", background="green", foreground="black", command=view_folder)
view_path_button.grid(row=3, column=2, sticky="NEWS", pady=2, padx=2)


def back_out_folder():
    path = view_path_entry.get()
    folder_list = path.split("/")
    num_folders = len(folder_list) - 1

    new_path = ""
    for i in range(num_folders):
        new_path += folder_list[i] + "/"

    if new_path == "C:/":
        pass
    elif new_path[-1] == "/":
        new_path = new_path[:-1]

    view_path_entry.delete(0, END)
    view_path_entry.insert(0, new_path)
    view_folder()


up_arrow = PhotoImage(master=root, file='up_arrow.png')
up_arrow_button = Button(root, image=up_arrow, background="black", width=70, command=back_out_folder)
up_arrow_button.grid(row=5, column=0, sticky="NWS", pady=2, padx=2)


def enter_folder():
    current_item = local_browser_tree.focus()
    highlighted_row = local_browser_tree.item(current_item)
    folder = highlighted_row["values"][0]
    old_path = view_path_entry.get()
    if old_path[-1] == "/":
        new_path = old_path + folder
    else:
        new_path = old_path + "/" + folder
    view_path_entry.delete(0, END)
    view_path_entry.insert(0, new_path)
    view_folder()


down_arrow = PhotoImage(master=root, file='down_arrow.png')
down_arrow_button = Button(root, image=down_arrow, background="black", width=70, command=enter_folder)
down_arrow_button.grid(row=5, column=0, sticky="NES", pady=2, padx=2)

# Remote Browser TreeView
remote_browser_tree = ttk.Treeview(root, columns=('Column 1', 'Column 2'),
                                   show='headings')
# Add column headings
remote_browser_tree.heading('Column 1', text='Name')
remote_browser_tree.heading('Column 2', text='Type')
remote_browser_tree.column("Column 1")
remote_browser_tree.column("Column 2")
# Pack the widget
remote_browser_tree.grid(row=4, column=4, columnspan=3, sticky="NEWS", pady=2, padx=2)
# Treeview Vertical Scrollbar
remote_browser_tree_scroll = ttk.Scrollbar(root, orient="vertical", command=remote_browser_tree.yview)
remote_browser_tree.configure(yscrollcommand=remote_browser_tree_scroll.set)
remote_browser_tree_scroll.grid(row=4, column=7, sticky="NS", pady=2)


def start_connection():
    client_connect_box(ftpclient, sftpclient)
    if sftpclient.being_used:
        listing = sftpclient.client.listdir()
    else:
        listing = ftpclient.client.nlst()

    remote_browser_tree.delete(*remote_browser_tree.get_children())
    file_list = []
    folder_list = []
    for item in listing:
        if "." not in item:
            folder_list.append(item)
        else:
            file_list.append(item)

    for folder in folder_list:
        remote_browser_tree.insert('', 'end', values=(folder, "folder"))

    for file in file_list:
        remote_browser_tree.insert('', 'end', values=(file, "file"))


start_connection_button = Button(root, text="Start New Connection", command=start_connection, bg="green", fg="black")
start_connection_button.grid(row=3, column=4, sticky="NEWS", pady=2)


def update_treeview(path):
    remote_browser_tree.delete(*remote_browser_tree.get_children())
    if sftpclient.being_used:
        sftpclient.client.chdir(path)
        listing = sftpclient.client.listdir()
    else:
        ftpclient.client.cwd(path)
        listing = ftpclient.client.nlst()

    file_list = []
    folder_list = []
    for item in listing:
        if "." not in item:
            folder_list.append(item)
        else:
            file_list.append(item)

    for folder in folder_list:
        remote_browser_tree.insert('', 'end', values=(folder, "folder"))

    for file in file_list:
        remote_browser_tree.insert('', 'end', values=(file, "file"))


def remote_up_arrow_func():
    if sftpclient.being_used:
        path = sftpclient.client.getcwd()
    else:
        path = ftpclient.client.pwd()
    try:
        folder_list = path.split("/")
        num_folders = len(folder_list) - 1

        new_path = ""
        for i in range(num_folders):
            new_path += folder_list[i] + "/"

        update_treeview(new_path)
    except AttributeError:
        messagebox.showinfo("Select Folder", "Select a folder prior to clicking up arrow.")


remote_up_arrow = PhotoImage(master=root, file='up_arrow.png')
remote_up_arrow_button = Button(root, image=remote_up_arrow, background="black", width=70, command=remote_up_arrow_func)
remote_up_arrow_button.grid(row=5, column=4, sticky="NWS", pady=2, padx=2)


def remote_down_arrow_func():
    current_item = remote_browser_tree.focus()
    highlighted_row = remote_browser_tree.item(current_item)
    if sftpclient.being_used:
        try:
            folder = highlighted_row["values"][0]
            old_path = sftpclient.client.getcwd()
            if old_path:
                new_path = old_path + "/" + folder
            else:
                new_path = "/" + folder
            update_treeview(new_path)
        except IndexError:
            messagebox.showinfo("Select Folder", "Select a folder prior to clicking down arrow.")
    else:
        try:
            folder = highlighted_row["values"][0]
            old_path = ftpclient.client.pwd()
            if old_path == "/":
                new_path = old_path + folder
            else:
                new_path = old_path + "/" + folder
            update_treeview(new_path)
        except IndexError:
            messagebox.showinfo("Select Folder", "Select a folder prior to clicking down arrow.")


remote_down_arrow = PhotoImage(master=root, file='down_arrow.png')
remote_down_arrow_button = Button(root, image=remote_down_arrow, background="black", width=70,
                                  command=remote_down_arrow_func)
remote_down_arrow_button.grid(row=5, column=4, sticky="NES", pady=2, padx=2)


def upload():
    current_item = local_browser_tree.focus()
    highlighted_row = local_browser_tree.item(current_item)
    file_name = highlighted_row["values"][0]
    local_path = view_path_entry.get()
    if sftpclient.being_used:
        if local_path[-1] == "/":
            local_path = local_path + file_name
        else:
            local_path = local_path + "/" + file_name
        current_dir = sftpclient.client.getcwd()
        if current_dir:
            remote_path = current_dir + "/" + file_name
        else:
            remote_path = "/" + file_name
        sftpclient.client.put(local_path, remote_path)
        update_treeview(current_dir)

        if sql_box.is_enabled:
            query = f'''
                       INSERT INTO transactions (protocol, transaction_type, source_path, dest_path, time)
                       VALUES('SFTP', 'Upload', '{local_path}', '{remote_path}', '{time}')
                       '''
            sql_box.cur.execute(query)
            sql_box.conn.commit()
    else:
        if local_path[-1] == "/":
            local_path = local_path + file_name
        else:
            local_path = local_path + "/" + file_name
        with open(local_path, 'rb') as file:
            ftpclient.client.storbinary(f'STOR {file_name}', file)
        path = ftpclient.client.pwd()
        update_treeview(path)

        if sql_box.is_enabled:
            query = f'''
                       INSERT INTO transactions (protocol, transaction_type, source_path, dest_path, time)
                       VALUES('FTP', 'Download', '{local_path}', '{path}', '{time}')
                       '''
            sql_box.cur.execute(query)
            sql_box.conn.commit()


upload_button = Button(root, text="Upload", background="green", foreground="black",
                       command=upload)
upload_button.grid(row=5, column=1, sticky="NEWS", pady=2, padx=2)


def download():
    current_item = remote_browser_tree.focus()
    highlighted_row = remote_browser_tree.item(current_item)
    file_name = highlighted_row["values"][0]
    local_path = view_path_entry.get()
    if sftpclient.being_used:
        current_dir = sftpclient.client.getcwd()
        if current_dir:
            remote_path = current_dir + "/" + file_name
            if local_path[-1] == "/":
                local_path = local_path + file_name
            else:
                local_path = local_path + "/" + file_name
            sftpclient.client.get(remote_path, local_path)

            if sql_box.is_enabled:
                query = f'''
                INSERT INTO transactions (protocol, transaction_type, source_path, dest_path, time)
                VALUES('SFTP', 'Download', '{local_path}', '{remote_path}', '{time}')
                '''
                sql_box.cur.execute(query)
                sql_box.conn.commit()
        else:
            remote_path = "/" + file_name
            if local_path[-1] == "/":
                local_path = local_path + file_name
            else:
                local_path = local_path + "/" + file_name
            sftpclient.client.get(remote_path, local_path)

            if sql_box.is_enabled:
                query = f'''
                           INSERT INTO transactions (protocol, transaction_type, source_path, dest_path, time)
                           VALUES('SFTP', 'Download', '{local_path}', '{remote_path}', '{time}')
                           '''
                sql_box.cur.execute(query)
                sql_box.conn.commit()
    else:
        if local_path[-1] == "/":
            local_path = local_path + file_name
        else:
            local_path = local_path + "/" + file_name
        with open(local_path, "wb") as file:
            ftpclient.client.retrbinary(f"RETR {file_name}", file.write)
            remote_path = ftpclient.client.pwd()
            if sql_box.is_enabled:
                query = f'''
                           INSERT INTO transactions (protocol, transaction_type, source_path, dest_path, time)
                           VALUES('FTP', 'Download', '{local_path}', '{remote_path}', '{time}')
                           '''
                sql_box.cur.execute(query)
                sql_box.conn.commit()

    view_folder()


download_button = Button(root, text="Download", background="green", foreground="black",
                         command=download)
download_button.grid(row=5, column=5, sticky="NEWS", pady=2, padx=2)


def db_func():
    sql_box.box()


db_button = Button(root, text="DB settings", background="green", foreground="black",
                   command=db_func)
db_button.grid(row=3, column=6, sticky="NEWS", pady=2, padx=2)


root.mainloop()
