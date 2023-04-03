import tkinter
import tkcalendar
from tkinter import messagebox
import datetime
import sqlite3
import backend

selected_row = tuple()
previous_selected_rows = tuple()
current_selected_rows = tuple()
ids = list() #contains a list of IDs which is displayed in the Listbox
columnno = 2

def sort_data(buttonname,column,asc_or_desc):  #to sort the data in Listbox in a certain order
    global ids
    global columnno
    query = "1 = 1 "
    id_list = []
    for idno in ids:
        query += "OR Id = ? "
        id_list.append(idno[0])
    query += 'ORDER BY ' + column + ' ' + asc_or_desc
    if buttonname['text'] == 'Username' :
        columnno = 1
    elif buttonname['text'] == 'Date' :
        columnno = 2
    elif buttonname['text'] == 'Score' :
        columnno = 3
    elif buttonname['text'] == 'Snake Color' :
        columnno = 4
    elif buttonname['text'] == 'Level' :
        columnno = 5
    elif buttonname['text'] == 'Time (secs)' :
        columnno = 6
    elif buttonname['text'] == 'Username' :
        columnno = 7
    if asc_or_desc == 'ASC':
        hover_arrow.config(text='▲')
        buttonname.config(command=lambda: sort_data(buttonname,column,'DESC'))
    else:
        hover_arrow.config(text='▼')
        buttonname.config(command=lambda: sort_data(buttonname,column,'ASC'))
    hover_arrow.grid_forget()
    hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5)
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT username, date, score, snakecolor, level, time_taken FROM game_records WHERE " + query, id_list )
    data = backend.formatdata(cur.fetchall())
    listbox.delete(0,'end')
    for i in range(len(data)):
        data[i] = (str((i+1)).zfill(2) + ' ' * (6-len(str((i+1)).zfill(2))) + data[i])
        listbox.insert('end',(data[i]))
    conn.commit()
    conn.close()
    clear_selected()

def select_row(event):
    hide_calendar()
    global selected_row
    global previous_selected_rows
    global current_selected_rows

    current_selected_rows = listbox.curselection()
    try:
        index = current_selected_rows[0]
    except :
        clearall()
        return
        
    if len(selected_row) == 0 :
        previous_selected_rows = listbox.curselection()

    if len(previous_selected_rows) < len(current_selected_rows):
        for i in range(len(previous_selected_rows)):
            if current_selected_rows[i] != previous_selected_rows[i] :
                previous_selected_rows = current_selected_rows
                index = (current_selected_rows[i])
                break
        else:
            previous_selected_rows = current_selected_rows
            index = (current_selected_rows[-1])

    elif len(previous_selected_rows) > len(current_selected_rows):
        for i in range(len(current_selected_rows)):
            if previous_selected_rows[i] != current_selected_rows[i] :
                previous_selected_rows = list(current_selected_rows)
                previous_selected_rows.remove(current_selected_rows[i])
                previous_selected_rows = tuple(previous_selected_rows)
                index = (current_selected_rows[i])
                break
        else:
            previous_selected_rows = list(previous_selected_rows)
            previous_selected_rows.pop()
            previous_selected_rows = tuple(previous_selected_rows)
            index = previous_selected_rows[-1]

    selected_row = listbox.get(index).split()
    e1.delete(0,'end')
    e1.insert('end',selected_row[1])
    e2.delete(0,'end')
    e2.insert('end',selected_row[2])
    e3.delete(0,'end')
    e3.insert('end',selected_row[3])
    e4.delete(0,'end')
    e4.insert('end',selected_row[4])
    e5['text'] = selected_row[5]
    e6.delete(0,'end')
    e6.insert('end',selected_row[6])

def deletedata_from_db():
    global ids
    global current_selected_rows
    for i in range(len(ids)):
        if i in current_selected_rows:
            backend.delete(ids[i][0])

def call_delete():
    global current_selected_rows
    if len(current_selected_rows) == 0 :
        tkinter.messagebox.showerror("Snake_Game",'\tSelect a row to delete\t')
    else:
        deletedata_from_db()
        for i in current_selected_rows[::-1]:
            listbox.delete(i)
        messagebox.showinfo('Snake_Game','The selected row has been successfully deleted')
        e1.delete(0,'end')
        e2.delete(0,'end')
        e3.delete(0,'end')
        e4.delete(0,'end')
        e5['text'] = ' '
        e6.delete(0,'end')
        listbox.config(state='normal')
    clear_selected()

