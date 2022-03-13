import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql

def addlog():
    msg=''
    usrid=''
    ln=''
    ts=''
    lv=''
    ti=''
    if request.method == 'POST':
      ts = request.form['Timestamp']
      lv = request.form['lvalue']  
      ln = request.form['lnote']
      ti = request.form['trackerId']
      usrid=session['usrid']
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute("INSERT INTO log (TimeStamp, Value, Note,UserId, TrackerId)  VALUES (?,?,?,?,?)",(ts,lv,ln,usrid,ti) )
         con.commit()
         msg = "Record successfully added"
         
    return render_template("dashboard.html",msg = [msg,ts,lv,ln,usrid,ti])