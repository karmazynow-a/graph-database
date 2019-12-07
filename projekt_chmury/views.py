# -*- coding: utf-8 -*-
from .models import Przystanek, list_all, get_autobus
from flask import Flask, request, session, redirect, url_for, render_template, flash
from urllib.parse import parse_qs, urlparse, urlunparse

import json

def create_app():
  app = Flask(__name__)
  return app

app=create_app()

@app.route('/', methods=['GET','POST'])
def index():
    p = list_all()
    return render_template('index.html', przystanki=p)

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        nazwa = request.form['nazwa']
        ulica = request.form['ulica']
        numer = request.form['numer']

        if len(numer) < 1 or len(ulica) < 3:
            flash('Bledny adres przystanku!')
        elif not Przystanek(nazwa).add(ulica, numer):
            flash('Przystanek z ta nazwa juz istnieje!')
        else:
            return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/add_rel', methods=['GET','POST'])
def add_rel():
    if request.method == 'POST':
        nazwa1 = request.form['nazwa1']
        nazwa2 = request.form['nazwa2']
        autobus = request.form['autobus']
        czas = request.form['czas']

        if nazwa1 == nazwa2:
            flash('Wybierz dwa różne przystanki!')
        elif len(autobus) < 0:
            flash('Podaj numer autobusu')
        elif int(czas) < 1:
            flash('Podaj poprawną wartość czasu!')
        else:
            Przystanek(nazwa1).add_rel(nazwa2, autobus, czas)
            flash('Dodano!')
            return redirect(url_for('index'))

    return render_template('add_rel.html', p1 = list_all(), p2 = list_all())

@app.route('/delete', methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        n = request.form['nazwa']
        Przystanek(n).delete()
        return redirect(url_for('index'))

    p = list_all()
    return render_template('delete.html', przystanki = p)

@app.route('/delete_rel', methods=['GET','POST'])
def delete_rel():
    if request.method == 'POST':
        nazwa1 = request.form['nazwa1']
        nazwa2 = request.form['nazwa2']

        if nazwa1 == nazwa2:
            flash('Wybierz dwa różne przystanki!')
        elif not Przystanek(nazwa1).delete_rel(nazwa2):
            flash('Połączenie nie istnieje!')
        else:
            return redirect(url_for('index'))

    return render_template('delete_rel.html', p1 = list_all(), p2 = list_all())

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        nazwa1 = request.form['nazwa1']
        nazwa2 = request.form['nazwa2']
        if nazwa1 == nazwa2:
            flash('Wybierz dwa różne przystanki!')
        else:
            res = Przystanek(nazwa1).patch(nazwa2)
            trasa = []
            for row in res:
                trasa.append(row)

            if not trasa:
                flash('Brak połączenia!')

            return redirect(url_for('search_res') + "?trasa=" + json.dumps(trasa))

    return render_template('search.html', p1 = list_all(), p2 = list_all())

@app.route('/search_res', methods=['GET','POST'])
def search_res():
    parsed = urlparse(request.url)
    o = parse_qs(parsed.query)['trasa'][0]
    output = json.loads(o)
    if len(output) < 2:
        return redirect(url_for('search'))

    czas = output[-1][1]

    przystanki = ['-']
    for i in range (0, len(output) - 1):
        przystanki.append( get_autobus(output[i][0], output[i+1][0])[0] )

    return render_template('search_res.html', output = output, czas = int(czas), p = przystanki)

@app.route('/modify', methods=['GET','POST'])
def modify():
    if request.method == 'POST':
        n  = request.form['nazwa']
        return redirect(url_for('modify_one') + "?nazwa=" + n)

    p = list_all()
    return render_template('modify.html', przystanki = p)

@app.route('/modify_one', methods=['GET','POST'])
def modify_one():
    if request.method == 'POST':
        nazwa = request.form['nazwa']
        ulica = request.form['ulica']
        numer = request.form['numer']

        if len(numer) < 1 or len(ulica) < 3:
            flash('Bledny adres przystanku!')
        else:
            Przystanek(nazwa).modify(ulica, numer)
            return redirect(url_for('index'))
            
        return redirect(url_for('index'))

    parsed = urlparse(request.url)
    nazwa = parse_qs(parsed.query)['nazwa'][0]

    p = Przystanek(nazwa).find()
    return render_template('modify_one.html', p = p[0][0]['data'])