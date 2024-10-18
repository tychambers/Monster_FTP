from tkinter import *
from PIL import Image, ImageTk


def pop_up(resp):
    message_box = Tk()
    message_box.title("Monster FTP")
    message_box.iconbitmap(r"monster2.ico")
    message_box.geometry("300x125")
    message_box.configure(background="black")
    message_box.focus_force()

    if resp == "Success":
        message_box.title("Connection Successful")
        success_label = Label(message_box, text=f"Connection Successful!", wraplength=200, background="black", padx=5,
                              foreground="green")
        success_label.grid(row=1, column=1, columnspan=4, sticky="NEWS")
    else:
        error_label = Label(message_box, text=f"{resp}", wraplength=200, background="black", padx=5,
                            foreground="green")
        error_label.grid(row=1, column=1, columnspan=4, sticky="NEWS")

    def destroy():
        message_box.withdraw()
        message_box.quit()

    image = Image.open("dead_zombie.png")

    # Convert the image to a Tkinter-compatible format
    photo = ImageTk.PhotoImage(master=message_box, image=image, height=1, width=1)

    # Create a label to display the image
    image_label = Label(message_box, image=photo)
    image_label.grid(row=1, column=0, sticky="NEWS", pady=10, padx=10)

    okay = Button(message_box, text="Continue", command=destroy, width=10, bg="black", fg="green")
    okay.grid(row=2, column=2, sticky="NEWS", pady=2, padx=5)

    message_box.mainloop()
