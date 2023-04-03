import tkinter
from tkinter import ttk
from tkinter import messagebox, colorchooser
import os
import time
import sqlite3
import webcolors
import backend

from io import BytesIO
from PIL import Image,ImageTk


# Defining variables to store the current profile pic
binary_img = ''
profile_pic = ''
snakecolor_hex = ''

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" #To hide the welcome message of pygame module
from pygame import mixer
def button_click_sound(): #Plays the 'button_music.mp3' whenever a button is clicked
    mixer.init()
    mixer.music.load(dc.button_music)
    mixer.music.play()

# Getting screen width and height
from win32api import GetSystemMetrics
screen_width  =  GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

# Creating a Tkinter screen
root = tkinter.Tk()
root.geometry(f'1000x680+{((screen_width-1000)//2)-5}+20')
root.title('Snake_Game')
root.resizable(0,0)

import defined_constants as dc
root.iconphoto(True,dc.game_icon)
game_icon_i = dc.game_icon.subsample(4,4)

style = ttk.Style()
style.layout('TNotebook.Tab', [])

def changetitle():
    if l1['text'] == 'Snake Game' :
        l1['text'] = 'Snake_Game'
    elif l1['text'] == 'Snake_Game' :
        l1['text'] = 'Snake__Game'
    else:
        l1['text'] = 'Snake Game'
    root.after(1000,changetitle)
    
root.after(1000,changetitle)


# Making Tabs using Notebook
my_notebook = ttk.Notebook(root,width=1000,height=700)
my_notebook.pack()
main_page = tkinter.Frame(my_notebook)
customize_page = tkinter.Frame(my_notebook,bg=dc.black)
settings_page = tkinter.Frame(my_notebook,bg=dc.black)
main_page.pack(fill='both',expand=1)
customize_page.pack(fill='both',expand=1)
my_notebook.add(main_page,text ="Welcome Tab")
my_notebook.add(customize_page,text="Customize")
my_notebook.add(settings_page,text="Settings")

# Setting backgroung image
background_label = tkinter.Label(main_page,image=dc.game_bg)
background_label.place(x=0,y=0,relwidth=1,relheight=1)

# Functions for opening tabs
def start_game():
    button_click_sound()
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchall()[0][0] != 0 :
        backend.update_userdata(snakecolor.get(),snakecolor_hex,food.get(),level_button['text'],controlkeys_button['text'])
        root.withdraw()
        os.system('python snakegame.py')
        root.deiconify()
    else:
        my_notebook.select(2)
def main():
    button_click_sound()
    my_notebook.select(0)
    root.focus_set()
def customize():
    button_click_sound()
    my_notebook.select(1)
    root.focus_set()
def settings():
    button_click_sound()
    my_notebook.select(2)
def open_database():
    button_click_sound()
    root.withdraw()
    os.system('python frontend.py')
    root.deiconify()
def close_program():
    MsgBox = messagebox.askquestion('Snake_Game','Are you sure you want to exit the application',icon = 'info')
    if MsgBox == 'yes':
        conn = sqlite3.connect('snakegame_db.db')
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM users")
        if cur.fetchall()[0][0] != 0 :
            backend.update_userdata(snakecolor.get(),snakecolor_hex,food.get(),level_button['text'],controlkeys_button['text'])
        root.destroy()

# Welcome Tab
l1 = tkinter.Label(main_page,text='Snake_Game',image=game_icon_i,compound='left',font=('Castellar',45),bg=dc.color5,padx=10)
l1.pack(pady=70)

start_game_button = tkinter.Button(main_page,text='Start Game',font=('OCR A Extended',20),command=start_game,bg='gold',bd=5,width=15)
start_game_button.pack(pady=5)
customize_button = tkinter.Button(main_page,text='Customize',font=('OCR A Extended',20),bg='gold',command=customize,bd=5,width=15)
customize_button.pack(pady=5)
settings_button = tkinter.Button(main_page,text='Settings',font=('OCR A Extended',20),bg='gold',command=settings,bd=5,width=15)
settings_button.pack(pady=5)
db_button = tkinter.Button(main_page,text='Database',font=('OCR A Extended',20),bg='gold',command=open_database,bd=5,width=15)
db_button.pack(pady=5)
exit_button = tkinter.Button(main_page,text='Exit',font=('OCR A Extended',20),bg='gold',command=close_program,bd=5,width=15)
exit_button.pack(pady=5)

# Navigation buttons
previous_and_next_button_customizetab = tkinter.Frame(customize_page,bg=dc.black)
previous_and_next_button_settingstab = tkinter.Frame(settings_page,bg=dc.black)
previous_and_next_button_customizetab.place(x=10,y=10)
previous_and_next_button_settingstab.place(x=10,y=10)

previous_customizepage_button = tkinter.Button(previous_and_next_button_customizetab,image=dc.miniprevious_image,activebackground=dc.black,command=main,bg=dc.black,bd=0)
next_customizepage_button = tkinter.Button(previous_and_next_button_customizetab,image=dc.mininext_image,activebackground=dc.black,bg=dc.black,command=settings,bd=0)
previous_customizepage_button.pack(side='left',padx=(10,5))
next_customizepage_button.pack(side='right',padx=(10,0)) 

previous_settingspage_button = tkinter.Button(previous_and_next_button_settingstab,image=dc.miniprevious_image,activebackground=dc.black,command=customize,bg=dc.black,bd=0)
next_settingspage_button = tkinter.Button(previous_and_next_button_settingstab,image=dc.mininext_image,activebackground=dc.black,bg=dc.black,command=main,bd=0)
previous_settingspage_button.pack(side='left',padx=(10,5))
next_settingspage_button.pack(side='right',padx=(10,0))

