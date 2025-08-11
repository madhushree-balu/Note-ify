from handlers import handler
from flask import Flask, render_template, request, session, url_for, redirect

handler.create_tables()

app = Flask(__name__)
app.secret_key = "super secret key"

@app.get("/")
def index():
    if 'username' in session:
        notes = handler.get_all_notes( session['username'] )

        return render_template('notes.html', notes=notes)
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
    
    return redirect(url_for('signup'))

@app.get("/note/<int:note_id>")
def note(note_id):
    username=session.get('username',None)
    if username is None:
        return redirect(url_for('login'))
    note = handler.get_note(note_id,username)

    if not note:
        return redirect(url_for('index'))

    return render_template( "/note.html", note=note )

@app.get("/new")
def new():
    username=session.get('username',None)
    if username is None:
        return redirect(url_for('login'))
    note_id=handler.create_note(username)
    return redirect(url_for('note',note_id=note_id))


@app.post("/api/save/<int:note_id>")
def save(note_id):
    username=session.get('username',None)
    if username is None:
        return {
            "success":False
        }
    data = request.get_json()
    if not data:
        return { "success":False }
    
    title = data.get('title')
    content = data.get('content')

    # fix this
    # handler.modify_note(note_id,username,title,content)
    return {
        "success":True
    }

# @app.get("/api/fav/<int:note_id>")
# def fav(note_id):
#     # the code to toggle the star and return the bool val
#     # also implement it in the handler file.
#     # return { success: ?, star: ? }
#     ...

# @app.delete("/api/delete/<int:note_id>")
# def delete(note_id):
#     # implement the code here to delete the note.
#     # return redirect to login
#     # also implement the required function in the handler file
#     ...

if __name__=="__main__":
    app.run(debug=True)


    

    

