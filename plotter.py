import tkinter
from tkinter import ttk,messagebox
import datetime
import sqlite3
import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import sys
from cefpython3 import cefpython as cef

# Extracting data from the database
conn = sqlite3.connect("snakegame_db.db")
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM game_records")
no_of_rows = cur.fetchall()[0][0]
df = pd.read_sql_query("SELECT username, score, snakecolor, level, time_taken FROM game_records ORDER BY Id;", conn)
df = df.rename(columns={'username':'Name', 'score':'Score', 'snakecolor':'Snake Color', 'level':'Level', 'time_taken':'Time Taken(secs)'}) 
date_df = pd.read_sql_query("SELECT date FROM game_records ORDER BY Id;",conn)

date_list    = []
year_list    = []
month_list   = []
day_listnum  = []
day_listname = []
for i in range(no_of_rows):
    date_list.append([int(str(date_df.iloc[i])[8:12]),int(str(date_df.iloc[i])[13:15]),int(str(date_df.iloc[i])[16:18])])
for i in date_list:
    x = datetime.datetime(i[0],i[1],i[2])
    year_list.append(i[0])
    month_list.append(x.strftime('%b'))
    day_listname.append(x.strftime('%a'))
    day_listnum.append(int(x.strftime('%d')))
date_data = {'Year':year_list,'Month':month_list,'Day(num)':day_listnum,'Day(name)':day_listname}
date_df = pd.DataFrame(date_data)
df = pd.concat([df,date_df],axis=1)

conn.commit()
conn.close()

# Defining variables
w,h = 0,0
x_label = ''
y_label = ''
discrete = []
orient = ''
marginalx = ''
marginaly = ''
points = ''

# Getting screen width and height
from win32api import GetSystemMetrics

screen_width  =  GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)

# Creating a Tkinter Window
root = tkinter.Tk()
root.geometry(f'470x350+{((screen_width-900)//2)}+{((screen_height-650)//2)}')
root.resizable(0,0)
root.title('Snake_Game')
from defined_constants import black, game_icon, settings_image, white

root.configure(bg=black)
root.iconphoto(True, game_icon)
root.tk.call('wm', 'iconphoto', root._w, game_icon)

l1 = tkinter.Label(root,text='Snake_Game - Plotter',font=('Castellar',25),pady=10,bg=black,fg=white)
l1.place(x=5,y=20)

plot_type = tkinter.StringVar()
l2 = tkinter.Label(root,text='Select Plot Type',font=('Montserrat',15),pady=10,bg=black,fg=white)
l2.place(x=30,y=100)
c1 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=plot_type)
c1['values'] = ('line','scatter','bar','histogram','box','pie','heatmap','violin','area',
'line polar','scatter polar','wind rose')
c1.bind("<Key>","pass")
c1.place(x=230,y=115)
c1.current(0)

x_change = tkinter.StringVar()
x_change.set('Select X-Axis')
x = tkinter.StringVar()
l3 = tkinter.Label(root,textvariable=x_change,font=('Montserrat',15),pady=10,bg=black,fg=white)
l3.place(x=30,y=150)
c2 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=x)
c2['values'] = df.columns.tolist()
c2.bind("<Key>","pass")
c2.place(x=230,y=165)
c2.current(0)

y_change = tkinter.StringVar()
y_change.set('Select Y-Axis')
y = tkinter.StringVar()
l4 = tkinter.Label(root,textvariable=y_change,font=('Montserrat',15),pady=10,bg=black,fg=white)
l4.place(x=30,y=200)
c3 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=y)
c3['values'] = df.columns.tolist()
c3.bind("<Key>","pass")
c3.place(x=230,y=215)
c3.current(1)

