import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql

def addtracker():
   msg=''
   usrid=''
   if request.method == 'POST':
      try:
         tn = request.form['tname']
         td = request.form['tdescription']  
         tt = request.form['ttype']
         ts = request.form['tsettings']       
         usrid=session['usrid']
         with sql.connect("mad1.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Tracker (Name,Description,TrackerType,Settings,UserId)  VALUES (?,?,?,?,?)",(tn,td,tt,ts,usrid) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
        con.close()
        return render_template("dashboard.html",msg = [msg,tn,td,tt,ts,usrid])