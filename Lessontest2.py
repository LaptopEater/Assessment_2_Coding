from tkinter import *
from PIL import Image, ImageTk
import requests
from io import BytesIO

root = Tk()
root.title("Cocktail App")
root.geometry("1000x600")
root.resizable(0,0)
root["bg"] = "black"

drinks = {}

def show(drink):
    drinkname.config(text=drink["strDrink"])

    ing_list = []
    for i in range(1, 6):
        ing = drink.get(f"strIngredient{i}")
        if ing:
            ing_list.append(ing)
    ingredients.config(text="Ingredients:\n" + ", ".join(ing_list))
    
    instructions.config(text="Instructions:\n" + drink["strInstructions"])
    
    img_url = drink["strDrinkThumb"]
    img_data = requests.get(img_url).content
    img = Image.open(BytesIO(img_data)).resize((150,150))
    img = ImageTk.PhotoImage(img)
    drinkimage.config(image=img)
    drinkimage.image = img
    drinkimage.place(x=750, y=50)

def randomdrink():
    url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    data = requests.get(url).json()
    drink = data["drinks"][0]
    show(drink)

def searchdrink():
    name = search.get()
    if name.strip() == "":
        return
    url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?s={name}"
    data = requests.get(url).json()
    if data["drinks"]:
        drink = data["drinks"][0]
        show(drink)

def viewall():
    listbox.delete(0, END)
    drinks.clear()
    
    for letter in "abcdefghijklmnopqrstuvwxyz":
        url = f"https://www.thecocktaildb.com/api/json/v1/1/search.php?f={letter}"
        data = requests.get(url).json()
        if data["drinks"]:
            for drink in data["drinks"]:
                name = drink["strDrink"]
                drinks[name] = drink
                listbox.insert(END, name)

def selectdrink(event):
    selection = listbox.curselection()
    if selection:
        name = listbox.get(selection[0])
        drink = drinks[name]
        show(drink)

gif = Image.open("Advanced Programming//1A-S1M.gif")  
frames = []
try:
    while True:
        frames.append(ImageTk.PhotoImage(gif.copy().resize((500,200))))
        gif.seek(len(frames))
except EOFError:
    pass
bartender = Label(root, bg="black",width=500)
bartender.place(x=400, y=400)  
def play(i=0):
    frame = frames[i % len(frames)]
    bartender.config(image=frame)
    root.after(100, play, i+1)

drinkname = Label(root, text="", bg='black', fg="#e8a000", font=("Roboto", 20,'bold'))
drinkname.place(x=400, y=20)

ingredients = Label(root, text="Ingredients:", bg='black', fg='white',wraplength=500, justify=LEFT)
ingredients.place(x=400, y=80)

instructions = Label(root, text="Instructions:", bg='black', fg='white', wraplength=500, justify=LEFT)
instructions.place(x=400, y=200)

drinkimage = Label(root, bg="black")
drinkimage.place(x=750, y=20)  

search = Entry(root, font=("Roboto", 14), width=20)
search.place(x=10, y=320)

frame = Frame(root, bg="black")
frame.place(x=10, y=400)
scroll = Scrollbar(frame, orient="vertical")
scroll.pack(side=RIGHT, fill=Y)

listbox = Listbox(frame, width=40, height=10, yscrollcommand=scroll.set)
listbox.pack()
scroll.config(command=listbox.yview)
view = Button(root, text="View Drinks", bg="brown", fg="white", command=viewall)
view.place(x=10, y=350)

searchbutton = Button(root, text="Search", bg="brown", fg="white", command=searchdrink)
searchbutton.place(x=100, y=350)

randombutton = Button(root, text="Random", bg="brown", fg="white", command=randomdrink)
randombutton.place(x=170, y=350)

listbox.bind("<<ListboxSelect>>", selectdrink)

title = Label(root, text="CockTail Application", bg='black', fg="#e8a000", font=("Comic Sans", 20, 'bold'))
title.place(x=0, y=0)
play()

root.mainloop()
