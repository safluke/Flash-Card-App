import tkinter as tk
import pandas
from pandas.errors import EmptyDataError
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
FONT_NAME = "Arial"
current_word = {}
dict_from_csv=[]


try:
    data= pandas.read_csv('words_to_learn.csv')
    
except FileNotFoundError:
    original_data=pandas.read_csv('french_words.csv')
    dict_from_csv=original_data.to_dict(orient="records")   
    
except EmptyDataError:
    os.remove('words_to_learn.csv')
    original_data=pandas.read_csv('french_words.csv')
    dict_from_csv=original_data.to_dict(orient="records")   
else:
    dict_from_csv = data.to_dict(orient="records")
    

    
def Next_Card():
    global current_word, flip_timer, dict_from_csv, original_data
    window.after_cancel(flip_timer)
    

    current_word=random.choice(dict_from_csv)
      
    try:
        canvas.itemconfig(language_text,text=data.columns[0], fill="Black")
    except NameError:
        canvas.itemconfig(language_text,text=original_data.columns[0], fill="Black")
    canvas.itemconfig(word_text,text=current_word.get("French"), fill="Black")
    canvas.itemconfig(card_background, image=flash_image)
    
    flip_timer=window.after(3000, func=Flip_Card)
    
    
def Flip_Card():
    
    try:
        canvas.itemconfig(language_text,text=data.columns[1], fill="White")
    except NameError:
        canvas.itemconfig(language_text,text=original_data.columns[1], fill="White")
    canvas.itemconfig(word_text,text=current_word.get("English"), fill= "White")
    canvas.itemconfig(card_background, image=flash2_image)
    
def Is_Known():
    
    dict_from_csv.remove(current_word)
    data=pandas.DataFrame(dict_from_csv)
    data.to_csv("words_to_learn.csv", index=False)
    canvas.itemconfig(counter_text,text=len(dict_from_csv),fill="black", font=(FONT_NAME,20,"bold"))
    if len(dict_from_csv)>0:
        Next_Card()
    else:
        window.after_cancel(flip_timer)
        canvas.itemconfig(language_text, fill="White")
        canvas.itemconfig(word_text,text="Congratulations!\nReset to \nstart again.", fill="Black")   

    

def Reset():
    global dict_from_csv, original_data
    try:
        os.remove('words_to_learn.csv')
    except:
        pass
    finally:
        
        original_data=pandas.read_csv('french_words.csv')
        dict_from_csv=original_data.to_dict(orient="records")      
        canvas.itemconfig(counter_text,text=len(dict_from_csv),fill="black", font=(FONT_NAME,20,"bold"))
        Next_Card()
    
window=tk.Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg= BACKGROUND_COLOR)




flip_timer=window.after(3000, func=Flip_Card)

canvas=tk.Canvas(width= 800, height = 526,highlightthickness=0, bg=BACKGROUND_COLOR)
flash_image= tk.PhotoImage(file="card_front.png")
flash2_image= tk.PhotoImage(file="card_back.png")
card_background=canvas.create_image(400,263, image=flash_image)



language_text=canvas.create_text(400,150,text="", fill="black", font=(FONT_NAME,60,"italic"))

word_text=canvas.create_text(400,263,text="", fill="black", font=(FONT_NAME,60,"bold"))

counter_text=canvas.create_text(700,450,text=len(dict_from_csv),fill="black", font=(FONT_NAME,20,"bold"))

canvas.grid(column=1, row=0, columnspan=3)


#Buttons
tick_image=tk.PhotoImage(file="right.png")
cross_image=tk.PhotoImage(file="wrong.png")
reset_image=tk.PhotoImage(file="reset.png")
#tick button
tick_button = tk.Button(image = tick_image, highlightthickness=0, command=Is_Known)
tick_button.grid(column=2, row=3)
#cross button
cross_button = tk.Button(image = cross_image, highlightthickness=0, command=Next_Card)
cross_button.grid(column=1, row=3)
#reset button
cross_button = tk.Button(image = reset_image, highlightthickness=0, command=Reset, bg=BACKGROUND_COLOR)
cross_button.grid(column=3, row=3)

Next_Card()

window.mainloop()