def call_view():
    global ids
    listbox.delete(0,'end')
    data = backend.formatdata(backend.view()[1])
    ids = backend.view()[0]
    for i in range(len(data)):
        data[i] = (str((i+1)).zfill(2) + ' ' * (6-len(str((i+1)).zfill(2))) + data[i])
        listbox.insert('end',(data[i]))
    clear_selected()

def call_search(*args):
    global ids
    listbox.delete(0,'end')
    data = backend.formatdata(backend.search(name_txt.get(),date_txt.get(),score_int.get(),snakecolor_txt.get(),e5['text'],timetaken_txt.get())[1])
    ids  = backend.search(name_txt.get(),date_txt.get(),score_int.get(),snakecolor_txt.get(),e5['text'],timetaken_txt.get())[0]
    for i in range(len(data)):
        data[i] = (str((i+1)).zfill(2) + ' ' * (6-len(str((i+1)).zfill(2))) + data[i])
        listbox.insert('end',(data[i]))
    index = listbox.index("end")
    if index == 0 and (e1.get() != '' or e2.get() != ''  or e3.get() != ''  or e4.get() != '' or e5['text'] != '' or e6.get() != '' ):
        messagebox.showerror('Snake_Game',"\tNo results found\t\t")
    clear_selected()
def clearall():
    e1.delete(0,'end')
    e2.delete(0,'end')
    e3.delete(0,'end')
    e4.delete(0,'end')
    e5['text'] = ' '
    e6.delete(0,'end')

def close_program():
    listbox.config(state='disabled')
    MsgBox = messagebox.askquestion('Snake_Game','Are you sure you want to exit the application',icon = 'info')
    if MsgBox == 'yes':
       root.destroy()
    else:
        listbox.config(state='normal')

def clear_selected():
    global selected_row
    global current_selected_rows
    current_selected_rows = tuple()
    selected_row = tuple()
    listbox.selection_clear(0, 'end')

def change_selectmode():
    if b3['text'][1:7] == 'Single' :
        b3.config(text=' Multiple',image=multi_select_image,padx=9,pady=0)
        listbox.config(selectmode='multiple')
    else:
        b3.config(text=' Single  ',image=single_select_image,padx=11,pady=4)
        listbox.config(selectmode='browse')

def change_level_button():
    if e5['text'] == ' ':
        e5['text'] = 'All'
    elif e5['text'] == 'All':
        e5['text'] = 'Easy'
    elif e5['text'] == 'Easy':
        e5['text'] = 'Medium'
    elif e5['text'] == 'Medium':
        e5['text'] = 'Hard'
    elif e5['text'] == 'Hard':
        e5['text'] = 'All'

def get_date():
    date_txt.set(calendar.get_date())
def hide_calendar(*args):
    calendar_frame.place_forget()
    b7.config(command=show_calendar)
def show_calendar():
    hover_label.place_forget()
    calendar_frame.place(x=630,y=180)
    b7.config(command=hide_calendar)

# Getting screen width and height
from win32api import GetSystemMetrics

screen_width  =  GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

# Initiating a tkinter screen
root = tkinter.Tk()
root.geometry(f'920x700+{((screen_width-920)//2)-7}+0')
root.title('Snake_Game')
root.resizable(0,0)
from defined_constants import (black, white, color1, calendar_image, clearall_image,
                               delete_image, exit_image, game_icon, search_image, viewall_image, single_select_image, multi_select_image)

root.configure(bg=black)
root.iconphoto(False, game_icon)

label = tkinter.Label(root,text='SNAKE_GAME - DATABASE',font=('Castellar',35),fg=white,bg=black)
label.place(x=120,y=30)

# Labels for Entries
l1 = tkinter.Label(root, text='Username',font=('Montserrat',18),bg=black,fg=white)
l1.place(x=60,y=140)
l2 = tkinter.Label(root, text='Date  Played',font=('Montserrat',18),bg=black,fg=white)
l2.place(x=500,y=140)
l3 = tkinter.Label(root, text='Score',font=('Montserrat',18),bg=black,fg=white)
l3.place(x=60,y=180)
l4 = tkinter.Label(root, text='Snakecolor',font=('Montserrat',18),bg=black,fg=white)
l4.place(x=500,y=180)
l5 = tkinter.Label(root, text='Level',font=('Montserrat',18),bg=black,fg=white)
l5.place(x=60,y=220)
l6 = tkinter.Label(root, text='Time (secs)',font=('Montserrat',18),bg=black,fg=white)
l6.place(x=500,y=220)


# Entry boxes
name_txt = tkinter.StringVar()
e1 = tkinter.Entry(root, textvariable=name_txt,font=('Anonymous Pro',15),width=17,bg=white,selectbackground=color1)
e1.place(x=200,y=150)

