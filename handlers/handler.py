import sqlite3  
import hashlib

query_user_table = """
create table if not exists user (
    username char(200) primary key,
    emailid varchar(100) unique,
    password varchar(256) not null
)
"""

notes_table = """
create table if not exists notes(
    noteid integer  ,
    username char(200),
    title varchar(255),
    content text,
    created_on datetime default current_timestamp,
    modified_on datetime default current_timestamp,
    star boolean default false,
    foreign key (username) references user(username),
    primary key (noteid,username)
)
"""


def create_tables():
    conn = sqlite3.connect('noteify.db')
    cursor = conn.cursor()
    cursor.execute(query_user_table)
    cursor.execute(notes_table)    
    conn.commit()
    conn.close()



def get_userby_username (username):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""
    select username,emailid,password from user where username=?
    """,(username,))
    return res.fetchone()

def get_userby_email(email):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""
    select username,emailid,password from user where emailid=?
    """,(email,))
    return res.fetchone()
def match_passsword(username,password):
    
    data=get_userby_username(username)
    if not data:
        return False
    hashed_password=hashlib.sha256(password.encode('utf-8')).hexdigest()

    print(data)
    return hashed_password==data[2]

def create_user(username, email, password) -> bool:
    # check if the username already exists here
    if get_userby_username(username):
        return False

    # check if the email already exists here:
    if get_userby_email(email):
        return False

    # hash the password
    hashed_password=hashlib.sha256(password.encode('utf-8')).hexdigest()
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    cur.execute("""
    insert into user values (?,?,?)
    """,(username,email,hashed_password))
    conn.commit()
    conn.close()
    return True


def get_all_notes(username):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""select * from notes where username=?
    """,(username,))
    result=res.fetchall()
    conn.close()
    print(result)
    return result

def get_latest_created_notes(username):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""
    select max(noteid) from notes where username=?
    """,(username,))
    result=res.fetchone()
    conn.close()
    return result[0] if result else None

def create_note(username,title='',content=''):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    noteid=count_username(username)+1
    cur.execute("""
    insert into notes(noteid, username, title, content ) values(?,?,?,?)
    """,(noteid ,username,title,content,))
    conn.commit()
    conn.close()
    return noteid

    
def modify_note(noteid, username, title, content):
    if not get_note(noteid, username):
        return False
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    cur.execute("""
    update notes set title=?,content=? where noteid=? and username=?
    """,(title,content,noteid,username))
    conn.commit()
    conn.close()
    return True

def get_note(noteid, username):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""
    select * from notes where username=? and noteid=?
    """,(username,noteid,))
    arr = res.fetchone()
    conn.close()
    return arr
    
def delete_note(noteid, username):
    if not get_note(noteid, username):
        return False
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    cur.execute("""
    delete from notes where noteid=? and username=?
    """,(noteid,username))
    conn.commit()
    conn.close()
    return True

def count_username(username):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""
    select count(*) from notes where username=?
    """,(username,))
    result=res.fetchone()[0]    
    conn.close()
    return result


    


