import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql

def adduser():
   msg=''
   if request.method == 'POST':
      try:
         un = request.form.get('username')
         pwd = request.form.get('password')         
         with sql.connect("mad1.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (UserName,Password)  VALUES (?,?)",[un,pwd] )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        con.close()
        return render_template("login.html",msg = [msg,un,pwd])


def checkuser():
   msg=''
   if request.method == 'POST':  
    un1 = request.form.get('username1')
    pwd = request.form.get('password1')       
    with sql.connect("mad1.db") as con:
        cur = con.cursor()
        cur.execute("SELECT Userid,Password FROM users where UserName = (?)",[un1])
        valemail = cur.fetchone()
        session['usrid']=valemail[0]
        if pwd == valemail[1]:
           return render_template("createtracker.html", msg =session['usrid']) 
              
        else:
            flash('Looks you are not registered') 
            return redirect(url_for('login'))

