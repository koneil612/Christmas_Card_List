import os, config
import pg
from flask import Flask, render_template, request, redirect, url_for, session
from christmascardlist import *


# ##this is making sure that everything is in utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


app = Flask(__name__)
app.secret_key = "herro"


###
# Routing for your application. Each route is a new page location and saying where we want it to go / do
###


@app.route('/', methods=['POST', 'GET'])
def login():
    if 'username' in session:
        return redirect('/home')
    else:
        return render_template("submit_login.html")

@app.route('/submit_login', methods=['GET','POST'])
def submit_login():
    user=User(username)
    if user.login(password):
        return redirect('/home')
    else:
        return redirect('/')

# @app.route('/logout', methods=['POST', 'GET'])
# def logout():
#     User.logout()

@app.route('/home', methods= ['GET', 'POST'])
def home():
    # if not logged in
    #redir to login
    # if 'username' not in session:
    #     return redirect('/submit_login')
    return render_template("phonebooklisting.html", title="Christmas Card List")

@app.route('/phonebook', methods= ['GET'])
#pulls all the listings in the phonebook
def phonebook():
    list = Entry.getObjects()
    return render_template("phonebook.html", title="Christmas Card List", entry_list=list)

@app.route('/new_entry')
def new_entry():
    return render_template("new_entry.html")

@app.route('/submit_new_entry', methods=['POST'])
def submit_new_entry():
    entry = Entry()
    entry.firstname=request.form.get('firstname')
    entry.lastname=request.form.get('lastname')
    entry.address=request.form.get('address')
    entry.address2=request.form.get('address2')
    entry.city=request.form.get('city')
    entry.state=request.form.get('state')
    entry.szip=request.form.get('zip')
    entry.save()
    return render_template("submit_new_entry.html", firstname=firstname, lastname=lastname, address=address, address2=address2, city=city, state=state, zip=szip)

    # q = "INSERT INTO addresses (firstname, lastname, address, address2, city, state, zip) values ('%s','%s','%s','%s','%s','%s','%s')" % (Database.escape(firstname), Database.escape(lastname), Database.escape(address), Database.escape(address2), Database.escape(city), Database.escape(state), szip)
    # query = db.query(q)



@app.route('/update_entry', methods=['GET'])
def update_entry():
    id=list[0]
    firstname=list[1]
    lastname=list[2]
    address=list[3]
    address2=list[4]
    city=list[5]
    state=list[6]
    zip=list[7]
    entry=Entry(id)
    entry.save()
    return render_template("update_entry.html", firstname=firstname, lastname=lastname, address=address, address2=address2, city=city, state=state, zip=zip,id=id)


###
# The functions below should be applicable to all Flask apps.
###

# @app.route('/<file_name>.txt')
# def send_text_file(file_name):
#     """Send your static text file."""
#     file_dot_text = file_name + '.txt'
#     return app.send_static_file(file_dot_text)


# @app.after_request
# def add_header(response):
#     """
#     Add headers to both force latest IE rendering engine or Chrome Frame,
#     and also to cache the rendered page for 10 minutes.
#     """
#     response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
#     response.headers['Cache-Control'] = 'public, max-age=600'
#     return response
#
#
# @app.errorhandler(404)
# def page_not_found(error):
#     """Custom 404 page."""
#     return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
