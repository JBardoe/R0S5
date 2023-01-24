from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import user

def getLogins():
    logins=[]
    file1=open("C:/Users/arron/OneDrive/Documents/GitHub/IA-Website/website/information/logins.csv","r")
    for line in file1:
        data=line.strip().split(",")
        logins.append([data[0],data[1]])
    file1.close()
    return logins

def checkLogin(email):
    logins=getLogins()
    for i in range(len(logins)):
        if logins[i][0] == email:
            return False
    return True

def authenticate(email,pword):
    logins=getLogins()
    for i in range(len(logins)):
        if logins[i][0] == email and logins[i][1] == pword:
            return True
    return False

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email=request.form.get('email')
        pword=request.form.get('password')
        flag=authenticate(email, pword)
        if not flag:
            flash("Incorrect username or password. Please try again.", category='error')
        else:
            return redirect(url_for('auth.login'))
    return render_template("login.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email=request.form.get('email')
        pword=request.form.get('password')
        fname=request.form.get('fname')
        lname=request.form.get('lname')
        cname=request.form.get('cname')
        flag=checkLogin(email)
        if not flag:
            flash("That email is already associated with an account. Please retry.", category='error')
        else:
            newUser = user(email,pword,fname,lname,cname)
            newUser.add()
            return redirect(url_for('auth.login'))
    return render_template("register.html")