color_change = tkinter.StringVar()
color_change.set('Select Hover')
color = tkinter.StringVar()
l5 = tkinter.Label(root,textvariable=color_change,font=('Montserrat',15),pady=10,bg=black,fg=white)
l5.place(x=30,y=250)
c4 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=color)
c4['values'] = df.columns.tolist()
c4.bind("<Key>","pass")
c4.place(x=230,y=265)
c4.current(3)

template = tkinter.StringVar()
l6 = tkinter.Label(root,text="Select Template",font=('Montserrat',15),pady=10,bg=black,fg=white)
l6.place(x=500,y=100)
c5 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=template)
c5['values'] = ('ggplot2', 'seaborn', 'simple_white', 'plotly','plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         'ygridoff', 'gridon', 'none')
c5.bind("<Key>","pass")
c5.place(x=700,y=115)
c5.current(4)

xlabel = tkinter.StringVar()
xlabel.set('default')
l7 = tkinter.Label(root,text='Change X-Label',font=('Montserrat',15),pady=10,bg=black,fg=white)
l7.place(x=500,y=150)
c6 = tkinter.Entry(root,width=17,font=('Anonymous Pro',12),textvariable=xlabel)
c6.place(x=700,y=165)

ylabel = tkinter.StringVar()
ylabel.set('default')
l8 = tkinter.Label(root,text='Change Y-Label',font=('Montserrat',15),pady=10,bg=black,fg=white)
l8.place(x=500,y=200)
c7 = ttk.tkinter.Entry(root,width=17,font=('Anonymous Pro',12),textvariable=ylabel)
c7.place(x=700,y=215)

color_scale = tkinter.StringVar()
l9 = tkinter.Label(root,text='Color Scale',font=('Montserrat',15),pady=10,bg=black,fg=white)
l9.place_forget()
c8 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=color_scale)
c8['values'] = ('aggrnyl','agsunset','blackbody','bluered','blues','blugrn','bluyl','brwnyl','bugn','bupu','burg',
'burgyl','cividis','darkmint','electric','emrld','gnbu','greens','greys','hot','inferno','jet','magenta','magma',
'mint','orrd','oranges','oryel','peach','pinkyl','plasma','plotly3','pubu','pubugn','purd','purp','purples',
'purpor','rainbow','rdbu','rdpu','redor','reds','sunset','sunsetdark','teal','tealgrn','viridis','ylgn','ylgnbu',
'ylorbr','ylorrd','algae','amp','deep','dense','gray','haline','ice','matter','solar','speed','tempo','thermal',
'turbid','armyrose','brbg','earth','fall','geyser','prgn','piyg','picnic','portland','puor','rdgy','rdylbu',
'rdylgn','spectral','tealrose','temps','tropic','balance','curl','delta','edge','hsv','icefire','phase',
'twilight','mrybm','mygbm')
c8.bind("<Key>","pass")
c8.current(10)

discrete_scale = tkinter.StringVar()
c12 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=discrete_scale)
c12['values'] = ('Plotly','G10','T10','Alphabet','Dark24','Light24','D3','Vivid','Safe','Prism','Pastel','Bold',
'Antique','Set3','Pastel2','Set2','Dark2','Pastel1','Set1')
c12.bind("<Key>","pass")
c12.current(0)

trendline = tkinter.StringVar()
l10 = tkinter.Label(root,text='Trendlines',font=('Montserrat',15),pady=10,bg=black,fg=white)
c9 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=trendline)
c9['values'] = (None,'ols','lowess')
c9.bind("<Key>","pass")
c9.current(0)

marginal_x = tkinter.StringVar()
l11 = tkinter.Label(root,text='Marginal_X Graph',font=('Montserrat',15),pady=10,bg=black,fg=white)
c10 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=marginal_x)
c10['values'] = ('None','rug','box','violin','histogram')
c10.bind("<Key>","pass")
c10.current(0)

marginal_y = tkinter.StringVar()
l12 = tkinter.Label(root,text='Marginal_Y Graph',font=('Montserrat',15),pady=10,bg=black,fg=white)
c11 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=marginal_y)
c11['values'] = ('None','rug','box','violin','histogram')
c11.bind("<Key>","pass")
c11.current(0)

