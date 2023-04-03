import sqlite3
import os

def connect(): #Creating tables
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS game_records (
                    Id INTEGER PRIMARY KEY,
                    username TEXT,
                    date TEXT,
                    score INTEGER,
                    snakecolor TEXT,
                    level TEXT,
                    time_taken REAL,
                    user_id INTEGER,
                    CONSTRAINT fk_users
                      FOREIGN KEY (user_id) REFERENCES users(Id)
                      	ON DELETE CASCADE  )    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                    Id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT,
                    image_id INTEGER)   ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS current_user (
                    user_id INTEGER,
                    username TEXT,
                    snakecolor_txt TEXT DEFAULT 'Green',
                    snakecolor_hex TEXT DEFAULT '#80B918',
                    food TEXT DEFAULT 'Apple',
                    level TEXT DEFAULT 'Easy',
                    controls TEXT DEFAULT 'Arrow Keys' );    ''')

    cur.execute('''CREATE TABLE IF NOT EXISTS profile_pics (
                    Id INTEGER PRIMARY KEY,
                    pic_name TEXT,
                    image BLOB)     ''')
    
    cur.execute('SELECT COUNT(*) FROM current_user')
    if cur.fetchall()[0][0] == 0 :
        cur.execute('INSERT INTO current_user (user_id,username) VALUES (?,?)',(0,''))

    conn.commit()
    conn.close()

def insert(username, date, score, snakecolor, level, time_taken,user_id): #Inserting game details in 'game_records' table
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO game_records VALUES (NULL , ?,?,?,?,?,?,?)" , 
                    (username, date, score, snakecolor, level, time_taken, user_id))
    conn.commit()
    conn.close()

def view() -> list: #Retriving data from 'game_records' table
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT Id FROM game_records ORDER BY Id")
    ids = cur.fetchall()
    cur.execute("SELECT username, date, score, snakecolor, level, time_taken FROM game_records ORDER BY Id")
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return ids,rows

def delete(id): #Deleting data from 'game_records' table
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM game_records WHERE Id=? ", (id,))
    conn.commit()
    conn.close()
 
def search(username='', date='', score='', snakecolor='', level='', time_taken=''): #Function for 'Seach' Button - frontend.py
    if level == 'All':
        level = ' '
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute('''SELECT Id FROM game_records WHERE 
                (username = ? OR ? = '') 
                AND (date = ? OR ? = '') 
                AND (score = ? OR ? = '') 
                AND (snakecolor = ? OR ? = '') 
                AND (level = ? or ? = ' ') 
                AND (time_taken = ? OR ? = '') 
                ORDER BY Id''',
        (username ,username, date, date , score, score , snakecolor, snakecolor, level, level, time_taken, time_taken))
    ids = cur.fetchall()
    cur.execute('''SELECT username, date, score, snakecolor, level, time_taken FROM game_records WHERE 
                    (username = ? OR ? = '') 
                    AND (date = ? OR ? = '') 
                    AND (score = ? OR ? = '') 
                    AND (snakecolor = ? OR ? = '') 
                    AND (level = ? or ? = ' ') 
                    AND (time_taken = ? OR ? = '') 
                    ORDER BY Id''',
        (username ,username, date, date , score, score , snakecolor, snakecolor, level, level, time_taken, time_taken))
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return ids,rows

def formatdata(rows): #Adding whitespaces to the 'data from table' to make uniform alignment in Listbox - frontend.py
    refined_rows = []
    for row in rows:
        row = list(row)
        row[0] = row[0] + (' ' * (17-len(row[0])))
        row[1] = row[1] + (' ' * 2)
        row[2] = str(row[2]) + (' ' * (7-len(str(row[2]))))
        row[3] = row[3] + (' ' * (15-len(row[3])))
        row[4] = row[4] + (' ' * (10-len(row[4])))
        row[5] = str(row[5])
        row = row[0] + row[1] + row[2] + row[3] + row[4] + row[5]
        refined_rows.append(row)
    return refined_rows

def update_userdata(snakecolor_txt,snakecolor_hex,food,level_button,controlkeys_button): #Updating current_user data - main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute('''UPDATE current_user SET 
                    snakecolor_txt=?,snakecolor_hex=?,food=?,level=?,controls=? ''',
                    (snakecolor_txt,snakecolor_hex,food,level_button,controlkeys_button)    )
    conn.commit()
    conn.close()

def current_userdata() -> list: #Getting current_user data from the table - main.py & snakegame.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM current_user")
    data = cur.fetchall()
    if data != []:
        current_userdata = data[0]
    else:
        current_userdata = [0,'','Green','#80B918','Apple','Easy','Arrow Keys']
    conn.commit()
    conn.close()
    return current_userdata

def current_user_profile_pic(): #Getting current_user DP(binary data) - main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute('''SELECT image FROM profile_pics
                    JOIN users ON users.image_id = profile_pics.Id
                    JOIN current_user ON current_user.user_id = users.Id ''')
    row = cur.fetchall()[0][0]
    conn.commit()
    conn.close()
    return row

def current_user_display() -> list: #Getting in current_user data to display in user profile - main.py
    userdata = []
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT username FROM current_user")
    userdata.append(cur.fetchall()[0][0])
    cur.execute('''SELECT SUM(score)/10 FROM current_user
                    LEFT JOIN game_records ON
                        current_user.user_id = game_records.user_id ''')
    userdata.append(cur.fetchall()[0][0])
    cur.execute('''SELECT MAX(score) from current_user
                    LEFT JOIN game_records ON
                        current_user.user_id = game_records.user_id ''')
    userdata.append(cur.fetchall()[0][0])
    cur.execute('''SELECT COUNT(current_user.username) FROM current_user
                INNER JOIN game_records ON
                    current_user.user_id = game_records.user_id ''')
    userdata.append(cur.fetchall()[0][0])
    conn.commit()
    conn.close()
    return userdata

def update_current_user(username): #Changing current_user - main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT Id, username FROM users WHERE username = ?",(username,))
    cur.execute("UPDATE current_user SET user_id = ?, username=?",(cur.fetchall()[0]))
    conn.commit()
    conn.close()

def add_usersin_users_and_current_users_table(username,password): #Adding new users in the table - main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (NULL,?,?,?)",(username,password,1))
    cur.execute("SELECT Id,username FROM users ORDER BY Id DESC LIMIT 1")
    cur.execute("UPDATE current_user SET user_id=?, username=?",cur.fetchall()[0])
    conn.commit()
    conn.close()

def update_profile_pic(image_id): #Updating image_id for the current_user - main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT current_user.user_id FROM current_user")
    user_id = cur.fetchall()[0][0]
    cur.execute('''UPDATE users SET image_id = ?
                        WHERE users.Id = ? ''',(image_id,user_id))
    # cur.execute("UPDATE users SET image_id = ? WHERE users.Id = current_user.user_id",(image_id,))
    # cur.execute('''UPDATE users SET users.image_id = ? FROM users
    #                 INNER JOIN current_user ON
    #                 current_user.user_id = users.Id ''',(image_id,))
    conn.commit()
    conn.close()

