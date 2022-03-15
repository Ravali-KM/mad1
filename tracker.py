import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql

def addtracker():
   msg=''
   usrid=''
   if request.method == 'POST':
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

   con.close()
   return render_template("dashboard.html",msg = [msg,tn,td,tt,ts,usrid])


lheadings = ["Time","Value","Note"]
ldata = []

def logtable(tid):
   usrid=''
   if request.method == 'GET':
      usrid=session['usrid']
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute('SELECT LogId,TimeStamp,Value,Note FROM Log \
            WHERE TrackerId=(?) AND UserId=(?)',[tid,usrid])
         ldata = cur.fetchall()
         return render_template('tracker.html',lheadings=lheadings,ldata=ldata)
         
         
        
         
         