import re
from tkinter.tix import Select
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql

dheadings = ["Add Log","Trackers","Last Time Stamp","Average value"]
ddata = []

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
           usrid=session['usrid']  
           with sql.connect("mad1.db") as con:
               cur = con.cursor()
               cur.execute("Select count(*) from Tracker Where userId=(?)",[usrid])
               number = cur.fetchone()
               count = int(''.join(map(str, number))) 
               
               while(count!=0):
                  count-=1
                  cur.execute("select t.Trackerid,t.Name,max(l.TimeStamp),avg(l.Value)\
                     from Tracker t \
                     left outer join Log l using (TrackerId) where t.UserId=(?)",[usrid])
                  ddata=cur.fetchall()
                  return render_template("dashboard.html",dheadings=dheadings, ddata = ddata)
              
        else:
            flash('Looks you are not registered') 
            return redirect(url_for('login'))


