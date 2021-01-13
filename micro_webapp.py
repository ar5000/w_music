#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
import requests
import json
import random
import xml.etree.ElementTree as ET
# [MODELS]
import instrument_model
# [APP START]
app = Flask(__name__)
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'this_IS_$up3r_SECUR3~'
# Key is the username and the value is a dictionary with the password as a key
#  and the role as another key.
users = {'Miguel':{
        "password": '1234',
        "role": 'admin'
    },
    'Kyle':{
        "password": "secure",
        "role": "buyer"
    }
}
##jan6 
artists = ['BTS','Michael Jackson', 'Lady Gaga','ABBA','Aerosmith']
songURL = 'https://www.songsterr.com/a/ra/songs/byartists.json'
## end
# instruments = [{name:"", ref_num:2342, image:"", category:""}]
# cart = []
# [MAIN][Admin Route]
@app.route('/instruments/show/all')
def show_all():
    if 'role' not in session or session['role']!='admin':
        res = "for admin only, please login"
        return render_template('messages.html', message=res)
    conn = sqlite3.connect("music_store.db")
    cu = conn.cursor()
    instrument_model.show_all(cu)
    res = [{"ref_num":row[0], "category": row[2],"name":row[1], "url":row[3]} for row in cu]
    conn.close()
    return render_template('index.html', instruments=res)
@app.route('/instruments/show/<ref_number>')
def show_detail_page(ref_number):
    conn = sqlite3.connect("music_store.db")
    cu = conn.cursor()
    instrument_model.show_one(cu, (ref_number,))
    ref_num, name, cat, url = cu.fetchone()
    if cat == 'string':
        ##add songsterr
        artist = artists[random.randint(0,len(artists))-1]
        r = requests.get(songURL, params={'artists':'"'+artist+'"'})
        if r.status_code == 200:
            j=r.json()
            songNo = random.randint(0,len(j)-1)
            ##songsterrURL = "http://www.songsterr.com/a/wa/song?id="+str(j[songNo]['id'])
            instrument = {"ref_num":ref_num, "category": cat,"name":name, "url":url, "songs":j[songNo]['title'], "artist": artist}
            # TODO: reuse the same template as detailed.html and make use of conditionals
            # return render_template('detailed.html', instrument=instrument)
        songster = requests.get(f'http://www.songsterr.com/a/ra/songs.xml?pattern={instrument["songs"]}')
        root = ET.fromstring(songster.content)
        songs = []
        for child in root:
            songs.append(child.attrib['id'])
        songurl= f'http://www.songsterr.com/a/wa/song?id={songs[0]}'
        instrument['songurl']= songurl
    else:
        instrument = {"ref_num":ref_num, "category": cat,"name":name, "url":url}
    return render_template('detailed.html', instrument=instrument)
@app.route('/instruments/create', methods=["GET", "POST"])
def create_instrument():
    if request.method == "POST":    
        # process information in the body of the request
        ref_num = int(request.form['ref'])
        name = request.form['name']
        cat = request.form['category']
        url = request.form['url']
        # prepare fields for insert
        fields = (ref_num, name, cat, url)
        # prepare connection
        conn = sqlite3.connect("music_store.db")
        cu = conn.cursor()
        # instrument insert
        instrument_model.add_one(cu, fields)
        # check integrity of the operation
        added_ref_num = cu.lastrowid
        if added_ref_num == ref_num:
            conn.commit()
            res = "added!"
        else:
            res = 'oops, something happened please ask the administrator'
            # DRY
        conn.close()
        return res
    else:
        # this is GET
        return render_template("create_instrument.html")
@app.route('/instruments/update/<ref_number>', methods=['GET', 'POST'])
def update_one_instrument(ref_number):
    res = ''
    if request.method == 'POST':
        ref_num = ref_number
        cat = request.form['cat']
        name = request.form['name']
        url = request.form['url']
        # sql update operation
        fields = (name, cat, url, ref_num)
        # open db connection
        conn = sqlite3.connect("music_store.db")
        cu = conn.cursor()
        # instrument update
        instrument_model.update_one(cu, fields)
        # check integrity of operation
        if cu.rowcount > 0:
            conn.commit()
            res = 'update success'
        else:
            res = 'update failed'
        conn.close()
        return render_template("update.html", res=res)
    else:
        # for GET methods
        conn = sqlite3.connect("music_store.db")
        cu = conn.cursor()
        instrument_model.show_one(cu, (ref_number,))
        ref_num, name, cat, url = cu.fetchone()
        instrument = {"ref_num":ref_num, "category": cat,"name":name, "url":url}
        return render_template('update.html', instrument=instrument, res=res)
