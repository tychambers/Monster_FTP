from tkinter import *
from tkinter import filedialog
from SFTP import SFTPClient
from MessageBox import pop_up


def ssh_options(sftpclient):
    root = Tk()
    sftp_client = sftpclient

    root.title("SSH Settins")
    root.iconbitmap(r"monster2.ico")
    root.geometry("400x150")
    root.configure(background="black")

    title_label = Label(root, text="SSH Key Settings", font=("Arabic Transparent", 16, "bold"), background="black",
                        padx=5, fg="green")
    title_label.grid(row=0, column=0, columnspan=3, sticky="NEWS", pady=2)

    # private key label and entry
    pk_label = Label(root, text="Private Key Path: ", background="black", padx=5, foreground="green")
    pk_label.grid(row=1, column=0, sticky="W", pady=2, padx=2)
    pk_entry = Entry(root, width=35)
    pk_entry.insert(0, sftp_client.pk_path)
    pk_entry.grid(row=1, column=1, columnspan=2, sticky="W", pady=2)

    def browse_files():
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("all files", "*.*"),
                                                                                                ("Text files", "*.txt*")))
        pk_entry.delete(0, END)
        pk_entry.insert(0, filename)

    # folder icon
    click_btn = PhotoImage(master=root, file='green_folder.png')
    # img_label = Label(image=click_btn)
    folder_button = Button(root, image=click_btn, command=browse_files, background="black")
    folder_button.grid(row=1, column=3, columnspan=2, sticky="W", pady=2, padx=2)

    # private key password
    pk_pw_label = Label(root, text="Private Key Password: ", background="black", padx=5, foreground="green")
    pk_pw_label.grid(row=2, column=0, sticky="W", pady=2, padx=2)
    pk_pw_entry = Entry(root, width=35)
    pk_pw_entry.insert(0, sftp_client.pk_password)
    pk_pw_entry.config(show='*')
    pk_pw_entry.grid(row=2, column=1, columnspan=2, sticky="W", pady=2)

    def set_key():
        return_list = sftp_client.set_private_key(pk_entry.get(), pk_pw_entry.get())
        if return_list[0] == "" and return_list[1] == "":
            pop_up("Missing Path and Password")
        elif return_list[0] == "":
            pop_up("Missing Path")
        elif return_list[1] == "":
            pop_up("Missing Password")
        else:
            root.withdraw()
            root.quit()
            # root.destroy()

    ok_button = Button(root, text="OK", background="green", foreground="black", command=set_key)
    ok_button.grid(row=3, column=1, sticky="NEWS", pady=2, padx=2)

    def cancel():
        root.destroy()

    cancel_button = Button(root, text="Cancel", background="green", foreground="black", command=cancel)
    cancel_button.grid(row=3, column=2, sticky="NEWS", pady=2, padx=2)

    root.mainloop()
