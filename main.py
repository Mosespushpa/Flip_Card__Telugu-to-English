BACKGROUND_COLOR = "#B1DDC6"
from tkinter import *

import pandas
import random
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/Telugu_to_English.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card,flip_timer
    win.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    #print(current_card["Telugu"])
    canvas.itemconfig(card_title,text= "Telugu",fill="black")
    canvas.itemconfig(card_word,text= current_card["Telugu"],fill="black")
    canvas.itemconfig(card_background,image= card_front_img)
    flip_timer = win.after(3000,func=flip_card)

def flip_card():
    canvas.itemconfig(card_title,text= "English",fill= "white")
    canvas.itemconfig(card_word,text= current_card["English"],fill= "white")
    canvas.itemconfig(card_background,image= card_back_img)

def is_known():
    to_learn.remove(current_card)

    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv",index=False)
    next_card()
# ---------------------------- UI SETUP -------------------------------

win = Tk()
win.title("Flip Card")
win.config(padx=50,pady=50,background=BACKGROUND_COLOR) 

flip_timer = win.after(3000, func=flip_card)

canvas = Canvas(width=800,height=528)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="Word", font=("Ariel", 45, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0,columnspan=2)

cross_img = PhotoImage(file="images/wrong.png")
unknow_button = Button(image=cross_img,highlightthickness=0,command = next_card)
unknow_button.grid(row=1,column=0)

right_img = PhotoImage(file="images/right.png")
know_button = Button(image=right_img,highlightthickness=0,command = is_known)
know_button.grid(row=1,column=1)

next_card()

win.mainloop()
