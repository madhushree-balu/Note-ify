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
