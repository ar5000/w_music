#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, send_file
import requests
import json
import random
import xml.etree.ElementTree as ET
# from instrument_helpers import getsongsterr
import instruments

# [MODELS]
import instrument_model
# [APP START]
app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'this_IS_$up3r_SECUR3~'

@app.route('/instruments/show/all')
def show_all():
    if 'role' not in session or session['role']!='admin':
        res = "for admin only, please login"
        return render_template('messages.html', message=res)
    return render_template('index.html', instruments=instruments.Instrument.getall())

@app.route('/instruments/show/<ref_number>', methods=["GET", "POST"])
def show_detail_page(ref_number):
    instr = instruments.Instrument(ref=ref_number)
    reviews = instruments.Review.get_all_reviews(ref_number)
    message = ''
    if request.method == "POST":
        review = instruments.Review(ref=int(request.form['ref']), id= session['username'], stars= request.form['stars'], review= request['review'])
        message = review.post_review()
    return render_template("detailed.html", instrument=instr.todict(), reviews= reviews, message= message)



@app.route('/instruments/create', methods=["GET", "POST"])
def create_instrument():
    if request.method == "POST":    
        instr = instruments.Instrument(ref=int(request.form['ref']), name = request.form['name'], cat = request.form['category'], image= request.form['url']) 
        return instr.add_instrument()
    else:
        # this is GET
        return render_template("create_instrument.html")




@app.route('/instruments/update/<ref_number>', methods=['GET', 'POST'])
def update_one_instrument(ref_number):
    # res = ''
    if request.method == 'POST':
        instr = instruments.Instrument(ref=int(request.form['ref']), name = request.form['name'], cat = request.form['category'], image= request.form['url'])
        return render_template("new_update.html", message=instr.update_instrument())
    else:
        # for GET methods
        instr = instruments.Instrument(ref=ref_number) 
        return render_template('new_update.html', instrument=instr.todict())


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
        instr = instruments.Instrument(ref=ref_number) 
        return render_template('delete.html', instrument=instr.todict())
        # return redirect(url_for('/instruments/show/all'))


@app.route('/') #root URL
def welcome():
    return render_template("welcome.html", instruments=instruments.Instrument.getall())


@app.route('/cart/add/<ref_number>')
def add_to_cart(ref_number):
    if 'role' in session and session['role']=='buyer':
        conn = sqlite3.connect("music_store.db")
        cu = conn.cursor()
        cu.execute("UPDATE creds SET cart = cart || :item WHERE username=:user", {"item":ref_number+',', "user":session['username']})
        conn.commit()

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
    conn = sqlite3.connect("music_store.db")
    cu = conn.cursor()
    try: 
        cu.execute("SELECT cart FROM creds WHERE username = :user", {"user":session['username']})
        cart = list(map(int, cu.fetchmany()[0][0].split(',')[:-1]))
    except:
        cart = []
    
    all_instr = instruments.Instrument.makelist()

    ref_number_count = {}
    for instrument_number in cart:
        if ref_number_count.get(instrument_number) is None:
            ref_number_count[instrument_number] = 0
        ref_number_count[instrument_number] += 1
    res = [{"ref_num":row[0],"category":row[2],"name":row[1],"url":row[3],"count":ref_number_count[row[0]]} for row in all_instr if row[0] in ref_number_count]
   
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
                cu.execute("SELECT cart, Role_desc FROM creds JOIN Roles ON role = Role_num WHERE creds.username=:user", {"user":request.form['username']})
                cart, role = cu.fetchone()
                if cart:
                    session['cart']= list(map(int, (cart.split(',')[:-1])))
                session['role'] = role
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
    return render_template('login.html', message=user_id)
    #     <form method="post">
    #         <p><input type=text name=username value={user_id}>
    #         <p><input type=password name=password>
    #         <p><input type=submit value=Login>
    #     </form>
    # '''

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