# Customize Tab
cl2 = tkinter.Label(customize_page,text='Customize',font=('Castellar',30),bg=dc.black,fg=dc.pure_white,padx=10)
cl2.place(x=350,y=40)
customize_l1 = tkinter.Label(customize_page,text='Change the color of the snake using  ',font=('Monaco',18),bg=dc.black,fg=dc.moccasin,pady=10,padx=5)
customize_l1.place(x=105,y=120)
customize_l2 = tkinter.Label(customize_page,text='The color of the snake chosen ',font=('Monaco',18),bg=dc.black,fg=dc.moccasin,pady=10,padx=5)
customize_l2.place(x=105,y=160)
customize_l3 = tkinter.Label(customize_page,text='The food chosen for the snake to eat ',font=('Monaco',18),bg=dc.black,fg=dc.moccasin,pady=10,padx=5)
customize_l3.place(x=105,y=400)

color_slide = 1
def previous_color_slide():
    button_click_sound()
    global color_slide
    color_slide -= 1
    if color_slide == 1:
        orange_button.place_forget()
        pink_button.place_forget()
        violet_button.place_forget()
        white_button.place_forget()
        red_button.place(x=60,y=220)
        green_button.place(x=280,y=220)
        blue_button.place(x=500,y=220)
        yellow_button.place(x=720,y=220)
        color_previous_button.config(state='disabled')
    elif color_slide == 2:
        lightblue_button.place_forget()
        lightgreen_button.place_forget()
        magenta_button.place_forget()
        cyan_button.place_forget()
        orange_button.place(x=60,y=220)
        pink_button.place(x=280,y=220)
        violet_button.place(x=500,y=220)
        white_button.place(x=720,y=220)
    elif color_slide == 3:
        color_next_button.config(state='normal')
        gray_button.place_forget()
        peach_button.place_forget()
        brown_button.place_forget()
        chocolate_button.place_forget()
        lightblue_button.place(x=60,y=220)
        lightgreen_button.place(x=280,y=220)
        magenta_button.place(x=500,y=220)
        cyan_button.place(x=720,y=220)

def next_color_slide():
    button_click_sound()
    global color_slide
    if color_slide == 1:
        color_previous_button.config(state='normal')
        red_button.place_forget()
        green_button.place_forget()
        blue_button.place_forget()
        yellow_button.place_forget()
        orange_button.place(x=60,y=220)
        pink_button.place(x=280,y=220)
        violet_button.place(x=500,y=220)
        white_button.place(x=720,y=220)
    elif color_slide == 2:
        orange_button.place_forget()
        pink_button.place_forget()
        violet_button.place_forget()
        white_button.place_forget()
        lightblue_button.place(x=60,y=220)
        lightgreen_button.place(x=280,y=220)
        magenta_button.place(x=500,y=220)
        cyan_button.place(x=720,y=220)
    elif color_slide == 3:
        lightblue_button.place_forget()
        lightgreen_button.place_forget()
        magenta_button.place_forget()
        cyan_button.place_forget()
        gray_button.place(x=60,y=220)
        peach_button.place(x=280,y=220)
        brown_button.place(x=500,y=220)
        chocolate_button.place(x=720,y=220)
    color_slide += 1
    if color_slide == 4:
        color_next_button.config(state='disabled')

food_slide = 1
def previous_food_slide():
    button_click_sound()
    global food_slide
    food_slide -= 1
    if food_slide == 1:
        clover.place_forget()
        egg.place_forget()
        frog.place_forget()
        grapes.place_forget()
        red_apple.place(x=60,y=450)
        capsicum.place(x=280,y=450)
        carrot.place(x=500,y=450)
        cherry.place(x=720,y=450)
    elif food_slide == 2:
        green_apple.place_forget()
        lime.place_forget()
        mango.place_forget()
        mushroom.place_forget()
        clover.place(x=60,y=450)
        egg.place(x=280,y=450)
        frog.place(x=500,y=450)
        grapes.place(x=720,y=450)
    elif food_slide == 3:
        food_next_button.config(state='normal')
        peach.place_forget()
        pine_apple.place_forget()
        strawberry.place_forget()
        watermelon.place_forget()
        green_apple.place(x=60,y=450)
        lime.place(x=280,y=450)
        mango.place(x=500,y=450)
        mushroom.place(x=720,y=450)
    if food_slide == 1:
        food_previous_button.config(state='disabled')
def next_food_slide():
    button_click_sound()
    global food_slide
    if food_slide == 1:
        food_previous_button.config(state='normal')
        red_apple.place_forget()
        capsicum.place_forget()
        carrot.place_forget()
        cherry.place_forget()
        clover.place(x=60,y=450)
        egg.place(x=280,y=450)
        frog.place(x=500,y=450)
        grapes.place(x=720,y=450)
    elif food_slide == 2:
        clover.place_forget()
        egg.place_forget()
        frog.place_forget()
        grapes.place_forget()
        green_apple.place(x=60,y=450)
        lime.place(x=280,y=450)
        mango.place(x=500,y=450)
        mushroom.place(x=720,y=450)
    elif food_slide == 3:
        green_apple.place_forget()
        lime.place_forget()
        mango.place_forget()
        mushroom.place_forget()
        peach.place(x=60,y=450)
        pine_apple.place(x=280,y=450)
        strawberry.place(x=500,y=450)
        watermelon.place(x=720,y=450)
    food_slide += 1
    if food_slide == 4:
        food_next_button.config(state='disabled')

color_previous_button = tkinter.Button(customize_page,image=dc.previous_image,bg=dc.black,activebackground=dc.black,bd=0,state='disabled',command=previous_color_slide)
color_previous_button.place(x=10,y=270)
color_next_button = tkinter.Button(customize_page,image=dc.next_image,bg=dc.black,activebackground=dc.black,bd=0,command=next_color_slide)
color_next_button.place(x=945,y=270)

