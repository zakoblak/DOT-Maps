from flask import Flask, render_template, request, redirect, url_for, flash
from tinydb import TinyDB, Query

app = Flask(__name__)
app.secret_key = 'skrivni_kljuc'

db = TinyDB('uporabniki.json')
users = db.table('users')
User = Query()

@app.route('/')
def domov():
    return render_template('spletna.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = users.get((User.username == username) & (User.password == password))

    if user:
        flash('Prijava uspešna!', 'success')
    else:
        flash('Napačno uporabniško ime ali geslo.', 'error')

    return redirect(url_for('domov'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = users.get(User.username == username)

        if existing_user:
            flash('Uporabniško ime že obstaja.', 'error')
            return redirect(url_for('register'))

        users.insert({'username': username, 'password': password})
        flash('Registracija uspešna!', 'success')
        return redirect(url_for('domov'))

    return render_template('registracija.html')

if __name__ == '__main__':
    app.run(debug=True)