barmode = tkinter.StringVar()
l13 = tkinter.Label(root,text='Barmode',font=('Montserrat',15),pady=10,bg=black,fg=white)
c13 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=barmode)
c13['values'] = ('relative','stack','group')
c13.bind("<Key>","pass")
c13.current(0)

orientation = tkinter.StringVar()
l14 = tkinter.Label(root,text='Orientation',font=('Montserrat',15),pady=10,bg=black,fg=white)
c14 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=orientation)
c14['values'] = ('horizontal','vertical')
c14.bind("<Key>","pass")
c14.current(1)

opacity = tkinter.DoubleVar()
l15 = tkinter.Label(root,text='Transparency',font=('Montserrat',15),pady=10,bg=black,fg=white)
c15 = ttk.Spinbox(root,from_=0,to=100,increment=5,width=15,font=('Anonymous Pro',12),textvariable=opacity)
c15.bind("<Key>","pass")

direction = tkinter.StringVar()
l16 = tkinter.Label(root,text='Direction',font=('Montserrat',15),pady=10,bg=black,fg=white)
c16 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=direction)
c16['values'] = ('clockwise','counterclockwise')
c16.bind("<Key>","pass")
c16.place_forget()
c16.current(0)

start_angle = tkinter.IntVar()
l17 = tkinter.Label(root,text='Start Angle',font=('Montserrat',15),pady=10,bg=black,fg=white)
c17 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=start_angle)
c17['values'] = (0,45,90,135,180,225,270,315)
c17.bind("<Key>","pass")
c17.current(0)

box_mode = tkinter.StringVar()
l18 = tkinter.Label(root,text='Box Mode',font=('Montserrat',15),pady=10,bg=black,fg=white)
c18 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=box_mode)
c18['values'] = ('group','overlay')
c18.bind("<Key>","pass")
c18.current(0)

point_s = tkinter.StringVar()
l19 = tkinter.Label(root,text='Points',font=('Montserrat',15),pady=10,bg=black,fg=white)
c19 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=point_s)
c19['values'] = ('False','outliers','suspectedoutliers','all')
c19.bind("<Key>","pass")
c19.current(0)

hole = tkinter.DoubleVar()
l20 = tkinter.Label(root,text='Donut',font=('Montserrat',15),pady=10,bg=black,fg=white)
c20 = ttk.Spinbox(root,from_=0,to=1,increment=.1,width=15,font=('Anonymous Pro',12),textvariable=hole)
c20.bind("<Key>","pass")

text_position = tkinter.StringVar()
l21 = tkinter.Label(root,text='Text Position',font=('Montserrat',15),pady=10,bg=black,fg=white)
c21 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=text_position)
c21['values'] = ('inside','outside')
c21.bind("<Key>","pass")
c21.current(0)

text_info = tkinter.StringVar()
l22 = tkinter.Label(root,text='Text Info',font=('Montserrat',15),pady=10,bg=black,fg=white)
c22 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=text_info)
c22['values'] = ('percent','percent+label','percent+label+value','percent+label+text','none')
c22.bind("<Key>","pass")
c22.current(0)

box_needed = tkinter.BooleanVar()
l23 = tkinter.Label(root,text='Box',font=('Montserrat',15),pady=10,bg=black,fg=white)
c23 = ttk.Combobox(root,width=15,font=('Anonymous Pro',12),textvariable=box_needed)
c23['values'] = (True,False)
c23.bind("<Key>","pass")
c23.current(0)

sep = ttk.Separator(root, orient='horizontal')

