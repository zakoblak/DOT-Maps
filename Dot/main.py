from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from tinydb import TinyDB, Query
import os

app = Flask(__name__)
app.secret_key = 'skrivni_kljuc'

db = TinyDB('uporabniki.json')
users = db.table('users')
User = Query()

points_db = TinyDB('točke.json')
points_table = points_db.table('points')

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

@app.route('/save_point', methods=['POST'])
def save_point():
    """
    Shrani točko z informacijami, ki jih uporabnik vnese.
    """
    point_data = request.json
    points_table.insert(point_data)
    return jsonify({"status": "success", "message": "Točka uspešno shranjena!"}), 200

@app.route('/get_points', methods=['GET'])
def get_points():
    """
    Pridobi vse shranjene točke in jih vrne v GeoJSON formatu.
    """
    points = points_table.all()
    geojson = {"type": "FeatureCollection", "features": []}
    for point in points:
        geojson["features"].append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point['lon'], point['lat']]
            },
            "properties": point['properties']
        })
    return jsonify(geojson)

@app.route('/onas')
def onas():
    return render_template('onas.html')

@app.route('/kontak')
def kontak():
    return render_template('kontak.html')

if __name__ == '__main__':
    app.run(debug=True)