food_previous_button = tkinter.Button(customize_page,image=dc.previous_image,bg=dc.black,activebackground=dc.black,bd=0,state='disabled',command=previous_food_slide)
food_previous_button.place(x=10,y=500)
food_next_button = tkinter.Button(customize_page,image=dc.next_image,bg=dc.black,activebackground=dc.black,bd=0,command=next_food_slide)
food_next_button.place(x=945,y=500)

color_chooser_txt = tkinter.StringVar()
color_chooser = ttk.Combobox(customize_page,width=18,font=('Anonymous Pro',15),textvariable=color_chooser_txt,state='readonly')
color_chooser['values'] = ('Standard Colors','Color Palette')
color_chooser.place(x=655,y=130)

snakecolor = tkinter.StringVar()
snakecolor.set(backend.current_userdata()[2])
snakecolor_hex = backend.current_userdata()[3]
color_chosen_entrybox = tkinter.Entry(customize_page,textvariable=snakecolor,font=('Anonymous Pro',15),bg=dc.white,selectbackground=dc.color1,width=20,state='readonly')
color_chosen_entrybox.place(x=655,y=170)

food = tkinter.StringVar()
food.set(backend.current_userdata()[4])
food_chosen_entrybox = tkinter.Entry(customize_page,textvariable=food,font=('Anonymous Pro',15),bg=dc.white,selectbackground=dc.color1,width=20,state='readonly')
food_chosen_entrybox.place(x=655,y=410)

# Enabling and Disabling button as well changing the snakecolor
def color_unselect():
    red_button.config(state='normal',relief='flat')
    green_button.config(state='normal',relief='flat')
    blue_button.config(state='normal',relief='flat')
    yellow_button.config(state='normal',relief='flat')
    orange_button.config(state='normal',relief='flat')
    pink_button.config(state='normal',relief='flat')
    violet_button.config(state='normal',relief='flat')
    white_button.config(state='normal',relief='flat')
    lightblue_button.config(state='normal',relief='flat')
    lightgreen_button.config(state='normal',relief='flat')
    magenta_button.config(state='normal',relief='flat')
    cyan_button.config(state='normal',relief='flat')
    gray_button.config(state='normal',relief='flat')
    brown_button.config(state='normal',relief='flat')
    peach_button.config(state='normal',relief='flat')
    chocolate_button.config(state='normal',relief='flat')
def color_select():
    global snakecolor_hex
    if snakecolor.get() == 'Red':
        snakecolor_hex = dc.red
        red_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Green':
        snakecolor_hex = dc.green
        green_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Blue':
        snakecolor_hex = dc.blue
        blue_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Yellow':
        snakecolor_hex = dc.yellow
        yellow_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Orange':
        snakecolor_hex = dc.orange
        orange_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Pink':
        snakecolor_hex = dc.pink
        pink_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Violet':
        snakecolor_hex = dc.violet
        violet_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'White':
        snakecolor_hex = dc.white
        white_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Lightblue':
        snakecolor_hex = dc.lightblue
        lightblue_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Lightgreen':
        snakecolor_hex = dc.lightgreen
        lightgreen_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Magenta':
        snakecolor_hex = dc.magenta
        magenta_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Cyan':
        snakecolor_hex = dc.cyan
        cyan_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Gray':
        snakecolor_hex = dc.gray
        gray_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Brown':
        snakecolor_hex = dc.brown
        brown_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Peach':
        snakecolor_hex = dc.peach
        peach_button.config(state='disabled',relief='sunken')
    if snakecolor.get() == 'Chocolate':
        snakecolor_hex = dc.chocolate
        chocolate_button.config(state='disabled',relief='sunken')
def change_color(nameofthecolor):
    button_click_sound()
    color_unselect()
    snakecolor.set(nameofthecolor)
    color_select()