def normalit():
    root.geometry('470x350')
    l1.config(font=('Castellar',25))
    l1.place(x=5,y=20)
    b1.place(x=380,y=320)
    b3.place_forget()
    b2.place(x=10,y=320)
    c1.config(state='normal')
    c2.config(state='normal')
    c3.config(state='normal')
    c4.config(state='normal')
    c9.current(0)
    l9.place_forget()
    l10.place_forget()
    l11.place_forget()
    l11.place_forget()
    l12.place_forget()
    l13.place_forget()
    l14.place_forget()
    l15.place_forget()
    l16.place_forget()
    l17.place_forget()
    l18.place_forget()
    l19.place_forget()
    l20.place_forget()
    l21.place_forget()
    l22.place_forget()
    c8.place_forget()
    c9.place_forget()
    c10.place_forget()
    c10.place_forget()
    c11.place_forget()
    c12.place_forget()
    c13.place_forget()
    c14.place_forget()
    c15.place_forget()
    c16.place_forget()
    c17.place_forget()
    c18.place_forget()
    c19.place_forget()
    c20.place_forget()
    c21.place_forget()
    c22.place_forget()
    sep.place_forget()

def expand_it():
    root.geometry('900x350')
    l1.config(font=('Castellar',30))
    l1.place(x=180,y=5)
    b1.place_forget()
    b2.place_forget()
    b3.place(x=10,y=320)
    b4.place(x=800,y=320)
    b5.place(x=830, y=10)
    b6.place(x=550,y=260)
    c1.config(state='disabled')
    c2.config(state='disabled')
    c3.config(state='disabled')
    c4.config(state='disabled')
    
def check_plot(event):
    if c1.get() == 'pie' :
        x_change.set('Select Values')
        y_change.set('Select Names')
        l5.place(x=30,y=250)
        c4.place(x=230,y=265)
    elif c1.get() == 'heatmap' :
        l5.place_forget()
        c4.place_forget()
    elif c1.get() == 'line polar' or c1.get() == 'scatter polar' or c1.get() == 'wind rose':
        x_change.set('Select Radius')
        y_change.set('Select Theta')
        color_change.set('Select Hover')
        l5.place(x=30,y=250)
        c4.place(x=230,y=265)
    else:
        x_change.set('Select X-Axis')
        y_change.set('Select Y-Axis')
        color_change.set('Select Hover')
        l5.place(x=30,y=250)
        c4.place(x=230,y=265)

def check_color(event):
    global discrete
    if c12.get() == 'Plotly' :
        discrete = px.colors.qualitative.Plotly
    elif c12.get() == 'G10' :
        discrete = px.colors.qualitative.G10
    elif c12.get() == 'T10' :
        discrete = px.colors.qualitative.T10
    elif c12.get() == 'Alphabet' :
        discrete = px.colors.qualitative.Alphabet
    elif c12.get() == 'Dark24' :
        discrete = px.colors.qualitative.Dark24
    elif c12.get() == 'Light24' :
        discrete = px.colors.qualitative.Light24
    elif c12.get() == 'D3' :
        discrete = px.colors.qualitative.D3
    elif c12.get() == 'Vivid' :
        discrete = px.colors.qualitative.Vivid
    elif c12.get() == 'Safe' :
        discrete = px.colors.qualitative.Safe
    elif c12.get() == 'Prism' :
        discrete = px.colors.qualitative.Prism
    elif c12.get() == 'Pastel' :
        discrete = px.colors.qualitative.Pastel
    elif c12.get() == 'Bold' :
        discrete = px.colors.qualitative.Bold
    elif c12.get() == 'Antique' :
        discrete = px.colors.qualitative.Antique
    elif c12.get() == 'Set3' :
        discrete = px.colors.qualitative.Set3
    elif c12.get() == 'Pastel2' :
        discrete = px.colors.qualitative.Pastel2
    elif c12.get() == 'Set2' :
        discrete = px.colors.qualitative.Set2
    elif c12.get() == 'Dark2' :
        discrete = px.colors.qualitative.Dark2
    elif c12.get() == 'Pastel1' :
        discrete = px.colors.qualitative.Pastel1
    elif c12.get() == 'Set1' :
        discrete = px.colors.qualitative.Set1

