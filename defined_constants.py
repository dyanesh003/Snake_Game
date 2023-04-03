import sqlite3
from io import BytesIO
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Importing fonts
from pyglet import font
font.add_file(r'fonts\AnonymousPro.ttf')
font.add_file(r'fonts\JetbrainsMono.ttf')
font.add_file(r'fonts\Monaco.ttf')
font.add_file(r'fonts\Montserrat.ttf')
font.add_file(r'fonts\ProFont.ttf')
font.add_file(r'fonts\RobotoMono.ttf')
font.add_file(r'fonts\Ubuntu.ttf')
font.add_file(r'fonts\CASTELAR.TTF')
font.add_file(r'fonts\OCRAEXT.TTF')


button_music = 'button_click1.mp3'
standard_colors = ['Red','Green','Blue','Yellow','Orange','Pink','Violet','White','Lightblue','Lightgreen','Magenta','Cyan','Gray','Peach','Brown','Chocolate']


# Colors for the snake
red        = '#D00000'
green      = '#80B918'
blue       = '#262CF1'
yellow     = '#ffEA00'
orange     = '#FB8500'
pink       = '#F20089'
violet     = '#39083B'
white      = '#E1E1E1'
lightblue  = '#4CC9F0'
lightgreen = '#37EC2F'
magenta    = '#FF00FF'
cyan       = '#00FFFF'
gray       = '#6C757D'
peach      = '#FFA55C'
brown      = '#522500'
chocolate  = '#140900'

# Other Colors
pure_black = '#000000'
pure_white = '#FFFFFF' 
black      = '#171717'
black1     = '#0F0F0F'
black2     = '#121216'
black3     = '#111111'

moccasin   = '#FFE4B5'
color1     = '#FF3F45' 
color2     = '#FF5350'
color3     = '#FFA600'
color4     = '#00E0A7'
color5     = '#FCC625'


# Images for background, food and others
game_icon            = PhotoImage(file = r'snakegame_images\icon.png')
game_bg              = PhotoImage(file = r'snakegame_images\game_bg.png')
settings_image       = PhotoImage(file = r'snakegame_images\settings.png')
previous_image       = PhotoImage(file = r'snakegame_images\previous.png')
next_image           = PhotoImage(file = r'snakegame_images\next.png')
miniprevious_image   = PhotoImage(file = r'snakegame_images\miniprevious.png')
mininext_image       = PhotoImage(file = r'snakegame_images\mininext.png')
calendar_image       = PhotoImage(file = r'snakegame_images\cal1.png')
eye_opened           = PhotoImage(file = r'snakegame_images\icon_eyeopen.png')
eye_closed           = PhotoImage(file = r'snakegame_images\icon_eyeclosed.png')
red_apple_image      = PhotoImage(file = r'snakegame_food\_apple.png')                      
capsicum_image       = PhotoImage(file = r'snakegame_food\_capsicum.png')
carrot_image         = PhotoImage(file = r'snakegame_food\_carrot.png')
cherry_image         = PhotoImage(file = r'snakegame_food\_cherry.png')
clover_image         = PhotoImage(file = r'snakegame_food\_clover.png')
egg_image            = PhotoImage(file = r'snakegame_food\_egg.png')
frog_image           = PhotoImage(file = r'snakegame_food\_frog.png')
grapes_image         = PhotoImage(file = r'snakegame_food\_grapes.png')
green_apple_image    = PhotoImage(file = r'snakegame_food\_green_apple.png')
lime_image           = PhotoImage(file = r'snakegame_food\_lime.png')
mango_image          = PhotoImage(file = r'snakegame_food\_mango.png')
mushroom_image       = PhotoImage(file = r'snakegame_food\_mushroom.png')
peach_image          = PhotoImage(file = r'snakegame_food\_peach.png')
pine_apple_image     = PhotoImage(file = r'snakegame_food\_pine_apple.png')
strawberry_image     = PhotoImage(file = r'snakegame_food\_strawberry.png')
watermelon_image     = PhotoImage(file = r'snakegame_food\_watermelon.png')
search_image         = PhotoImage(file = r'snakegame_images\search.png')
single_select_image  = PhotoImage(file = r'snakegame_images\single_select.png')
multi_select_image   = PhotoImage(file = r'snakegame_images\multi_select.png')
delete_image         = PhotoImage(file = r'snakegame_images\delete.png')
viewall_image        = PhotoImage(file = r'snakegame_images\viewall.png')
clearall_image       = PhotoImage(file = r'snakegame_images\clearall.png')
exit_image           = PhotoImage(file = r'snakegame_images\exit.png')