date_txt = tkinter.StringVar()
e2 = tkinter.Entry(root, textvariable=date_txt,font=('Anonymous Pro',15),width=17,bg=white,selectbackground=color1)
e2.place(x=670,y=150)

score_int = tkinter.StringVar()
e3 = tkinter.Entry(root, textvariable=score_int,font=('Anonymous Pro',15),width=17,bg=white,selectbackground=color1)
e3.place(x=200,y=190)

snakecolor_txt = tkinter.StringVar()
e4 = tkinter.Entry(root, textvariable=snakecolor_txt,font=('Anonymous Pro',15),width=17,bg=white,selectbackground=color1)
e4.place(x=670,y=190)

e5 = tkinter.Button(root,text=' ',font=('Anonymous Pro',12),pady=0,width=17,padx=15,bg=white,command=change_level_button)
e5.place(x=200,y=230)

timetaken_txt = tkinter.StringVar()
e6 = tkinter.Entry(root, textvariable=timetaken_txt,font=('Anonymous Pro',15),width=17,bg=white,selectbackground=color1)
e6.place(x=670,y=230)

# Making a Canvas for listbox
listbox_temp_frame = tkinter.Frame(root,bg=black,borderwidth=0)
canvas = tkinter.Canvas(listbox_temp_frame,bg=black,width=575,height=340)
canvas_sb = tkinter.Scrollbar(listbox_temp_frame,orient='horizontal',width=15)
canvas_sb.pack(side='bottom',fill='x')
listbox_frame = tkinter.Frame(canvas)
listbox_frame.bind("<Configure>",lambda e:canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0,0),window=listbox_frame,anchor='nw')
canvas.configure(xscrollcommand=canvas_sb.set)
canvas_sb.config(command= canvas.xview)

sb1 = tkinter.Scrollbar(listbox_temp_frame,width=15)
sb1.pack(side='right',fill='y')
listbox_temp_frame.place(x=50,y=315)
canvas.pack(fill='both',expand=True)

# Buttons for listbox
listbox_buttons_frame = tkinter.Frame(listbox_frame,bg=black)
lb1 = tkinter.Button(listbox_buttons_frame,text='Serial No',width=10,bg=white)
lb2 = tkinter.Button(listbox_buttons_frame,text='Username',width=32,bg=white,
                        command=lambda: sort_data(lb2,'username','ASC'))
lb3 = tkinter.Button(listbox_buttons_frame,text='Date',width=23,bg=white,
                        command=lambda: sort_data(lb3,'date','DESC'))
lb4 = tkinter.Button(listbox_buttons_frame,text='Score',width=12,bg=white,
                        command=lambda: sort_data(lb4,'score','ASC'))
lb5 = tkinter.Button(listbox_buttons_frame,text='Snake Color',width=29,bg=white,
                        command=lambda: sort_data(lb5,'snakecolor','ASC'))
lb6 = tkinter.Button(listbox_buttons_frame,text='Level',width=18,bg=white,
                        command=lambda: sort_data(lb6,'level','ASC'))
lb7 = tkinter.Button(listbox_buttons_frame,text='Time (secs)',width=16,bg=white,
                        command=lambda: sort_data(lb7,'time_taken','ASC'))
hover_arrow = tkinter.Label(listbox_buttons_frame,text='▲',bg=white)

lb1.grid(row=0,column=0)
lb2.grid(row=0,column=1)
lb3.grid(row=0,column=2)
lb4.grid(row=0,column=3)
lb5.grid(row=0,column=4)
lb6.grid(row=0,column=5)
lb7.grid(row=0,column=6)
listbox_buttons_frame.pack()

# Listbox
listbox = tkinter.Listbox(listbox_frame,height=12,width=35,font=('Courier New',17),bg=white,activestyle='none',
                            selectbackground=color1,yscrollcommand=sb1.set,selectmode='browse')
listbox.pack(fill='both',expand=True)
sb1.config(command= listbox.yview)

