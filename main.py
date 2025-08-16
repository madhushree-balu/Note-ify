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


# TODO
# 1. [ ]
# check if the session is valid before each request
# for certain all the endpoints except that of index,
# login and signin.
# if the user has not logged in, redirect them to the login page
@app.before_request
def before_request():
    if request.path not in ['/','/login','/signup']:
        if 'username' not in session:
            return redirect(url_for('login'))
# 2. [ ]
# also make use of "flash" function for proper error messages

# 3. [ ]
# review and refine all the code.
# 4. [ ]
# implement a "/api/fav/<int:note_id>" endpoint to toggle and return
# the star value. the return should be in the format: { "success": ?, "star": ? }
# see through necessary validations
@app.get("/api/fav/<int:note_id>")
def fav(note_id):
    username=session.get('username',None)
     
    return {"success":True,"star":handler.toggle_fav(note_id,username)}

# 5. [ ]
# implement a "/api/delete/<int:note_id>" endpoint to delete the note.
# return the success value
@app.get("/api/delete/<int:note_id>")
def delete(note_id):
    username=session.get('username',None)
    
    return {"success":handler.delete_note(note_id,username)}

# 6. [ ]
# look for other "# TODO" in the code.

#7[]
#to check and uncheck the star and public function which does not work

# static handler
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
    flash('User already exists  or email already exists')
    return redirect(url_for('signup'))

# TODO
# instead of /note/<int:note_id> use /<str:username>/<int:note_id>
# check if the username in the route is equal to that of in the session
# if so, fetch and return display the note using the function "get_note"
# if not, fetch and proceed with the function "get_public_note"
@app.get("/<string:uname>/<int:note_id>")
def note(note_id,uname):
    username=session.get('username',None)
    if uname == username or handler.get_public(note_id,uname) is not None:
        note = handler.get_note(note_id,uname)
    else:
        note = None
    if not note:
        return redirect(url_for('index'))
        
    return render_template( "/note.html", note=note )

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

    handler.modify_note(note_id,username,title,content,fav,public)

    # TODO fix this
    # handler.modify_note(note_id,username,title,content)
    return {
        "success":True
    }


# TODO
# @app.delete("/api/delete/<int:note_id>")
# def delete(note_id):
#     # implement the code here to delete the note.
#     # return redirect to login
#     # also implement the required function in the handler file
#     ...

if __name__=="__main__":
    app.run(debug=True)


    

    

