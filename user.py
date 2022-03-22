import re
from tkinter.tix import Select
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql

dheadings = ["Add Log","Trackers","Last Time Stamp","Average value","Edit","Delete"]
ddata = []

def adduser():
   msg=''
   if request.method == 'POST':
      try:
         un = request.form.get('username')
         pwd = request.form.get('password')         
         with sql.connect("mad1.db") as con:
            cur = con.cursor()
            cur.execute("SELECT UserName FROM users")
            uname= cur.fetchall()     
            for i in uname:
              if un in i:
                  raise Exception
              else:  
                  cur.execute("INSERT INTO users (UserName,Password)  VALUES (?,?)",[un,pwd] ) 
                  con.commit()
                  msg = "Record successfully added"
      except Exception:
         con.rollback()
         msg = "username already taken, try again with another user name"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        con.close()
        return render_template("login.html",msg = msg)


def checkuser():
   msg=''
   if request.method == 'POST':  
    un1 = request.form.get('username1')
    pwd = request.form.get('password1')       
    with sql.connect("mad1.db") as con:
        cur = con.cursor()
        cur.execute("SELECT Userid,Password FROM users where UserName = (?)",[un1])
        valemail = cur.fetchone()
        if pwd == valemail[1]:
            usrid=session['usrid']  
            return dashboard(usrid, msg="successfully logged in")
             
        else:
            flash('Looks you are not registered') 
            return render_template('login.html')

def dashboard(usrid, msg):
   with sql.connect("mad1.db") as con:
      cur = con.cursor()
      ddata=[]
      cur.execute("select t.Trackerid,t.Name from tracker t where t.UserId=(?)",[usrid])
      ddata=cur.fetchall()
      fdata=[]
      for i in ddata:
         j=list(i)
         cur.execute("select max(timestamp),avg(value) from log where trackerid=(?)",[i[0]])
         k=cur.fetchall()
         if k[0][0] != None :
            j.append(k[0][0])
            if k[0][1] != None:
               j.append(k[0][1])                     
            fdata.append(j)
         else:
            fdata.append(i)
      return render_template("dashboard.html",dheadings=dheadings, ddata = fdata, msg=msg)