@app.route('/instruments/delete/<ref_number>', methods=["GET", "DELETE", "POST"])
def delete_instrument(ref_number):
    if request.method == "POST" or  request.method == "DELETE":
        # prepare connection
        conn = sqlite3.connect("music_store.db")
        cu = conn.cursor()
        # instrument delete
        instrument_model.delete_one(cu, (ref_number,))
        # validate
        if cu.rowcount > 0:
            # apply changes
            conn.commit()
            res = "Deleted successfully"
        else:
            res = "Oops, something happened please ask the administrator"
        if request.method == "DELETE":
            return res
        return render_template('delete.html', res=res)
    else:
        conn = sqlite3.connect("music_store.db")
        cu = conn.cursor()
        instrument_model.show_one(cu, (ref_number,))
        ref_num, name, cat, url = cu.fetchone()
        instrument = {"ref_num":ref_num, "category": cat,"name":name, "url":url}
        return render_template('delete.html', instrument=instrument)
        # return redirect(url_for('/instruments/show/all'))
@app.route('/') #root URL
def welcome():
    storedName = request.cookies.get('user_id')
    conn = sqlite3.connect("music_store.db")
    cu = conn.cursor()
    instrument_model.show_all(cu)
    res = [{"ref_num":row[0], "category": row[2],"name":row[1], "url":row[3]} for row in cu]
    conn.close()
    return render_template("welcome.html", instruments=res)
@app.route('/cart/add/<ref_number>')
def add_to_cart(ref_number):
    if 'role' in session and session['role']=='buyer':
        temp = session['cart']
        temp.append(int(ref_number))
        session['cart'] = temp
        res = "added to cart!"
        return render_template('messages.html', message=res)
    else:
        res = "please login as buyer" 
        return render_template('messages.html', message=res) 
# --- SOLUTION ---
# reuse '/cart/show/all' 
@app.route('/cart/show/all')
def show_cart():
    # Retrieve all instruments in our db
    conn = sqlite3.connect("music_store.db")
    cu = conn.cursor()
    instrument_model.show_all(cu)
    if session:
        cart = session['cart']
    else:
        cart = []
    ref_number_count = {}
    for instrument_number in cart:
        if ref_number_count.get(instrument_number) is None:
            ref_number_count[instrument_number] = 0
        ref_number_count[instrument_number] += 1
    res = [{"ref_num":row[0],"category":row[2],"name":row[1],"url":row[3],"count":ref_number_count[row[0]]} for row in cu if row[0] in ref_number_count]
    conn.close()
    return render_template('cart.html', cart=res)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        conn = sqlite3.connect("music_store.db")
        cu = conn.cursor()        
        cu.execute("SELECT fla FROM creds where username = :user", {"user":request.form['username']})
        try: #how many times has this person tried to log in?
            attempts = cu.fetchone()[0] 
        except:
            attempts = 0
        # check failed login attempts
        if attempts < 5:
            cu.execute("SELECT (SELECT password from creds where username=:user) = :form_pass", {"user":request.form['username'], "form_pass":request.form['password']})
            auth = cu.fetchone() # ask sqlite "Does the password from the form match the password in the db?"
            if bool(auth[0]):          
                cu.execute("UPDATE creds SET fla= 0 WHERE username=:user", {"user":request.form['username']})
                conn.commit() # reset password attempts to zero
                session['username'] = request.form['username']
                session['cart'] = []
                session['role'] = users[request.form['username']]['role']
                resp = redirect(url_for('welcome'))
                resp.set_cookie('user_id', session['username'])
                session.permanent = True
                conn.close()
                return resp

            else:
                cu.execute("UPDATE creds SET fla= fla+1 WHERE username=:user", {"user":request.form['username']})
                conn.commit() #increment the bad login attempts
                conn.close()
                res = f"invalid user/password- attempt #{attempts+1}"
                return render_template('messages.html', message=res)
        else:
            res = f"Your account is locked after {attempts} unsuccessful attempts"
            return render_template('messages.html', message=res)


    user_id = request.cookies.get('user_id') or ''
    return f'''
        <form method="post">
            <p><input type=text name=username value={user_id}>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''
@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('cart')
    session.pop('role')
    resp = redirect(url_for('welcome'))
    resp.set_cookie('user_id', '')
    return resp
@app.route('/greeting')
def greeting():
    print('[DEBUG][greeting]::', session)
    return 'Good morning!'