red_button = tkinter.Button(customize_page,text='Red',bd=20,bg=dc.red,command=lambda: change_color('Red'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
green_button = tkinter.Button(customize_page,text='Green',bd=20,bg=dc.green,command=lambda: change_color('Green'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
blue_button = tkinter.Button(customize_page,text='Blue',bd=20,bg=dc.blue,command=lambda: change_color('Blue'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
yellow_button = tkinter.Button(customize_page,text='Yellow',bd=20,bg=dc.yellow,command=lambda: change_color('Yellow'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
orange_button = tkinter.Button(customize_page,text='Orange',bd=20,bg=dc.orange,command=lambda: change_color('Orange'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
pink_button = tkinter.Button(customize_page,text='Pink',bd=20,bg=dc.pink,command=lambda: change_color('Pink'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
violet_button = tkinter.Button(customize_page,text='Violet',bd=20,bg=dc.violet,command=lambda: change_color('Violet'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
white_button = tkinter.Button(customize_page,text='White',bd=20,bg=dc.white,command=lambda: change_color('White'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
lightblue_button = tkinter.Button(customize_page,text='Light Blue',bd=20,bg=dc.lightblue,command=lambda: change_color('Lightblue'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
lightgreen_button = tkinter.Button(customize_page,text='Light Green',bd=20,bg=dc.lightgreen,command=lambda: change_color('Lightgreen'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
magenta_button = tkinter.Button(customize_page,text='Magenta',bd=20,bg=dc.magenta,command=lambda: change_color('Magenta'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
cyan_button = tkinter.Button(customize_page,text='Cyan',bd=20,bg=dc.cyan,command=lambda: change_color('Cyan'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
gray_button = tkinter.Button(customize_page,text='Gray',bd=20,bg=dc.gray,command=lambda: change_color('Gray'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
peach_button = tkinter.Button(customize_page,text='Peach',bd=20,bg=dc.peach,command=lambda: change_color('Peach'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
brown_button = tkinter.Button(customize_page,text='Brown',bd=20,bg=dc.brown,command=lambda: change_color('Brown'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
chocolate_button = tkinter.Button(customize_page,text='Chocolate',bd=20,bg=dc.chocolate,command=lambda: change_color('Chocolate'),width=25,height=7,relief='flat',disabledforeground=dc.pure_white)
red_button.place(x=60,y=220)
green_button.place(x=280,y=220)
blue_button.place(x=500,y=220)
yellow_button.place(x=720,y=220)

if backend.current_userdata()[2] in dc.standard_colors:
    color_chooser.current(0)
else:
    color_chooser.current(1)
    red_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')
    green_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')
    blue_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')
    yellow_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')

def color_palette_or_standard(event):
    if color_chooser.get() == 'Standard Colors' :
        color_next_button.config(state='normal')
        red_button.config(state='normal',bg=dc.red,relief='flat',text='Red')
        green_button.config(state='normal',bg=dc.green,relief='flat',text='Green')
        blue_button.config(state='normal',bg=dc.blue,relief='flat',text='Blue')
        yellow_button.config(state='normal',bg=dc.yellow,relief='flat',text='Yellow')
    else:
        global snakecolor_hex
        global color_slide
        if color_slide == 4 :
            previous_color_slide()
            previous_color_slide()
            previous_color_slide()
        elif color_slide == 3 :
            previous_color_slide()
            previous_color_slide()
        elif color_slide == 2 :
            previous_color_slide()
        color_unselect()
        color_next_button.config(state='disabled')
        getcolor_from_colorchooser = colorchooser.askcolor(title ="Choose SnakeColor")[1]
        if getcolor_from_colorchooser == None:
            return
        snakecolor_hex = getcolor_from_colorchooser
        try:
            snakecolor.set(webcolors.hex_to_name(snakecolor_hex).title())
        except (ValueError,TypeError):
            snakecolor.set(snakecolor_hex.upper())

        red_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')
        green_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')
        blue_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')
        yellow_button.config(state='disabled',bg=snakecolor_hex,relief='flat',text='')

color_chooser.bind('<<ComboboxSelected>>',color_palette_or_standard)

def food_unselect():
    red_apple.config(bd=0,relief='flat')
    capsicum.config(bd=0,relief='flat')
    carrot.config(bd=0,relief='flat')
    cherry.config(bd=0,relief='flat')
    clover.config(bd=0,relief='flat')
    egg.config(bd=0,relief='flat')
    frog.config(bd=0,relief='flat')
    grapes.config(bd=0,relief='flat')
    green_apple.config(bd=0,relief='flat')
    lime.config(bd=0,relief='flat')
    mango.config(bd=0,relief='flat')
    mushroom.config(bd=0,relief='flat')
    peach.config(bd=0,relief='flat')
    pine_apple.config(bd=0,relief='flat')
    strawberry.config(bd=0,relief='flat')
    watermelon.config(bd=0,relief='flat')
def food_select():
    if food.get() == 'Apple' :
        red_apple.config(bd=10,relief='raised')
    if food.get() == 'Capsicum' :
        capsicum.config(bd=10,relief='raised')
    if food.get() == 'Carrot' :
        carrot.config(bd=10,relief='raised')
    if food.get() == 'Cherry' :
        cherry.config(bd=10,relief='raised')
    if food.get() == 'Clover' :
        clover.config(bd=10,relief='raised')
    if food.get() == 'Egg' :
        egg.config(bd=10,relief='raised')
    if food.get() == 'Frog' :
        frog.config(bd=10,relief='raised')
    if food.get() == 'Grapes' :
        grapes.config(bd=10,relief='raised')
    if food.get() == 'Green Apple' :
        green_apple.config(bd=10,relief='raised')
    if food.get() == 'Lime' :
        lime.config(bd=10,relief='raised')
    if food.get() == 'Mango' :
        mango.config(bd=10,relief='raised')
    if food.get() == 'Mushroom' :
        mushroom.config(bd=10,relief='raised')
    if food.get() == 'Peach' :
        peach.config(bd=10,relief='raised')
    if food.get() == 'Pineapple' :
        pine_apple.config(bd=10,relief='raised')
    if food.get() == 'Strawberry' :
        strawberry.config(bd=10,relief='raised')
    if food.get() == 'Watermelon' :
        watermelon.config(bd=10,relief='raised')
def change_food(nameofthefood):
    button_click_sound()
    food_unselect()
    food.set(nameofthefood)
    food_select()

red_apple = tkinter.Button(customize_page,image=dc.red_apple_image,bg=dc.black,relief='flat',command=lambda: change_food('Apple'),activebackground=dc.black,bd=10)
capsicum = tkinter.Button(customize_page,image=dc.capsicum_image,bg=dc.black,relief='flat',command=lambda: change_food('Capsicum'),activebackground=dc.black)
carrot = tkinter.Button(customize_page,image=dc.carrot_image,bg=dc.black,relief='flat',command=lambda: change_food('Carrot'),activebackground=dc.black)
cherry = tkinter.Button(customize_page,image=dc.cherry_image,bg=dc.black,relief='flat',command=lambda: change_food('Cherry'),activebackground=dc.black)
clover= tkinter.Button(customize_page,image=dc.clover_image,bg=dc.black,relief='flat',command=lambda: change_food('Clover'),activebackground=dc.black)
egg = tkinter.Button(customize_page,image=dc.egg_image,bg=dc.black,relief='flat',command=lambda: change_food('Egg'),activebackground=dc.black)
frog = tkinter.Button(customize_page,image=dc.frog_image,bg=dc.black,relief='flat',command=lambda: change_food('Frog'),activebackground=dc.black)
grapes = tkinter.Button(customize_page,image=dc.grapes_image,bg=dc.black,relief='flat',command=lambda: change_food('Grapes'),activebackground=dc.black)
green_apple = tkinter.Button(customize_page,image=dc.green_apple_image,bg=dc.black,relief='flat',command=lambda: change_food('Green Apple'),activebackground=dc.black)
lime = tkinter.Button(customize_page,image=dc.lime_image,bg=dc.black,relief='flat',command=lambda: change_food('Lime'),activebackground=dc.black)
mango = tkinter.Button(customize_page,image=dc.mango_image,bg=dc.black,relief='flat',command=lambda: change_food('Mango'),activebackground=dc.black)
mushroom = tkinter.Button(customize_page,image=dc.mushroom_image,bg=dc.black,relief='flat',command=lambda: change_food('Mushroom'),activebackground=dc.black)
peach = tkinter.Button(customize_page,image=dc.peach_image,bg=dc.black,relief='flat',command=lambda: change_food('Peach'),activebackground=dc.black)
pine_apple = tkinter.Button(customize_page,image=dc.pine_apple_image,bg=dc.black,relief='flat',command=lambda: change_food('Pineapple'),activebackground=dc.black)
strawberry = tkinter.Button(customize_page,image=dc.strawberry_image,bg=dc.black,relief='flat',command=lambda: change_food('Strawberry'),activebackground=dc.black)
watermelon = tkinter.Button(customize_page,image=dc.watermelon_image,bg=dc.black,relief='flat',command=lambda: change_food('Watermelon'),activebackground=dc.black)
red_apple.place(x=60,y=450)
capsicum.place(x=280,y=450)
carrot.place(x=500,y=450)
cherry.place(x=720,y=450)

color_select()
food_select()

# Settings Tab
l3 = tkinter.Label(settings_page,text='Settings',font=('Castellar',30),bg=dc.black,padx=10,fg=dc.pure_white)
l3.place(x=380,y=40)

create_login_frame = tkinter.Frame(settings_page,bg=dc.black,relief='raised',bd=10)
current_users_frame = tkinter.Frame(settings_page,bg=dc.black,relief='raised',bd=10)

level_labelframe = tkinter.LabelFrame(settings_page,text='Level',bg=dc.black,fg=dc.white)
level_labelframe.place(x=125,y=360)
controlkeys_labelframe = tkinter.LabelFrame(settings_page,text='Controls',bg=dc.black,fg=dc.white)
controlkeys_labelframe.place(x=125,y=460)

temp_frame = tkinter.Frame(settings_page,bg=dc.black)
canvas = tkinter.Canvas(temp_frame,bg=dc.black,width=325,height=270)
profile_pic_frame = tkinter.Frame(canvas,bg=dc.black)
profile_pic_frame.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0),window=profile_pic_frame,anchor='nw')
profile_pic_frame_scrollbar = tkinter.Scrollbar(temp_frame,orient="vertical",command=canvas.yview,width=12,elementborderwidth=0)
canvas.configure(yscrollcommand=profile_pic_frame_scrollbar.set)

change_user_frame = tkinter.Frame(settings_page,bg=dc.black,relief='raised',bd=10)
change_user_frame.grid_rowconfigure(0,weight=1)
change_user_frame.grid_columnconfigure(0,weight=1)
sb = tkinter.Scrollbar(change_user_frame,width=15)
sb.grid(row=1,column=7,sticky=tkinter.E+tkinter.W,ipady=68,padx=3)
create_login_frame.pack(pady=120)

def change_profile_pic_frame():
    button_click_sound()
    current_user_b1.bind('<Leave>','pass')
    current_user_b1.config(bg=dc.color3)
    temp_frame.place(x=35,y=300)
def calling_change_user():
    button_click_sound()
    name_text.set('')
    password_text.set('')
    create_login_frame.pack_forget()
    current_users_frame.place_forget()
    change_user_frame.pack(pady=120)
    level_labelframe.place(x=125,y=470)
    controlkeys_labelframe.place(x=125,y=560)
    list_of_users.delete(0,'end')
    for i in backend.get_list_of_users():
        list_of_users.insert('end',i)
    list_of_users.select_set(0)
    list_of_users.focus()
def check_valid_username(string) -> bool:
    if len(string) < 4 :
        messagebox.showerror('Snake_Game',"Username can't be less than 4 characters")
        return False
    elif len(string) > 16 :
        messagebox.showerror('Snake_Game',"Username can't be greater than 16 characters")
        return False
    elif not string[0].isalpha() :
        messagebox.showerror('Snake_Game'," First letter need to be an alphabet  ")
        return False
    for i in string:
        if i.isalnum() or i in ['-','_','.'] :
            continue
        else:
            messagebox.showerror('Snake_Game',"Special Characters other than '-' , '_' and period are not allowed")
            return False
    return True

def check_valid_password(string) -> bool:
    if len(string) == 0:
        MsgBox = messagebox.askquestion('Snake_Game',"Do you want to continue without password?",icon='warning')
        if MsgBox == 'no':
            return False
    elif len(string) < 4:
        MsgBox = messagebox.showerror('Snake_Game',"Password can't be less than 4 characters")
        return False
    return True
    
def show_password(profile_e2,show_password_button):
    profile_e2.config(show="")
    show_password_button.config(image=dc.eye_opened,command=lambda: hide_password(profile_e2,show_password_button))
def hide_password(profile_e2,show_password_button):
    profile_e2.config(show="*")
    show_password_button.config(image=dc.eye_closed,command=lambda: show_password(profile_e2,show_password_button))
def add_users(username,password):
    button_click_sound()
    if check_valid_username(username) and check_valid_password(password):
        try:
            backend.add_usersin_users_and_current_users_table(username,password)
            messagebox.showinfo('Snake_Game',"\tAdded Successfully!\t")
            root.focus_set()
            name_text.set('')
            password_text.set('')
            calling_current_user()
            make_profile_picbg_normal()
            highlight_image_id()
        except sqlite3.IntegrityError:
            messagebox.showerror('Snake_Game',"The entered username has been already taken")
            return
def calling_create_users():
    button_click_sound()
    change_user_frame.pack_forget()
    create_login_frame.pack(pady=150)
    level_labelframe.place(x=125,y=360)
    controlkeys_labelframe.place(x=125,y=460)
    name_text.set('')
    password_text.set('')
    create_login_e1.focus()
    create_login_label['text'] = 'Create Profile'
    create_login_e1.config(state='normal')
    create_login_confirm_button.config(command=lambda: add_users(name_text.get(),password_text.get()))
def get_current_user_profile_pic():
    global binary_img
    global profile_pic
    binary_img = Image.open(BytesIO(backend.current_user_profile_pic()))
    profile_pic = ImageTk.PhotoImage(binary_img)
    current_user_b1.config(image=profile_pic)
def calling_current_user():
    global current_user_highscore
    global current_user_total_games
    create_login_frame.pack_forget()
    current_users_frame.place(x=125,y=120)
    level_labelframe.place(x=125,y=360)
    controlkeys_labelframe.place(x=125,y=460)
    userdata = backend.current_user_display()
    current_user_username_txt.set(userdata[0])
    current_user_fruits_ate_int.set(userdata[1])
    current_user_highscore = str(userdata[2])
    current_user_total_games = str(userdata[3])
    get_current_user_profile_pic()

    current_user_l3.config(text='Highscore: ' + str(current_user_highscore))
    current_user_l4.config(text='Games Played: ' + str(current_user_total_games))

def check_entered_password(entered_password,original_password,username):
    button_click_sound()
    if entered_password == original_password :
        backend.update_current_user(username)
        make_profile_picbg_normal()
        highlight_image_id()
        calling_current_user()
    else:
        messagebox.showerror('Snake_Game',"The entered password is incorrect")
def login_user():
    button_click_sound()
    selected_user = list_of_users.get(list_of_users.curselection()[0])[1]
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute('SELECT username from current_user')
    if selected_user == cur.fetchall()[0][0] :
        back_to_current_user()
        return
    original_username = backend.get_username_password(selected_user)[0]
    original_password = backend.get_username_password(selected_user)[1]
    if len(original_password) == 0 :
        change_user_frame.pack_forget()
        check_entered_password("",original_password,original_username)
        return
    change_user_frame.pack_forget()
    create_login_frame.pack(pady=150)
    level_labelframe.place(x=125,y=360)
    controlkeys_labelframe.place(x=125,y=460)
    create_login_label['text'] = 'Log In     '
    name_text.set(original_username)
    create_login_e1.config(state='readonly')
    create_login_confirm_button.config(command=lambda: check_entered_password(password_text.get(),original_password,original_username))
    create_login_e2.focus()

def back_to_current_user():
    button_click_sound()
    change_user_frame.pack_forget()
    current_users_frame.place(x=125,y=120)
    level_labelframe.place(x=125,y=360)
    controlkeys_labelframe.place(x=125,y=460)
    root.focus_set()
    calling_current_user()


# Functions for updating profile pic
def highlight_image_id():
    image_id = backend.get_imageid()
    if image_id == 1 :
        pic1_button.config(bg=dc.color3)
    if image_id == 2 :
        pic2_button.config(bg=dc.color3)
    if image_id == 3 :
        pic3_button.config(bg=dc.color3)
    if image_id == 4 :
        pic4_button.config(bg=dc.color3)
    if image_id == 5 :
        pic5_button.config(bg=dc.color3)
    if image_id == 6 :
        pic6_button.config(bg=dc.color3)
    if image_id == 7 :
        pic7_button.config(bg=dc.color3)
    if image_id == 8 :
        pic8_button.config(bg=dc.color3)
    if image_id == 9 :
        pic9_button.config(bg=dc.color3)
    if image_id == 10 :
        pic10_button.config(bg=dc.color3)
    if image_id == 11 :
        pic11_button.config(bg=dc.color3)
    if image_id == 12 :
        pic12_button.config(bg=dc.color3)
    if image_id == 13 :
        pic13_button.config(bg=dc.color3)
    if image_id == 14 :
        pic14_button.config(bg=dc.color3)
    if image_id == 15 :
        pic15_button.config(bg=dc.color3)
def make_profile_picbg_normal():
    pic1_button.config(bg=dc.black)
    pic2_button.config(bg=dc.black)
    pic3_button.config(bg=dc.black)
    pic4_button.config(bg=dc.black)
    pic5_button.config(bg=dc.black)
    pic6_button.config(bg=dc.black)
    pic7_button.config(bg=dc.black)
    pic8_button.config(bg=dc.black)
    pic9_button.config(bg=dc.black)
    pic10_button.config(bg=dc.black)
    pic11_button.config(bg=dc.black)
    pic12_button.config(bg=dc.black)
    pic13_button.config(bg=dc.black)
    pic14_button.config(bg=dc.black)
    pic15_button.config(bg=dc.black)
def set_profile_pic(number,image):
    backend.update_profile_pic(number)
    make_profile_picbg_normal()
    current_user_b1.config(image=image)
    highlight_image_id()

# Building create users frame
create_login_label = tkinter.Label(create_login_frame,text='Create Profile',font=('Anonymous Pro',24),bg=dc.black,fg=dc.color4)
create_login_l1 = tkinter.Label(create_login_frame,text='       Username',font=('Monaco',18),bg=dc.black,fg=dc.moccasin)
create_login_l2 = tkinter.Label(create_login_frame,text='Password',font=('Monaco',18),bg=dc.black,fg=dc.moccasin)
name_text = tkinter.StringVar()
password_text = tkinter.StringVar()
create_login_e1 = tkinter.Entry(create_login_frame,textvariable=name_text,font=('Anonymous Pro',16),width=15,selectbackground=dc.color1)
create_login_e2 = tkinter.Entry(create_login_frame,textvariable=password_text,show="*",font=('Anonymous Pro',16),width=15,selectbackground=dc.color1)
password_button = tkinter.Button(create_login_frame,image=dc.eye_closed,command=lambda: show_password(create_login_e2,password_button),bg=dc.pure_white,bd=0,borderwidth=0)
create_login_confirm_button = tkinter.Button(create_login_frame,text='Confirm',font=('Ubuntu',15),bg=dc.color1,activebackground=dc.color1,fg=dc.pure_black,activeforeground=dc.pure_white,borderwidth=3,width=10,
command=lambda: add_users(name_text.get(),password_text.get()))
create_login_back_button = tkinter.Button(create_login_frame,text='Back',font=('Ubuntu',15),bg=dc.color1,activebackground=dc.color1,fg=dc.pure_black,activeforeground=dc.pure_white,
borderwidth=3,width=10,command=calling_change_user)

create_login_label.grid(row=0,column=0)
create_login_l1.grid(row=1,column=0,pady=10)
create_login_e1.grid(row=1,column=1,pady=10,padx=20)
create_login_l2.grid(row=1,column=2,pady=10,padx=20)
create_login_e2.grid(row=1,column=3,pady=10)
password_button.grid(row=1,column=4,padx=(0,10))
create_login_confirm_button.grid(row=2,column=2,columnspan=2,pady=(5,10),padx=(0,0))
create_login_back_button.grid(row=2,column=0,columnspan=2,pady=(5,10))

# Building current user frame
current_user_username_txt = tkinter.StringVar()
current_user_fruits_ate_int = tkinter.IntVar()
current_user_highscore = ''
current_user_total_games = ''
current_user_label = tkinter.Label(current_users_frame,text='User Profile\t',font=('Anonymous Pro',24),bg=dc.black,fg=dc.color4)
current_user_b1 = tkinter.Button(current_users_frame,image='',bg=dc.black,activebackground=dc.black,command=change_profile_pic_frame,bd=0)
current_user_b2 = tkinter.Button(current_users_frame,text='Change User',font=('Ubuntu',9),command=calling_change_user,
bg=dc.color1,activebackground=dc.color2,activeforeground=dc.pure_white)
current_user_l1 = tkinter.Label(current_users_frame,text='Username: ',font=('Monaco',18),bg=dc.black,fg=dc.moccasin)
current_user_l2 = tkinter.Label(current_users_frame,text='Fruits Ate: ',font=('Monaco',18),bg=dc.black,fg=dc.moccasin)
current_user_l3 = tkinter.Label(current_users_frame,text='Highscore: ',font=('Monaco',11),bg=dc.black,fg=dc.moccasin)
current_user_l4 = tkinter.Label(current_users_frame,text='Games Played: ',font=('Monaco',11),bg=dc.black,fg=dc.moccasin)
current_user_e1 = tkinter.Entry(current_users_frame,textvariable=current_user_username_txt,font=('Anonymous Pro',15),width=15,bg=dc.white,state='readonly',selectbackground=dc.color1)
current_user_e2 = tkinter.Entry(current_users_frame,textvariable=current_user_fruits_ate_int,font=('Anonymous Pro',15),width=7,bg=dc.white,state='readonly',selectbackground=dc.color1)
current_user_sep = ttk.Separator(current_users_frame,orient='horizontal')

current_user_label.grid(row=0,column=0,padx=0,pady=10,columnspan=2)
current_user_b1.grid(row=1,column=0,padx=5,pady=(10,5),rowspan=4)
current_user_l1.grid(row=1,column=1,padx=(0,10),pady=(20,5))
current_user_l2.grid(row=1,column=3,padx=(10,0),pady=(20,5))
current_user_b2.grid(row=0,column=4)
current_user_e1.grid(row=1,column=2,padx=(0,10),pady=(20,5))
current_user_e2.grid(row=1,column=4,padx=(0,10),pady=(20,5))
current_user_l3.grid(row=3,column=1,padx=0,pady=0,rowspan=2)
current_user_l4.grid(row=3,column=2,padx=(20,0),rowspan=2)
current_user_sep.grid(row=2,column=1,columnspan=4,ipadx=50,sticky="ew")

# Building change user frame
change_user_label = tkinter.Label(change_user_frame,text='List of Users',font=('Anonymous Pro',26),bg=dc.black,fg=dc.color4,bd=0)
change_user_label.grid(row=0,column=0,ipady=10,ipadx=10,pady=5,sticky='w')
list_of_users = tkinter.Listbox(change_user_frame,height=5,width=44,font=('Roboto Mono',20),bg=dc.black,fg=dc.moccasin,yscrollcommand=sb.set)
list_of_users.grid(row=1,column=0,columnspan=6,padx=(10,0))
sb.config(command= list_of_users.yview)
list_of_users.delete(0,'end')
list_of_users.config(selectbackground=dc.color1,activestyle='none')
for i in backend.get_list_of_users():
    list_of_users.insert('end',i)
list_of_users.select_set(0)
select_user_button = tkinter.Button(change_user_frame,text='Select',font=('Ubuntu',15),bg=dc.color1,
    activebackground=dc.color2,activeforeground=dc.pure_white,bd=4,command=login_user)
back_to_current_user_button = tkinter.Button(change_user_frame,text=' Back ',font=('Ubuntu',15,),bg=dc.color1,
    activebackground=dc.color2,activeforeground=dc.pure_white,bd=4,command=back_to_current_user)
add_users_button = tkinter.Button(change_user_frame,text='Add Profile',font=('Ubuntu',9),bg=dc.color1,
    activebackground=dc.color2,activeforeground=dc.pure_white,command=calling_create_users)
select_user_button.grid(row=2,column=5,columnspan=2,ipady=0,ipadx=30,pady=(12,7),padx=12)
back_to_current_user_button.grid(row=2,column=0,columnspan=1,ipady=0,ipadx=30,pady=(12,7),padx=(0,320))
add_users_button.grid(row=0,column=5,columnspan=2,ipadx=20)

# Building change profile pic frame
label = tkinter.Label(temp_frame,text='Choose a Profile Pic',font=('Monaco',10),bg=dc.black,fg=dc.moccasin).pack()
pic1_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic1,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(1,dc.profile_pic1),bd=0)
pic2_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic2,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(2,dc.profile_pic2),bd=0)
pic3_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic3,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(3,dc.profile_pic3),bd=0)
pic4_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic4,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(4,dc.profile_pic4),bd=0)
pic5_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic5,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(5,dc.profile_pic5),bd=0)
pic6_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic6,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(6,dc.profile_pic6),bd=0)
pic7_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic7,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(7,dc.profile_pic7),bd=0)
pic8_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic8,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(8,dc.profile_pic8),bd=0)
pic9_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic9,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(9,dc.profile_pic9),bd=0)
pic10_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic10,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(10,dc.profile_pic10),bd=0)
pic11_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic11,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(11,dc.profile_pic11),bd=0)
pic12_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic12,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(12,dc.profile_pic12),bd=0)
pic13_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic13,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(13,dc.profile_pic13),bd=0)
pic14_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic14,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(14,dc.profile_pic14),bd=0)
pic15_button = tkinter.Button(profile_pic_frame,image=dc.profile_pic15,bg=dc.black,
activebackground=dc.black,command=lambda: set_profile_pic(15,dc.profile_pic15),bd=0)

pic1_button.grid(row=1,column=0)
pic2_button.grid(row=1,column=1)
pic3_button.grid(row=1,column=2)
pic4_button.grid(row=2,column=0)
pic5_button.grid(row=2,column=1)
pic6_button.grid(row=2,column=2)
pic7_button.grid(row=3,column=0)
pic8_button.grid(row=3,column=1)
pic9_button.grid(row=3,column=2)
pic10_button.grid(row=4,column=0)
pic11_button.grid(row=4,column=1)
pic12_button.grid(row=4,column=2)
pic13_button.grid(row=5,column=0)
pic14_button.grid(row=5,column=1)
pic15_button.grid(row=5,column=2)

highlight_image_id()
canvas.pack(side='left',fill='both',expand=True)
profile_pic_frame_scrollbar.pack(side='right',fill='y')

# Labelframe for level and controls
def change_level_button():
    button_click_sound()
    if level_button['text'] == 'Easy':
        level_button['text'] = 'Medium'
    elif level_button['text'] == 'Medium':
        level_button['text'] = 'Hard'
    elif level_button['text'] == 'Hard':
        level_button['text'] = 'Easy'
def change_controlkeys_button():
    button_click_sound()
    if controlkeys_button['text'] == 'Arrow Keys':
        controlkeys_button['text'] = 'W A S D'
    else:
        controlkeys_button['text'] = 'Arrow Keys'

level_label = tkinter.Label(level_labelframe,text='Select the Level to play ',font=('Monaco',18),bg=dc.black,fg=dc.moccasin,pady=10,padx=5)
level_label.grid(row=0,column=0,pady=7,padx=(75,60))
level_button = tkinter.Button(level_labelframe,text=backend.current_userdata()[5],font=('Anonymous Pro',12),command=change_level_button,width=15)
level_button.grid(row=0,column=1,pady=7,padx=(20,80))

controlkeys_label = tkinter.Label(controlkeys_labelframe,text='Select the Control Keys  ',font=('Monaco',18),bg=dc.black,fg=dc.moccasin,pady=10,padx=5)
controlkeys_label.grid(row=0,column=0,pady=7,padx=(75,60))
controlkeys_button = tkinter.Button(controlkeys_labelframe,text=backend.current_userdata()[6],font=('Anonymous Pro',12),command=change_controlkeys_button,width=15)
controlkeys_button.grid(row=0,column=1,pady=7,padx=(20,80))


conn = sqlite3.connect('snakegame_db.db')
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM users")
if cur.fetchall()[0][0] != 0 :
    calling_current_user()
else:
    calling_create_users()
    create_login_back_button.grid_forget()
    create_login_confirm_button.grid(row=2,column=1,columnspan=2,pady=(5,10))


# Keybindings
def profile_pic_create_effects(event):
    time.sleep(0.2)
    current_user_b1.config(bg=dc.color3)
def remove_temp_frame(event):
    current_user_b1.bind('<Leave>',lambda e: current_user_b1.config(bg=dc.black))
    current_user_b1.config(bg=dc.black)
    temp_frame.place_forget()
def press_confirm_button():
    if create_login_label['text'][0:6] == 'Log In' :
        selected_user = list_of_users.get(list_of_users.curselection()[0])[1]
        original_username = backend.get_username_password(selected_user)[0]
        original_password = backend.get_username_password(selected_user)[1]
        check_entered_password(password_text.get(),original_password,original_username)
    else:
        add_users(name_text.get(),password_text.get())
settings_page.bind('<Button-1>',remove_temp_frame)
current_user_b2.bind('<Button-1>',remove_temp_frame)
current_users_frame.bind('<Button-1>',remove_temp_frame)
level_labelframe.bind('<Button-1>',remove_temp_frame)
controlkeys_labelframe.bind('<Button-1>',remove_temp_frame)
level_button.bind('<Button-1>',remove_temp_frame)
controlkeys_button.bind('<Button-1>',remove_temp_frame)
current_user_b1.bind('<Enter>',profile_pic_create_effects)
current_user_b1.bind('<Leave>',lambda e: current_user_b1.config(bg=dc.black))
color_chooser.bind('<FocusIn>',lambda e: color_chosen_entrybox.focus())
create_login_e2.bind('<Return>',lambda e: press_confirm_button())
list_of_users.bind('<Return>',lambda e: login_user())

root.protocol("WM_DELETE_WINDOW",close_program)
root.mainloop()
