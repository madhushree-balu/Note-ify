from handlers import handler
from flask import (
    Flask, render_template, request, session,
    url_for, redirect, send_from_directory,
    abort,flash
)
import os

handler.create_tables()

app = Flask(__name__)
app.secret_key = "super secret key"



@app.before_request
def before_request():
    if request.path not in ['/','/login','/signup']:
        if 'username' not in session:
            return redirect(url_for('login'))



@app.get("/static/<path:filename>")
def serve_static(filename):
    # check if the path actually exists using os
    if not os.path.exists("static/" + filename):
        return abort(404)
    return send_from_directory("static", filename)



@app.get("/")
def index():
    if 'username' in session:
        notes = handler.get_all_notes( session['username'] )
        print(notes)
        return render_template('notes.html', notes=notes,username = session.get('username'))
    return render_template('index.html')



@app.get("/login")
def login():
    return render_template('login.html')



@app.post("/login")
def login_post():
    uname=request.form.get('username')
    paswd=request.form.get('password')
    print(uname,paswd)
    if handler.match_passsword(uname,paswd):
        session['username']=uname
        return redirect(url_for('index'))
    flash("Invalid username or password")
    return redirect(url_for('login'))



@app.get("/logout")
def logout():
    session.clear()
    return redirect (url_for('index'))



@app.get("/signup")
def signup():
    return render_template('signup.html')



@app.post("/signup")
def signup_post():
    uname=request.form.get('username')
    passwd=request.form.get('password')
    email=request.form.get('emailid')
    
    if handler.create_user(uname,email,passwd):
        session['username'] = uname
        return redirect(url_for('index')) # changed here
    print('User already exists  or email already exists')
    return redirect(url_for('signup'))



@app.get("/<string:uname>/<int:note_id>")
def note(note_id,uname):
    username=session.get('username',None)
    public_access = uname != username
    
    if not public_access or handler.get_public(note_id,uname) is not None:
        note = handler.get_note(note_id,uname)
    else:
        note = None
    if not note:
        return redirect(url_for('index'))
        
    return render_template("/note.html", note=note, public_access=public_access )



@app.get("/new")
def new():
    username=session.get('username',None)
    if username is None:
        return redirect(url_for('login'))
    note_id=handler.create_note(username)
    return redirect(url_for('note',note_id=note_id,uname=username))



@app.post("/api/save/<string:uname>/<int:note_id>")
def save(note_id,uname):
    username=session.get('username',None)
    if username is None or uname != username:
        return {
            "success":False
        }
    data = request.get_json()
    if not data:
        return { "success":False }
    
    title = data.get('title')
    content = data.get('content')
    fav = data.get('star', False)
    public = data.get('public', False)
    print(title,content,fav,public)
    handler.modify_note(note_id,username,title,content,fav,public)

    return {
        "success":True
    }



@app.get("/api/fav/<int:note_id>")
def fav(note_id):
    username=session.get('username',None)
    return {"success":True,"star":handler.toggle_fav(note_id,username)}



@app.get("/api/delete/<int:note_id>")
def delete(note_id):
    username=session.get('username',None)    
    return {"success":handler.delete_note(note_id,username)}



if __name__=="__main__":
    app.run(debug=True)