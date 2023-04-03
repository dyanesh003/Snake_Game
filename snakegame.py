import turtle
import time
import random
import datetime
from tkinter import Tk,messagebox
from backend import insert,current_userdata,get_highscore


# Getting data from the database
if len(current_userdata()[1]) == 0:
    root = Tk()
    root.withdraw()
    messagebox.showinfo('Snake_Game','\tRun main.py\t\t')
    quit()
current_userdata = current_userdata()
snakecolor_hex = current_userdata[3]
food = current_userdata[4]
level = current_userdata[5]
controls = current_userdata[6]
highscore = get_highscore(level)
if highscore == None:
    highscore = 0

# Defining Variables
score = 0
segments = []
running = True
snake_moved = False
timetaken = datetime.datetime(1,1,1)

# Setup the screen
wn = turtle.Screen()
wn.title('Snake_Game')
wn.setup(width=1200, height=600)
from defined_constants import black1,pure_white
wn.bgcolor(black1)
canvas = wn.getcanvas()
root = canvas.winfo_toplevel()
wn.tracer(0)

# Snake head
head = turtle.Turtle()
head.speed(0)
head.shape('square')
head.penup()
head.setpos(0,-50)
head.direction = 'stop'

# Snake food
def get_foodpic(food) -> str:
    x = 'snakegame_food\\'
    for i in food :
        if i == '_' :
            x += ' '
        else:
            x += i
    x += '.gif'
    return x
food_image = get_foodpic(food)
wn.addshape(food_image)
food = turtle.Turtle()
food.speed(0)
food.shape(food_image)
food.penup()
food.setpos(0,100)

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape('square')
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

#  Functions for moving the snake
def go_up():
    if head.direction != 'down':
        head.direction = 'up'
def go_down():
    if head.direction != 'up':
        head.direction = 'down'
def go_left():
    if head.direction != 'right':
        head.direction = 'left'
def go_right():
    if head.direction != 'left':
        head.direction = 'right'

def move():
    if head.direction == 'up':
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == 'down':
        y = head.ycor()
        head.sety(y - 20)
        
    if head.direction == 'left':
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == 'right':
        x = head.xcor()
        head.setx(x + 20)


 # Resetting the game
def game_over():
    global current_userdata
    global score
    global highscore
    global timetaken

    gameover_pen=turtle.Turtle()
    gameover_pen.speed(0)
    gameover_pen.shape('square')
    gameover_pen.color(pure_white)
    gameover_pen.penup()
    gameover_pen.hideturtle()
    gameover_pen.setpos(0,50)
    gameover_pen.write('GAME OVER!',align='center' , font=('ProfontWindows',64,'normal'))
    pen.penup()
    pen.hideturtle()
    pen.setpos(0,-10)
    pen.write(f'SCORE: {score} ', align='center', font=('ProfontWindows', 36, 'normal'))
    date=str(datetime.date.today())
    timetaken = round(timetaken.total_seconds(),2)
    insert(current_userdata[1],date,score,current_userdata[2],current_userdata[5],timetaken,current_userdata[0])

    time.sleep(2)
    gameover_pen.clear()
    pen.clear()
    pen.setpos(0,260)
    score=0
    time.sleep(1)
    head.setpos(0,-50)
    food.setpos(0,100)
    head.showturtle()
    food.showturtle()
    pen.write(f'SCORE: {score}  HIGH SCORE: {highscore}', align='center', font=('ProfontWindows', 30, 'normal'))
    head.direction='stop'


# Press Space to Start
text_turtle = turtle.Turtle()
text_turtle.color(pure_white)
text_turtle.goto(0,-30)
text_turtle.write('PRESS SPACE TO START',align='center',font=('ProFontWindows',64))
text_turtle.hideturtle()
head.color(snakecolor_hex)
pen.color(pure_white)
time_started = datetime.datetime(1,1,1)

# Main game
def start_game():
    global score
    global level
    global highscore
    global snakecolor_hex
    global timetaken
    global time_started
    global running
    global snake_moved
    
    delay = 0.1
    text_turtle.clear()
    wn.onkeypress(None, 'space')
    pen.write(f'SCORE: {score}  HIGH SCORE: {highscore}', align='center', font=('ProfontWindows', 30, 'normal'))

    while running:
        if head.direction == 'stop' :
            time_started = datetime.datetime.now()

        # Checking if snake eats the food
        if head.distance(food) < 20:
            x = random.randint(-590, 590)
            y = random.randint(-290, 290)
            food.goto(x,y)

            # Add a segment
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape('square')
            new_segment.color(snakecolor_hex)
            new_segment.penup()
            segments.append(new_segment)

            # Shorten the delay
            if level == 'Easy' :
                if score <= 500:
                    delay -= 0.001
                else:
                    delay -= 0.002

            elif level == 'Medium' :
                if score <= 200:
                    delay -= 0.001
                elif score <= 400:
                    delay -= 0.002
                elif score <= 600:
                    delay -= 0.003
                
            elif level == 'Hard' :
                if score <= 150:
                    delay -= 0.001
                elif score <= 300:
                    delay -= 0.002
                elif score <= 450:
                    delay -= 0.003
                elif score <= 600:
                    delay -= 0.004
            
            score += 10
            if score > highscore:
                highscore = score

            pen.clear()
            pen.write(f'SCORE: {score}  HIGH SCORE: {highscore}', align='center', font=('ProfontWindows', 30, 'normal'))

        # Check for a collision with the border
        if head.xcor()>590 or head.xcor()< -590 or head.ycor()>290 or head.ycor()< -290:
            head.direction = 'stop'
            time.sleep(2)
            time_ended=datetime.datetime.now()
            timetaken = time_ended - time_started

            # Hide the segments
            for segment in segments:
                segment.setpos(5000,5000)

            segments.clear()
            delay = 0.1
            pen.clear()
            game_over()

        # Check for head collision with the body segments
        for segment in segments:
            if segment.distance(head) < 20:
                time.sleep(2)
                head.setpos(0,0)
                head.direction = 'stop'
                time_ended = datetime.datetime.now()
                timetaken = time_ended - time_started

                # Hide the segments
                for segment in segments:
                    segment.setpos(5000, 5000)

                segments.clear()
                delay = 0.1
                pen.clear()
                game_over()

        # Move the end segments first in reverse order
        for i in range(len(segments)-1, 0, -1):
            x = segments[i-1].xcor()
            y = segments[i-1].ycor()
            segments[i].goto(x, y)

        # Move segment 0 to where the head is
        if len(segments) > 0:
            x = head.xcor()
            y = head.ycor()
            segments[0].goto(x,y)

        move()
        time.sleep(delay)
        wn.update()

def close_program():
    MsgBox = messagebox.askquestion('Snake_Game','Are you sure you want to exit the application',icon = 'info')
    if MsgBox == 'yes':
        global running
        running = False
        wn.bye()

# Keybindings
if controls == 'Arrow Keys' :
    wn.onkeypress(go_up, 'Up')
    wn.onkeypress(go_down, 'Down')
    wn.onkeypress(go_left, 'Left')
    wn.onkeypress(go_right, 'Right')

elif controls == 'W A S D' :
    wn.onkeypress(go_up, 'w')
    wn.onkeypress(go_down, 's')
    wn.onkeypress(go_left, 'a')
    wn.onkeypress(go_right, 'd')
wn.onkeypress(start_game, 'space')

wn.listen()
root.protocol("WM_DELETE_WINDOW", close_program)
wn.mainloop()
