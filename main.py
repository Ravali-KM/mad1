import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql
from log import *
from user import *
from tracker import *
from dashboard import *


app = Flask(__name__)
app.secret_key="ravali"

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/insertnewuser',methods = ['POST'])
def insertuser():
   return adduser()

@app.route('/dashboard',methods = ['POST'])
def chckuser():
   return checkuser()

@app.route('/newtracker')
def newtracker():
   return render_template('createtracker.html')

@app.route('/insertnewtracker',methods = ['POST'])
def inserttracker():
   return addtracker()

@app.route('/log/<int:trackerid>/<string:trackername>')
def insertlog(trackerid: int, trackername: str):
   return render_template('addlog.html',ti=trackerid, tn=trackername)

@app.route('/addlog', methods =['POST'])
def newlog():
   return addlog()

# @app.route('/dashboard')
# def dtable():
#    render_template("dashboard.html")
#    return dshtable()
         

if __name__=='__main__':
    app.run(debug= True)