# Buttons
b1 = tkinter.Button(root,text=' Search  ',font=('OCR A Extended',15),image=search_image,compound = 'left',padx=20,pady=8,command=call_search,bd=4)
b2 = tkinter.Button(root,text=' Delete  ',font=('OCR A Extended',15),image=delete_image,compound = 'left',padx=20,pady=8,command=call_delete,bd=4)
b3 = tkinter.Button(root,text=' Single  ',font=('OCR A Extended',15),image=single_select_image,compound = 'left',padx=11,pady=4,command = change_selectmode,bd=4)
b4 = tkinter.Button(root,text='View all ',font=('OCR A Extended',15),image=viewall_image,compound = 'left',padx=20,pady=8,command=call_view,bd=4)
b5 = tkinter.Button(root,text='Clear All',font=('OCR A Extended',15),image=clearall_image,compound = 'left',padx=20,pady=8,command=clearall,bd=4)
b6 = tkinter.Button(root,text=' Close   ',font=('OCR A Extended',15),image=exit_image,compound = 'left',padx=20,pady=8,command=close_program,bd=4)
b7 = tkinter.Button(root,image=calendar_image,bg=white,activebackground=white,borderwidth=0,command=show_calendar)

b1.place(x=660,y=315)
b2.place(x=660,y=375)
b3.place(x=660,y=435)
b4.place(x=660,y=495)
b5.place(x=660,y=555)
b6.place(x=660,y=615)
b7.place(x=835,y=151)

# Calendar frame
calendar_frame = tkinter.Frame(root,bg=black,bd=5,borderwidth=5)
calendar = tkcalendar.Calendar(calendar_frame,font=('JetBrains Mono',10),cursor='tcross',selectmode='day',
year=datetime.datetime.now().year,month=datetime.datetime.now().month,day=datetime.datetime.now().day,
showweeknumbers=False,showothermonthdays=False,firstweekday='sunday',date_pattern='yyyy-mm-dd',
selectbackground=color1,normalbackground=white,weekendbackground=white,normalforeground=black,weekendforeground=black)
select_date_button = tkinter.Button(calendar_frame,text='Select',font=('Anonymous Pro',12),width=13,command=get_date)
close_calendar_button = tkinter.Button(calendar_frame,text='Close',font=('Anonymous Pro',12),width=13,command=hide_calendar)

calendar.grid(row=0,column=0,columnspan=2)
select_date_button.grid(row=1,column=0)
close_calendar_button.grid(row=1,column=1)


# Keybindings
root.bind('<Return>',call_search)
listbox.bind('<<ListboxSelect>>',select_row)
listbox.bind("<Left>", lambda e: canvas.xview_scroll(-1, 'units'))
listbox.bind("<Right>", lambda e: canvas.xview_scroll(1, 'units'))
label.bind('<Button-1>',hide_calendar)
e1.bind('<Button-1>',hide_calendar)
e3.bind('<Button-1>',hide_calendar)
e4.bind('<Button-1>',hide_calendar)
e5.bind('<Button-1>',hide_calendar)
e6.bind('<Button-1>',hide_calendar)
b1.bind('<Button-1>',hide_calendar)
b2.bind('<Button-1>',hide_calendar)
b4.bind('<Button-1>',hide_calendar)
b5.bind('<Button-1>',hide_calendar)
b6.bind('<Button-1>',hide_calendar)
lb1.bind('<Button-1>',hide_calendar)
lb2.bind('<Button-1>',hide_calendar)
lb3.bind('<Button-1>',hide_calendar)
lb4.bind('<Button-1>',hide_calendar)
lb5.bind('<Button-1>',hide_calendar)
lb6.bind('<Button-1>',hide_calendar)
lb7.bind('<Button-1>',hide_calendar)


hover_label = tkinter.Label(root,text='  Calendar  ')
b7.bind('<Enter>', lambda e: root.after(1000,hover_label.place(x=e.x+835+5,y=e.y+151+5)))
b7.bind('<Leave>', lambda e: root.after(200,hover_label.place_forget()))
lb1.bind('<Enter>',lambda e: hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5))
lb2.bind('<Enter>',lambda e: hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5))
lb3.bind('<Enter>',lambda e: hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5))
lb4.bind('<Enter>',lambda e: hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5))
lb5.bind('<Enter>',lambda e: hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5))
lb6.bind('<Enter>',lambda e: hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5))
lb7.bind('<Enter>',lambda e: hover_arrow.grid(row=0,column=columnno,sticky='e',padx=5))
lb1.bind('<Leave>',lambda e: hover_arrow.grid_forget())
lb2.bind('<Leave>',lambda e: hover_arrow.grid_forget())
lb3.bind('<Leave>',lambda e: hover_arrow.grid_forget())
lb4.bind('<Leave>',lambda e: hover_arrow.grid_forget())
lb5.bind('<Leave>',lambda e: hover_arrow.grid_forget())
lb6.bind('<Leave>',lambda e: hover_arrow.grid_forget())
lb7.bind('<Leave>',lambda e: hover_arrow.grid_forget())

call_view()
root.protocol("WM_DELETE_WINDOW", close_program)
root.mainloop()