import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql
import io
import base64

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


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
      fig = Figure()
      axis = fig.add_subplot(1, 1, 1)
      axis.set_title("Graph")
      axis.set_xlabel("Time")
      axis.set_ylabel("Values")
      axis.grid()
      axis.plot(range(5), range(5), "ro-")
      
      # Convert plot to PNG image
      pngImage = io.BytesIO()
      FigureCanvas(fig).print_png(pngImage)
      
      # Encode PNG image to base64 string
      pngImageB64String = "data:image/png;base64,"
      pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
      
    

      usrid=session['usrid']
      with sql.connect("mad1.db") as con:
         cur = con.cursor()
         cur.execute('SELECT LogId,TimeStamp,Value,Note FROM Log \
            WHERE TrackerId=(?) AND UserId=(?)',[tid,usrid])
         ldata = cur.fetchall()
         return render_template('tracker.html',lheadings=lheadings,ldata=ldata,image=pngImageB64String)
         
         
        
         
         