#Resizing according to the GUI's needs
red_apple_image      = red_apple_image.subsample(3,4)
capsicum_image       = capsicum_image.subsample(3,3)
carrot_image         = carrot_image.subsample(3,4)
cherry_image         = cherry_image.subsample(3,4)
clover_image         = clover_image.subsample(3,4)
egg_image            = egg_image.subsample(2,2)
frog_image           = frog_image.subsample(1,1)
grapes_image         = grapes_image.subsample(3,4)
green_apple_image    = green_apple_image.subsample(3,4)
lime_image           = lime_image.subsample(3,4)
mango_image          = mango_image.subsample(3,4)
mushroom_image       = mushroom_image.subsample(3,4)
peach_image          = peach_image.subsample(3,4)
pine_apple_image     = pine_apple_image.subsample(3,4)
strawberry_image     = strawberry_image.subsample(3,4)
watermelon_image     = watermelon_image.subsample(3,4)
settings_image       = settings_image.subsample(6,6)
search_image         = search_image.subsample(2,2)
delete_image         = delete_image.subsample(2,2)
viewall_image        = viewall_image.subsample(2,2)
clearall_image       = clearall_image.subsample(2,2)
exit_image           = exit_image.subsample(2,2)

# Profile pics from database
conn = sqlite3.connect('snakegame_db.db')
cur = conn.cursor()
cur.execute('SELECT image FROM profile_pics ORDER BY Id')
list_of_images = cur.fetchall()

#Getting the binary data from the database
binary_img1   = Image.open(BytesIO(list_of_images[0][0]))
binary_img2   = Image.open(BytesIO(list_of_images[1][0]))
binary_img3   = Image.open(BytesIO(list_of_images[2][0]))
binary_img4   = Image.open(BytesIO(list_of_images[3][0]))
binary_img5   = Image.open(BytesIO(list_of_images[4][0]))
binary_img6   = Image.open(BytesIO(list_of_images[5][0]))
binary_img7   = Image.open(BytesIO(list_of_images[6][0]))
binary_img8   = Image.open(BytesIO(list_of_images[7][0]))
binary_img9   = Image.open(BytesIO(list_of_images[8][0]))
binary_img10  = Image.open(BytesIO(list_of_images[9][0]))
binary_img11  = Image.open(BytesIO(list_of_images[10][0]))
binary_img12  = Image.open(BytesIO(list_of_images[11][0]))
binary_img13  = Image.open(BytesIO(list_of_images[12][0]))
binary_img14  = Image.open(BytesIO(list_of_images[13][0]))
binary_img15  = Image.open(BytesIO(list_of_images[14][0]))

#Converting the binary data into IMAGE
profile_pic1  = ImageTk.PhotoImage(binary_img1)
profile_pic2  = ImageTk.PhotoImage(binary_img2)
profile_pic3  = ImageTk.PhotoImage(binary_img3)
profile_pic4  = ImageTk.PhotoImage(binary_img4)
profile_pic5  = ImageTk.PhotoImage(binary_img5)
profile_pic6  = ImageTk.PhotoImage(binary_img6)
profile_pic7  = ImageTk.PhotoImage(binary_img7)
profile_pic8  = ImageTk.PhotoImage(binary_img8)
profile_pic9  = ImageTk.PhotoImage(binary_img9)
profile_pic10 = ImageTk.PhotoImage(binary_img10)
profile_pic11 = ImageTk.PhotoImage(binary_img11)
profile_pic12 = ImageTk.PhotoImage(binary_img12)
profile_pic13 = ImageTk.PhotoImage(binary_img13)
profile_pic14 = ImageTk.PhotoImage(binary_img14)
profile_pic15 = ImageTk.PhotoImage(binary_img15)
