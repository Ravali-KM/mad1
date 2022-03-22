import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql
from tracker import *

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
         
    return dashboard(usrid=session['usrid'], msg=msg)

def dellog(lid):
  if request.method =='GET':
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute('DELETE from log where LogId=(?)',[lid])
      return dashboard(usrid=session['usrid'], msg="succesfully deleted")
  else:
      return dashboard(usrid=session['usrid'], msg="unsuccesful deletion")


def edtlog():
  if request.method =='POST':
    lts = request.form['Timestamp']
    lval = request.form['lvalue']
    lnt = request.form['lnote']
    lid = request.form['LogId']
    with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute("UPDATE Log set TimeStamp=(?),Value=(?),Note=(?) where logid=(?) ",(lts,lval,lnt,lid) )
         con.commit()
         msg = "Record successfully edited"
    con.close()
    return dashboard(usrid=session['usrid'], msg=msg)
      
  else:
      return dashboard(usrid=session['usrid'], msg="unsuccesful modification")
         
        
def logedit(lid):
  if request.method == "GET":
    ltmstmp =''
    lval=''
    lnote =''
    with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute("SELECT logid, TimeStamp, Value, Note, trackerid\
         from Log where logid=(?)",[lid])
         logdata = cur.fetchall()
         lid = logdata[0][0]
         ltmstmp = logdata[0][1]
         lval = logdata[0][2]
         lnote = logdata[0][3]
         tid = logdata[0][4]
         cur.execute("select name from tracker where trackerid = (?)", [tid])
         tname = cur.fetchone()
         return render_template('editlog.html',ltmstmp=ltmstmp,lval=lval,lnote=lnote, lid=lid, tname= tname[0])
    