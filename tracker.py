import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql
import io
import base64
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from user import dashboard


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
   return dashboard(usrid=session['usrid'], msg=msg)


lheadings = ["Time","Value","Note","Edit","Delete"]
ldata = []

def logtable(tid):
   usrid=''
   xvalue=[]
   yvl=[]
   if request.method == 'GET':      
      usrid=session['usrid']
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute('SELECT TimeStamp FROM Log\
            WHERE TrackerId=(?) AND UserId=(?)',[tid,usrid])
         X = cur.fetchall()
         for i in X:
            xvalue.append((i[0])) 
         cur.execute('SELECT Value FROM Log\
            WHERE TrackerId=(?) AND UserId=(?)',[tid,usrid])
         Y = cur.fetchall()
         for i in Y:
            yvl.append(float(i[0]))
         # arr= np.array(X,Y)
         # ar= tuple(arr)
         plt.plot(xvalue, yvl)
         plt.savefig(r'D:\21f1006439\MAD1\mad1\static\images\plot.png')
         
         cur.execute('SELECT LogId,TimeStamp,Value,Note FROM Log \
            WHERE TrackerId=(?) AND UserId=(?)',[tid,usrid])
         ldata = cur.fetchall()
         return render_template('tracker.html',lheadings=lheadings,ldata=ldata,name = 'new_plot', url ='/static/images/plot.png',X=xvalue,Y=yvl)
         
def deltracker(tid):
   if request.method =='GET':
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute('DELETE from tracker where TrackerId=(?)',[tid])
      return dashboard(usrid=session['usrid'], msg="succesfully deleted")
   else:
      return dashboard(usrid=session['usrid'],msg="unsuccesful deletion")
        
def editracker():
   if request.method =='POST':
      tn = request.form['tname']
      td = request.form['tdescription']  
      tt = request.form['ttype']
      ts = request.form['tsettings']      
      tid= request.form['trackerId']
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute("UPDATE Tracker set Name=(?),Description=(?),TrackerType=(?),Settings=(?) where Trackerid=(?) ",(tn,td,tt,ts,tid) )
         con.commit()
         msg = "Record successfully edited"
      con.close()
      return dashboard(usrid=session['usrid'], msg=msg)
      
   else:
      return dashboard(usrid=session['usrid'], msg="unsuccesful modification")
         
def trkedit(tid):
   if request.method=='GET':
      tname=''
      tdsptn=''
      ttype=''
      tsetngs=''
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute("SELECT trackerid, name, description, Trackertype, settings \
         from tracker where trackerid=(?)",[tid])
         trkrdata = cur.fetchall()
         tid = trkrdata[0][0]
         tname = trkrdata[0][1]
         tdsptn = trkrdata[0][2]
         ttype = trkrdata[0][3]
         tsetngs = trkrdata[0][4]
         return render_template('trackeredit.html',tname=tname,tdsptn=tdsptn,ttype=ttype,tsetngs=tsetngs, tid=tid)



