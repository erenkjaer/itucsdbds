from flask import Flask, render_template, request, g, session ,redirect,url_for
import psycopg2 as dbapi2
import dbcreate
URL="postgres://mscrlztk:j9PwWtS-g7dCBt9DxTsnO1GSRGDjgSJ-@kandula.db.elephantsql.com:5432/mscrlztk"
app=Flask(__name__)
app.secret_key='supersecret'

dbcreate.createtables()

@app.before_request
def before_request():
    if "user_id" in session:
        user=get_user(session.get('user_id'))
        g.username=user[1]
        g.email=user[3]
    else:
        g.username= None
        g.email=None

def adduser(usern,passw,email):
    with dbapi2.connect(URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""INSERT INTO users (username,password,email) VALUES (%s,%s,%s);""",(usern,passw,email))
            cursor.close()


@app.route('/signup', methods=('GET','POST'))
def signup():
    if request.method=='POST':
        username1=request.form["username"]
        password1=request.form["password"]
        email1=request.form["email"]
        adduser(username1,password1,email1)    
        return redirect(url_for('login'))
    return render_template('signup.html')


def get_user(username):
    with dbapi2.connect(URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM users WHERE username=%s""",(username,))
            user=cursor.fetchone()
            cursor.close()
    return user


@app.route('/login', methods=("POST","GET"))
def login():
    if request.method=="POST":
        session.pop('user_id', None)
        username1=request.form["username"]
        password1=request.form["password"]
        user=get_user(username1)
        if user is None:
            return redirect(url_for('login'))
        elif user[2] != password1:
            return redirect(url_for('login'))
        else:
            session['user_id']=user[1]
            return redirect(url_for('profile'))
    return render_template('login.html')

@app.route('/profile')
def profile():
    if not g.username:
        return redirect(url_for('login'))
    return  render_template('profile.html')
@app.route('/restaurants')
def restaurants():
    with dbapi2.connect(URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("""SELECT * FROM restaurants""")
            restaurants=cursor.fetchall()        
            cursor.execute("""SELECT feature,restaurantid FROM features INNER JOIN restaurants ON restaurantid=restaurants.id;""")
            features=cursor.fetchall()
            cursor.close()
    return render_template('restaurants.html',restaurants=restaurants,features=features)

@app.route('/comment', methods=('GET','POST'))
def comment():
    if request.method=='POST':
        username=request.form["usern"]
        restaurantname=request.form["restn"]
        point=request.form["point"]
        comment=request.form["comm"]
        with dbapi2.connect(URL) as connection:
            with connection.cursor() as cursor:
                statement="""INSERT INTO comments(username,restaurantname,point,explanation) VALUES(%s,%s,%s,%s);"""
                cursor.execute(statement,(username,restaurantname,point,comment))
        return  redirect(url_for('restaurants'))       
    return render_template('comment.html')

if __name__=='__main__':
    app.debug=True
    app.run()   