def get_list_of_users() -> list: #To display list of users in Listbox - main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute('''SELECT users.Id, users.username FROM users 
                    LEFT JOIN game_records
                        ON users.Id = game_records.user_id
                        group by users.Id''')
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

def get_username_password(username): #Getting usernaem and password for the entered username to check whether the entered password matches with the data in the table- main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute('''SELECT username, password FROM users WHERE users.username = ?''',(username,))
    data = cur.fetchall()[0]
    conn.commit()
    conn.close()
    return data

def get_imageid() -> int: #Getting the DP id for the current_user and it is used to highlight in the list of other pics - main.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT user_id from current_user")
    user_id = cur.fetchall()[0][0]
    if user_id != 0 :
        cur.execute("SELECT image_id FROM users WHERE users.Id = ? ",(user_id,))
        image_id = cur.fetchall()[0][0]
    else:
        image_id = 1
    conn.commit()
    conn.close()
    return image_id

def get_highscore(level): #Getting highscore - snakegame.py
    conn = sqlite3.connect('snakegame_db.db')
    cur = conn.cursor()
    cur.execute("SELECT MAX(score) FROM game_records WHERE level = ?",(level,))
    highscore = cur.fetchall()[0][0]
    conn.commit()
    conn.close()
    return highscore

connect()

def image_to_binary_converter(imagefile): #Converting JPG/PNG Image file to binary data
    file = open(imagefile,'rb')
    image_data = file.read()
    return image_data

conn = sqlite3.connect('snakegame_db.db')
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM profile_pics")
if cur.fetchall()[0][0] == 0 : #The below code will be executed only once
    list_of_images = os.listdir(os.getcwd() + '\\profile_pics')
    image_name = ''

    for i in list_of_images:
        image_name = i
        image_data = image_to_binary_converter("profile_pics/" + image_name)
        cur.execute("INSERT INTO profile_pics VALUES (NULL,?,?)",(image_name,image_data))
        

conn.commit()
conn.close()