def close_program():
    MsgBox = messagebox.askquestion('Snake_Game','Are you sure you want to exit the application',icon = 'info')
    if MsgBox == 'yes':
        cef.Shutdown()
        root.destroy()

def graph_window(filepath): #Showing the plotted graph using a cef window
    sys.excepthook = cef.ExceptHook
    cef.Initialize()
    cef.CreateBrowserSync(url="file:///"+os.getcwd().replace('\\','/') + '/' + filepath,window_title='Snake_Game')
    cef.MessageLoop()

def plotter():
    global w
    global h
    global x_label
    global y_label
    global xlabel
    global ylabel
    global discrete
    global orient
    global marginalx
    global marginaly
    fig = ''

    try:
        w = int(width.get())
    except:
        messagebox.showerror("Snake_Game",'Something went wrong in setting the width of the graph')
    try:
        h = int(height.get())
    except:
        messagebox.showerror("Snake_Game",'Something went wrong in setting the height of the graph')
    try:
        if len(discrete) == 0 :
            discrete = None
    except:
        pass
    if c14.get() == 'horizontal' :
        orient = 'h'
    elif c14.get() == 'vertical' :
        orient = 'v'
    if marginal_x.get() == 'None' :
        marginalx = None
    else:
        marginalx = marginal_x.get()
    if marginal_y.get() == 'None' :
        marginaly = None
    else:
        marginaly = marginal_y.get()
    if point_s.get() == 'False' :
        points = False
    else:
        points = point_s.get()

    if(plot_type.get() == 'line'):
        fig = px.line(df, x=x.get(), y=y.get(),color=color.get(),template=template.get(),width=0,height=0,color_discrete_sequence=discrete)

    elif(plot_type.get() == 'scatter'):
        fig = px.scatter(df, x=x.get(), y=y.get(),color=color.get(),template=template.get(),width=w,height=h,color_continuous_scale=color_scale.get(),
        trendline=trendline.get(),opacity=1 - opacity.get()/100,marginal_x=marginalx,marginal_y=marginaly)

    elif(plot_type.get() == 'bar'):
        fig = px.bar(df, x=x.get(), y=y.get(),color=color.get(),template=template.get(),width=w,
        height=h,color_discrete_sequence=discrete,orientation=orient,barmode=barmode.get())

    elif(plot_type.get() == 'histogram'):
        fig = px.histogram(df, x=x.get(), y=y.get(),color=color.get(),template=template.get(),width=w,
        height=h,color_discrete_sequence=discrete,orientation=orient,opacity=1 - opacity.get()/100,barmode=barmode.get(),marginal=marginalx)

    elif(plot_type.get() == 'box'):
        fig = px.box(df, x=x.get(), y=y.get(),color=color.get(),template=template.get(),width=w,
        height=h,color_discrete_sequence=discrete,boxmode=box_mode.get(),orientation=orient,points=points)

    elif(plot_type.get() == 'pie'):
        fig = px.pie(df, values=x.get(), names=y.get(),hover_data=[color.get()],template=template.get(),width=w,
        height=h,color_discrete_sequence=discrete,hole=hole.get(),opacity=1 - opacity.get()/100)
        fig.update_traces(textposition=text_position.get(),textinfo=text_info.get())

    elif(plot_type.get() == 'heatmap'):
        fig = px.density_heatmap(df, x=x.get(), y=y.get(),template=template.get(),width=w,height=h,color_continuous_scale=color_scale.get(),
        marginal_x=marginalx,marginal_y=marginaly,orientation=orient,opacity=1 - opacity.get()/100)

    elif(plot_type.get() == 'violin'):
        fig = px.violin(df, x=x.get(), y=y.get(),color=color.get(),template=template.get(),width=w,height=h,color_discrete_sequence=discrete,
        orientation=orient,violinmode=box_mode.get(),points=points,box=box_needed.get())

    elif(plot_type.get() == 'area'):
        fig = px.area(df, x=x.get(), y=y.get(),color=color.get(),template=template.get(),width=w,
        height=h,color_discrete_sequence=discrete,orientation=orient)

    elif(plot_type.get() == 'line polar'):
        fig = px.line_polar(df, r=x.get(), theta=y.get(),color=color.get(),line_close=True,template=template.get(),width=w,
        height=h,color_discrete_sequence=discrete,direction=direction.get(),start_angle=start_angle.get())

    elif(plot_type.get() == 'scatter polar'):
        fig = px.scatter_polar(df, r=x.get(), theta=y.get(),color=color.get(),symbol=color.get(),size=x.get(),template=template.get(),width=w,
        height=h,opacity=1 - opacity.get()/100,color_discrete_sequence=discrete,direction=direction.get(),start_angle=start_angle.get())

    elif(plot_type.get() == 'wind rose'):
        fig = px.bar_polar(df, r=x.get(), theta=y.get(),color=color.get(),color_discrete_sequence=discrete,template=template.get(),width=w,
        height=h,barmode=barmode.get(),direction=direction.get(),start_angle=start_angle.get())

    fig.update_layout(title_text=title.get())
    if xlabel.get() != 'default':
        fig.update_layout(xaxis_title=xlabel.get())
    if ylabel.get() != 'default':
        fig.update_layout(yaxis_title=ylabel.get())
    filepath = "snakegame_graphs/"+filename.get()+'.html'

    if not os.path.exists('snakegame_graphs') :
        os.mkdir('snakegame_graphs')
        print('successful')

    if os.path.exists(filepath) and os.path.isfile(filepath):
        Msgbox = messagebox.askquestion('Snake_Game',f'{filename.get()}.html already exist\nDo you want to replace it?',icon='warning')
        if Msgbox == 'yes' :
            fig.write_html(filepath, auto_open=False)
            root.withdraw()
            graph_window(filepath)
            root.deiconify()
            filename.set(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S Graph"))
            return
        else:
            filename.set(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S Graph"))
            return
    filename.set(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S Graph"))
    fig.write_html(filepath, auto_open=False)
    root.withdraw()
    graph_window(filepath)
    root.deiconify()

def customization():
    root.geometry('900x500')
    sep.place(x=30,y=310,width=840)
    b6.place_forget()
    b3.place(x=20,y=470)
    b4.place(x=800,y=470)

    if c1.get() == 'line' :
        root.geometry('900x350')
        b3.place(x=10,y=320)
        b4.place(x=800,y=320)
        sep.place_forget()
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)

    if c1.get() == 'scatter' :
        l9.place(x=500,y=250)
        c8.place(x=700,y=265)
        l10.place(x=30,y=320)
        c9.place(x=230,y=335)
        l15.place(x=500,y=320)
        c15.place(x=700,y=335)
        l11.place(x=30,y=370)
        c10.place(x=230,y=385)
        l12.place(x=500,y=370)
        c11.place(x=700,y=385)

    if c1.get() == 'bar' :
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l13.place(x=30,y=320)
        c13.place(x=230,y=335)
        l14.place(x=500,y=320)
        c14.place(x=700,y=335)

    if c1.get() == 'histogram' :
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l13.place(x=30,y=320)
        c13.place(x=230,y=335)
        l14.place(x=500,y=320)
        c14.place(x=700,y=335)
        l15.place(x=500,y=370)
        c15.place(x=700,y=385)
        l11.config(text='Marginal Graph')
        l11.place(x=30,y=370)
        c10.place(x=230,y=385)

    if c1.get() == 'box' :
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l14.place(x=500,y=320)
        c14.place(x=700,y=335)
        l18.config(text='Box Mode')
        l18.place(x=30,y=320)
        c18.place(x=230,y=335)
        l19.place(x=30,y=370)
        c19.place(x=230,y=385)

    if c1.get() == 'pie' :
        l9.place(x=500,y=250)
        c8.place(x=700,y=265)
        l15.place(x=500,y=320)
        c15.place(x=700,y=335)
        l20.place(x=500,y=320)
        c20.place(x=700,y=335)
        l20.place(x=30,y=320)
        c20.place(x=230,y=335)
        l21.place(x=30,y=370)
        c21.place(x=230,y=385)
        l22.place(x=500,y=370)
        c22.place(x=700,y=385)

    if c1.get() == 'heatmap' :
        l9.place(x=500,y=250)
        c8.place(x=700,y=265)
        l14.place(x=30,y=250)
        c14.place(x=230,y=265)
        l11.place(x=30,y=320)
        c10.place(x=230,y=335)
        l12.place(x=500,y=320)
        c11.place(x=700,y=335)
        l15.place(x=30,y=370)
        c15.place(x=230,y=385)

    if c1.get() == 'violin' :
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l14.place(x=500,y=320)
        c14.place(x=700,y=335)
        l18.config(text='Violin Mode')
        l18.place(x=30,y=320)
        c18.place(x=230,y=335)
        l19.place(x=30,y=370)
        c19.place(x=230,y=385)
        l23.place(x=500,y=370)
        c23.place(x=700,y=385)

    if c1.get() == 'area' :
        root.geometry('900x430')
        b3.place(x=20,y=390)
        b4.place(x=800,y=390)
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l14.place(x=30,y=320)
        c14.place(x=230,y=335)

    if c1.get() == 'line polar' :
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l16.place(x=30,y=320)
        c16.place(x=230,y=335)
        l17.place(x=500,y=320)
        c17.place(x=700,y=335)

    if c1.get() == 'scatter polar' :
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l16.place(x=30,y=320)
        c16.place(x=230,y=335)
        l17.place(x=30,y=370)
        c17.place(x=230,y=385)
        l15.place(x=500,y=320)
        c15.place(x=700,y=335)

    if c1.get() == 'wind rose' :
        l9.place(x=500,y=250)
        c12.place(x=700,y=265)
        l13.place(x=30,y=320)
        c13.place(x=230,y=335)
        l17.place(x=30,y=370)
        c17.place(x=230,y=385)
        l15.place(x=500,y=320)
        c15.place(x=700,y=335)
        l16.place(x=500,y=370)
        c16.place(x=700,y=385)
def show_remove_settings():
    if settings.winfo_ismapped():
        settings.place_forget()
    else:
        settings.place(x=550,y=40)
        filename.set(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S Graph"))

def checksettings_palced_or_not(*args):
    if settings.winfo_ismapped():
        settings.place_forget()

# Buttons
b1 = tkinter.Button(root,text=" Next ",font=("OCR A Extended",10),padx=6,command=expand_it,bd=3)
b1.place(x=380,y=320)

b2 = tkinter.Button(root,text=" Close ",font=("OCR A Extended",10),padx=6,command=close_program,bd=3)
b2.place(x=20,y=320)

b3 = tkinter.Button(root,text=" Back ",font=("OCR A Extended",10),padx=6,command=normalit,bd=3)
b3.place_forget()

b4 = tkinter.Button(root,text="Plot It",font=("OCR A Extended",10),padx=6,command=plotter,bd=3)
b4.place_forget()

b5 = tkinter.Button(root,image=settings_image,command=show_remove_settings,bg=black,bd=0,activebackground=black,activeforeground=black)
b5.place_forget()

b6 = tkinter.Button(root,text='Add More Customization...',font=("OCR A Extended",12),padx=10,command=customization,bd=5)
b6.place_forget()

settings = tkinter.LabelFrame(root,text='Settings',padx=15,pady=10,bg=black,fg=white)
settings.place_forget()
sl1 = tkinter.Label(settings,text='Title of The Graph :  ',bg=black,fg=white,anchor='w')
sl1.grid(row=0,column=0)
sl2 = tkinter.Label(settings,text='Select Width :  ',bg=black,fg=white,anchor='w')
sl2.grid(row=1,column=0)
sl3 = tkinter.Label(settings,text='Select Height :  ',bg=black,fg=white,anchor='w')
sl3.grid(row=2,column=0)
sl5 = tkinter.Label(settings,text='Save Graph As   :  ',bg=black,fg=white,anchor='w')
sl5.grid(row=3,column=0)

title = tkinter.StringVar()
title.set('Snake_Game DATAPLOT')
se1 = tkinter.Entry(settings,textvariable=title,width=25,insertbackground='white',bg=black,fg=white)
se1.grid(row=0,column=1)

width = tkinter.IntVar()
se2 = tkinter.Entry(settings,textvariable=width,width=25,insertbackground='white',bg=black,fg=white)
se2.grid(row=1,column=1)

height = tkinter.IntVar()
se3 = tkinter.Entry(settings,textvariable=height,width=25,insertbackground='white',bg=black,fg=white)
se3.grid(row=2,column=1)

filename = tkinter.StringVar()
filename.set(datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S Graph"))
title.set('Snake_Game DataPlot')
se4 = tkinter.Entry(settings,textvariable=filename,width=25,insertbackground='white',bg=black,fg=white)
se4.grid(row=3,column=1)

sb1 = tkinter.Button(settings,text='  Exit  ',command=checksettings_palced_or_not,bg=black,fg=white,anchor='center',padx=120)
sb1.grid(row=4, column=0,columnspan=5)

# Keybindings
b1.bind('<Button-1>',lambda e: settings.place_forget())
b2.bind('<Button-1>',lambda e: settings.place_forget())
b3.bind('<Button-1>',lambda e: settings.place_forget())
b4.bind('<Button-1>',lambda e: settings.place_forget())
b6.bind('<Button-1>',lambda e: settings.place_forget())

c2.bind('<FocusIn>', checksettings_palced_or_not)
c1.bind('<FocusIn>', checksettings_palced_or_not)
c3.bind('<FocusIn>', checksettings_palced_or_not)
c4.bind('<FocusIn>', checksettings_palced_or_not)
c5.bind('<FocusIn>', checksettings_palced_or_not)
c6.bind('<FocusIn>', checksettings_palced_or_not)
c7.bind('<FocusIn>', checksettings_palced_or_not)
c8.bind('<FocusIn>', checksettings_palced_or_not)
c9.bind('<FocusIn>', checksettings_palced_or_not)
c10.bind('<FocusIn>',checksettings_palced_or_not)
c11.bind('<FocusIn>',checksettings_palced_or_not)
c12.bind('<FocusIn>',checksettings_palced_or_not)
c13.bind('<FocusIn>',checksettings_palced_or_not)
c14.bind('<FocusIn>',checksettings_palced_or_not)
c15.bind('<FocusIn>',checksettings_palced_or_not)
c16.bind('<FocusIn>',checksettings_palced_or_not)
c17.bind('<FocusIn>',checksettings_palced_or_not)
c18.bind('<FocusIn>',checksettings_palced_or_not)
c19.bind('<FocusIn>',checksettings_palced_or_not)
c20.bind('<FocusIn>',checksettings_palced_or_not)
c21.bind('<FocusIn>',checksettings_palced_or_not)
c22.bind('<FocusIn>',checksettings_palced_or_not)
c23.bind('<FocusIn>',checksettings_palced_or_not)

c1.bind('<<ComboboxSelected>>',check_plot)
c12.bind('<<ComboboxSelected>>',check_color)

root.protocol("WM_DELETE_WINDOW", close_program)
root.mainloop()
