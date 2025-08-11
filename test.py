import sqlite3
create_tables=""" 
create table if not exists student(
studentid integer  primary key autoincrement,
studentname char(200) ,
age integer(100)
)
"""

conn=sqlite3.connect('sample.db')
cur=conn.cursor()
cur.execute(create_tables)
cur.execute(""" 
insert into student (studentname,age) values
('madhu','20'),
('tanu','16'),
('abc','12')
""")
conn.commit()
res=cur.execute(""" 
select * from student
""")
print(res.fetchall())

def count_username(username):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""
    select count(*) from notes where username=?
    """,(username,))        
    return res.fetchone()[0]  
    conn.close()
count_username('Madhushree')



def create_note(username,title='',content=''):
    conn=sqlite3.connect('noteify.db')
    cur=conn.cursor()
    res=cur.execute("""
    insert into notes(noteid, username, title, content ) values(?,?,?,?)
    """,(count_username(username)+1,username,title,content,))
    conn.commit()
    print(res.fetchall())
    conn.close()
    
create_note('Madhushree','title','content') 

