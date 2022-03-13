import re
from django.shortcuts import render
from flask import Flask, redirect,  url_for, render_template, request,flash, session
import sqlite3 as sql
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

@app.route('/checkuser',methods = ['POST'])
def chckuser():
   return checkuser()
       
@app.route('/insertnewtracker',methods = ['POST'])
def inserttracker():
   return addtracker()

@app.route('/dashboard', methods=['POST'])
def dtable():
   return dshtable()
         

if __name__=='__main__':
    app.run(debug= True)

