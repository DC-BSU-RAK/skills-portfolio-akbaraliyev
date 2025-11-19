from tkinter import *
from PIL import Image, ImageTk
import random

with open("randomJokes.txt", "r") as f:
    lines = f.readlines()

jokes = [line.strip() for line in lines if "?" in line]

current_setup = ""
current_answer = ""

def newJoke():
    global current_setup, current_answer

    joke = random.choice(jokes)
    parts = joke.split("?")

    current_setup = parts[0] + "?"
    current_answer = parts[1]

    setup_label.config(text=current_setup)
    answer_label.config(text="")

def showAnswer():
    answer_label.config(text=current_answer)

def quitApp():
    root.destroy()

root = Tk()
root.title("Alexa Tell Me a Joke")
root.geometry("1300x700")
root.config(bg="#C0C0C0")
root.iconphoto(True, ImageTk.PhotoImage(file="img/icon.png"))

title_label = Label(root, text="Alexa Tell Me a Joke", font=("Terminal", 40, "bold"), bg="#C0C0C0", fg="black")
title_label.pack(pady=30)

setup_label = Label(root, text="", font=("Terminal", 30), bg="#C0C0C0", fg="#0c840e", wraplength=1100, justify="center")
setup_label.pack(pady=40)

answer_label = Label(root, text="", font=("Terminal", 26), bg="#C0C0C0", fg="red", wraplength=1100, justify="center")
answer_label.pack(pady="20")

def load_button(path,size):
    img = Image.open(path)
    img = img.resize(size)
    return ImageTk.PhotoImage(img)

button_size = (328, 71)

alexa_img = load_button("img/alexa.png", button_size)
answer_img = load_button("img/show_answer.png", button_size)
next_img = load_button("img/next.png", button_size)
quit_img = load_button("img/quit.png", button_size)

btn_frame = Frame(root, bg="#C0C0C0")
btn_frame.pack(pady=50)

alexa_btn = Button(btn_frame, image=alexa_img, command=newJoke, borderwidth=0, highlightthickness=0, bg="#C0C0C0")
alexa_btn.grid(row=0, column=0, padx=30, pady=20)

answer_btn = Button(btn_frame, image=answer_img, command=showAnswer, borderwidth=0, highlightthickness=0, bg="#C0C0C0")
answer_btn.grid(row=0, column=1, padx=30, pady=20)

next_btn = Button(btn_frame, image=next_img, command=newJoke, borderwidth=0, highlightthickness=0, bg="#C0C0C0")
next_btn.grid(row=1, column=0, padx=30, pady=20)

quit_btn = Button(btn_frame, image=quit_img, command=quitApp, borderwidth=0, highlightthickness=0, bg="#C0C0C0")
quit_btn.grid(row=1, column=1, padx=30, pady=20)

root.mainloop()