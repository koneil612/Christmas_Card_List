import mysql.connector
import os
import pg
from flask import Flask, render_template, request, redirect, url_for, session

import sys


db = pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.secret_key = "herro"


###
# Routing for your application.
###

@app.route('/', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect('/home')
    else:
        return render_template("submit_login.html")

@app.route('/submit_login', methods=['GET','POST'])
def submit_login():
    username = request.form.get('username')
    password = request.form.get('password')
    db = pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)
    query = db.query("SELECT username, password FROM \"user\" WHERE username = '%s'" % username)
    result_list = query.namedresult()
    if result_list and len(result_list) > 0:
        user = result_list[0]
        if password== password:
            #successfully logged in
            session['username'] = user.username
            return redirect('/home')
        else:
            return redirect('/')
    else:
        return redirect('/')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['username']
    return redirect('/')

@app.route('/home', methods= ['GET', 'POST'])
def home():
    # if not logged in
    #redir to login
    # if 'username' not in session:
    #     return redirect('/submit_login')
    db = pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)
    query = db.query ("SELECT id, firstname, lastname, address, address2, city, state, zip FROM addresses")
    result_set = query.namedresult()
    db.close()

    return render_template("phonebooklisting.html", title="Christmas Card List", result_set = result_set)

@app.route('/phonebook', methods= ['GET'])
#pulls all the listings in the phonebook
def phonebook():
    db = pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)
    query =  db.query("SELECT id, firstname, lastname, address, address2, city, state, zip FROM addresses")
    result_set = query.namedresult()
    db.close()
    return render_template("phonebook.html", title="Christmas Card List", result_set=result_set)

@app.route('/new_entry')
def new_entry():
    return render_template("new_entry.html")

@app.route('/submit_new_entry', methods=['POST'])
def submit_new_entry():
    firstname=request.form.get('firstname')
    lastname=request.form.get('lastname')
    address=request.form.get('address')
    address2=request.form.get('address2')
    city=request.form.get('city')
    state=request.form.get('state')
    szip=request.form.get('zip')
    db = pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)
    q = "INSERT INTO addresses (firstname, lastname, address, address2, city, state, zip) values ('%s','%s','%s','%s','%s','%s','%s')" % (Database.escape(firstname), Database.escape(lastname), Database.escape(address), Database.escape(address2), Database.escape(city), Database.escape(state), szip)
    query = db.query(q)

    return render_template("submit_new_entry.html", firstname=firstname, lastname=lastname, address=address, address2=address2, city=city, state=state, zip=szip)

@app.route('/update_entry', methods=['GET'])
def update_entry():
    db = pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)
    id = request.args.get('id')
    q = "SELECT id, firstname, lastname, address, address2, city, state, zip FROM addresses WHERE id=%s" %id
    query = db.query(q)
    id=list[0]
    firstname=list[1]
    lastname=list[2]
    address=list[3]
    address2=list[4]
    city=list[5]
    state=list[6]
    zip=list[7]
    return render_template("update_entry.html", firstname=firstname, lastname=lastname, address=address, address2=address2, city=city, state=state, zip=zip,id=id)

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


###
# The functions below should be applicable to all Flask apps.
###

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


class Database(object):
    @staticmethod
    def getConnection():
        if config.DBTYPE=="mysql":
            return mysql.connector.connect(user=config.DBUSER,password=config.DBPASS,host=config.DBHOST,database=config.DBNAME)
        if config.DBTYPE=="postgresql":
            return pg.db(host=config.DBHOST, user=config.DBUSER, passwd=config.DBPASS, dbname=config.DBNAME)
    @staticmethod
    def escape(value):
        return value.replace("'","''")

    @staticmethod
    def getResult(query, getOne = False):
        result_set=()
        conn = Database.getConnection()
        if config.DBTYPE=="mysql":
            cur = conn.cursor()
            cur.execute(query)
            if getOne:
                result_set = cur.fetchone()
            else:
                result_set = cur.fetchall()
            cur.close()
        if config.DBTYPE=="postgresql":
            result = conn.query(query)
            result_set = result.getresult()
            if getOne and result_set:
                result_set=result_set[0]
        conn.close()
        return result_set

    @staticmethod
    def doQuery(query):
        conn = Database.getConnection()
        if config.DBTYPE == "mysql":
            cur = conn.cursor()
            cur.execute(query)
            conn.commit()
            lastID = cur.lastrowid
            cur.close()
        if config.DBTYPE == "postgresql":
            result = conn.query(query)
            lastID = result.getresult()[0][0]
            print "lastID=%d" %lastId
        conn.close()
        return lastID

if __name__ == '__main__':
    app.run(debug=True)
