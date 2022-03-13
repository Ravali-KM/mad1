import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash
import sqlite3 as sql

app = Flask(__name__)
app.secret_key="ravali"

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/insertnewuser',methods = ['POST'])
def adduser():
   msg=''
   if request.method == 'POST':
      try:
         un = request.form['username']
         pwd = request.form['password']         
         
         with sql.connect("mad1.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (UserName,Password)  VALUES (?,?)",(un,pwd) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        con.close()
        return render_template("dashboard.html",msg = msg)
         
@app.route('/checkuser',methods = ['POST'])
def checkuser():
   msg=''
   if request.method == 'POST':  
    un1 = request.form.get('username1')
    pwd = request.form.get('password1')       
    with sql.connect("mad1.db") as con:
        cur = con.cursor()
        cur.execute("SELECT Password FROM users where UserName = (?)",[un1])
        valemail = cur.fetchone()
        if pwd == valemail[0]:
            return render_template("dashboard.html",msg = "successful login") 
              
        else:
            flash('Looks you are not registered') 
            return redirect(url_for('login'))
       


@app.route('/insertnewtracker',methods = ['POST'])
def addtracker():
   msg=''
   if request.method == 'POST':
      try:
         tn = request.form['tname']
         td = request.form['tdescription']  
         tt = request.form['ttype']
         ts = request.form['tsettings']       
         
         with sql.connect("mad1.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Tracker (Name,Description,TrackerType,Settings)  VALUES (?,?,?,?)",(tn,td,tt,ts) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        con.close()
        return render_template("dashboard.html",msg = msg)
         

if __name__=='__main__':
    app.run(debug= True)

