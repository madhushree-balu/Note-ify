from handlers import handler
from flask import Flask, render_template, request, session, url_for, redirect

handler.create_tables()

app = Flask(__name__)

@app.get("/")
def index():
    if 'username' in session:
        notes = handler.get_all_notes()

        return render_template('notes.html', notes=notes)
    return render_template('index.html')


@app.get("/login")
def login():
    return render_template('login.html')


@app.post("/login")
def login_post():
    uname=request.form.get('username')
    paswd=request.form.get('password')

    if handler.match_passsword(uname,paswd):
        session['username']=uname
        return 'True'
    return 'False'


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
    
    if handler.create_user(uname,passwd,email):
        session['username'] = uname
        return 'True'
    return 'False'

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
    note_id=handler.create_note('username')
    return redirect(url_for('note',note_id=note_id))



if __name__=="__main__":
    app.run()


    

    

