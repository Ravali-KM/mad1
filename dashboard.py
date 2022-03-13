import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql

app = Flask(__name__)
dheadings = ["Trackers","Last Time Stamp","Average value"]
ddata = []
usrid=''

def dshtable():
    if request.method == 'GET':   
        usrid=session['usrid']  
        with sql.connect("mad1.db") as con:
            cur = con.cursor()
            cur.execute("SELECT t.Name,l.TimeStamp,avg(l.Value) FROM Tracker t, Log l \
                WHERE l.TimeStamp = (SELECT l1.TimeStamp FROM Log l1 ORDER BY l1.LogId \
                    DESC  LIMIT 1)")
            ddata=cur.fetchall()
            return render_template("dashboard.html",dheadings=dheadings, ddata = ddata)
    else:
        flash('error viewing dashboard') 
        return redirect(url_for('login'))