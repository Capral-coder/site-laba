from django.shortcuts import render

import pandas as pd
from pathlib import Path
import sqlite3 as sql


def index(request):
    return render(request,'index.html')


def purchase(request):
    try:
        FLS=request.POST['FLS']
        subject_name=request.POST['subjectname']
        work_number=request.POST['worknumber']
        variant=request.POST['variant']

        dbc=sql.connect(Path('./database.sql/'))
        dbcursor=dbc.cursor()

        dbcursor.execute('''CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lastname_firstname_surname TEXT,
            subject_name TEXT,
            work_number INTEGER,
            variant INTEGER)''')
        dbc.commit()

        try:
            dbcursor.execute('''INSERT INTO orders (lastname_firstname_surname, subject_name,work_number, variant) VALUES(?, ?, ?, ?)''',(FLS, subject_name, work_number, variant))
            dbc.commit()
            dbcursor.close()
            dbc.close()
            purchase_status='Замовлення оброблюється'
        except:
            purchase_status='Помилка'
        return render(request, 'purchase.html', {'purchase_status':purchase_status})
    except:
        return render(request, 'purchase.html')


def signin(request):
    try:
        login=request.POST['login']
        password=request.POST['password']
        dbc=sql.connect(Path('./database.sql/'))
        dbcursor=dbc.cursor()
        try:
            dbcursor.execute(f'SELECT is_admin FROM data WHERE e_mail="{login}"')
            if dbcursor.fetchall()[0][0] == 'True':
                dbcursor.execute(f'SELECT password FROM data WHERE e_mail="{login}"')
                if dbcursor.fetchall()[0][0] == password:
                    idd=sql.execute('SELECT id FROM orders')
                    FLS=sql.execute('SELECT (lastname, firstname, surname) FROM order')
                    dbcursor.close()
                    dbc.close()
                    return render(request, 'table.html' ,{'id':idd, 'FLS':FLS})
                else:
                    warning_signin='Неправильний логін або пароль'
                    return render(request, 'signin.html', {'warning_signin':warning_signin})
            else:
                warning_signin='Ви не адміністратор. Доступ заборонено'
                return render(request, 'signin.html', {'warning_signin':warning_signin})
        except:
            warning_signin='Неправильний логін або пароль'
            return render(request, 'signin.html', {'warning_signin':warning_signin})
    except:
        return render(request, 'signin.html')

def signup(request):
    try:
        lastname=request.POST['lastname']
        firstname=request.POST['firstname']
        surname=request.POST['surname']
        email=request.POST['email']
        password=request.POST['password']
        passwordagain=request.POST['passwordagain']


        dbc=sql.connect(Path('./database.sql/'))
        dbcursor=dbc.cursor()
        dbcursor.execute('''CREATE TABLE IF NOT EXISTS data(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lastname TEXT,
            firstname TEXT,
            surname TEXT,
            e_mail TEXT,
            password TEXT,
            gift TEXT,
            is_admin TEXT)''')
        dbc.commit()
        
        try:
            if password == passwordagain and len(password) >= 8:
                dbcursor.execute('''INSERT INTO data (lastname, firstname, surname, e_mail, password, gift, is_admin) VALUES(?, ?, ?, ?, ?, ?, ?)''', (lastname, firstname, surname, email, password, '', 'False'))
                dbc.commit()
                dbcursor.close()
                dbc.close()
                warning_signup='Ви успішно зареєструвались'
            else:
                if len(password) < 8:
                    warning_signup='Ваш пароль не надійний'
                else:
                    warning_signup='Паролі не збігаються'
        except:
            warning_signup='Помилка'
        return render(request, 'signup.html', {'warning_signup':warning_signup})
    except:
        return render(request, 'signup.html')
        
        