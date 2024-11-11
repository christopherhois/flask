from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import pyotp
import pymongo
import requests
app = Flask(__name__)

# Konfigurationen
app.config['JWT_SECRET_KEY'] = 'dein_secret_key'
client = MongoClient('mongo', 27017)
db = client.govent

jwt = JWTManager(app)

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # Admin, HR, Chef, Mitarbeiter

    if not username or not password or not role:
        return jsonify(message="Fehlende Angaben."), 400

    # Überprüfen, ob der Benutzer bereits existiert
    if db.users.find_one({'username': username}):
        return jsonify(message="Benutzer existiert bereits."), 400

    # Passwort hashen und Benutzer speichern
    hashed_password = generate_password_hash(password)
    db.users.insert_one({
        'username': username,
        'password': hashed_password,
        'role': role,
        'otp_secret': None  # wird später gesetzt, wenn 2FA aktiviert wird
    })

    return jsonify(message="Benutzer erfolgreich registriert."), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify(message="Fehlende Angaben."), 400

    # Benutzer aus der Datenbank abrufen
    user = db.users.find_one({'username': username})

    if not user or not check_password_hash(user['password'], password):
        return jsonify(message="Falscher Benutzername oder Passwort."), 401

    # JWT-Token erstellen
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200

@app.route('/api/pt', methods=['POST'])
@jwt_required()
def add_pt():
    current_user = get_jwt_identity()
    data = request.get_json()
    customer = data.get('customer')
    value = data.get('value')
    date = data.get('date')

    if not customer or value is None or not date:
        return jsonify(message="Fehlende Angaben."), 400

    # PT-Wert in der Datenbank speichern
    db.pt_values.insert_one({
        'user_id': current_user,
        'customer': customer,
        'value': value,
        'date': date
    })

    return jsonify(message="PT-Wert erfolgreich hinzugefügt."), 201



@app.route('/api/pt', methods=['GET'])
@jwt_required()
def get_pt_values():
    current_user = get_jwt_identity()
    user = db.users.find_one({'username': current_user})

    if user['role'] == 'Admin':
        # Admin kann alle PT-Werte sehen
        pt_values = list(db.pt_values.find())
    else:
        # Andere Benutzer sehen nur ihre eigenen PT-Werte
        pt_values = list(db.pt_values.find({'user_id': current_user}))

    # Konvertiere MongoDB-Ergebnis in eine Liste von JSON-kompatiblen Objekten
    for pt_value in pt_values:
        pt_value['_id'] = str(pt_value['_id'])  # Konvertiere _id zu String

    return jsonify(pt_values), 200

@app.route('/api/pt/<pt_id>', methods=['PUT'])
@jwt_required()
def update_pt_value(pt_id):
    current_user = get_jwt_identity()
    user = db.users.find_one({'username': current_user})

    data = request.get_json()
    new_value = data.get('value')

    if new_value is None:
        return jsonify(message="Fehlende Angaben."), 400

    # Überprüfe, ob der PT-Wert existiert
    pt_value = db.pt_values.find_one({'_id': pymongo.ObjectId(pt_id)})

    if not pt_value:
        return jsonify(message="PT-Wert nicht gefunden."), 404

    # Nur Admins oder der Benutzer, der den PT-Wert erstellt hat, dürfen bearbeiten
    if user['role'] != 'Admin' and pt_value['user_id'] != current_user:
        return jsonify(message="Zugriff verweigert."), 403

    # PT-Wert aktualisieren
    db.pt_values.update_one({'_id': pymongo.ObjectId(pt_id)}, {'$set': {'value': new_value}})

    return jsonify(message="PT-Wert erfolgreich aktualisiert."), 200


@app.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    user = db.users.find_one({'username': current_user})

    if user['role'] != 'Admin':
        return jsonify(message="Zugriff verweigert."), 403

    # Alle Benutzer aus der Datenbank abrufen
    users = list(db.users.find({}, {'password': 0}))  # Passwort wird aus Sicherheitsgründen nicht mitgesendet

    # Konvertiere MongoDB-Ergebnis in eine Liste von JSON-kompatiblen Objekten
    for user in users:
        user['_id'] = str(user['_id'])  # Konvertiere _id zu String

    return jsonify(users), 200


@app.route('/api/pt/<pt_id>', methods=['DELETE'])
@jwt_required()
def delete_pt_value(pt_id):
    current_user = get_jwt_identity()
    user = db.users.find_one({'username': current_user})

    if user['role'] != 'Admin':
        return jsonify(message="Zugriff verweigert."), 403

    # Überprüfen, ob der PT-Wert existiert
    pt_value = db.pt_values.find_one({'_id': pymongo.ObjectId(pt_id)})

    if not pt_value:
        return jsonify(message="PT-Wert nicht gefunden."), 404

    # PT-Wert löschen
    db.pt_values.delete_one({'_id': pymongo.ObjectId(pt_id)})

    return jsonify(message="PT-Wert erfolgreich gelöscht."), 200



# Beispiel: Benutzer-Einladung per E-Mail
@app.route('/api/invite_user', methods=['POST'])
@jwt_required()
def invite_user():
    current_user = get_jwt_identity()
    user = db.users.find_one({'username': current_user})

    if user['role'] not in ['Admin', 'HR']:
        return jsonify(message="Zugriff verweigert."), 403

    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify(message="E-Mail-Adresse fehlt."), 400

    # Sende E-Mail an den neuen Benutzer
    email_payload = {
        'to': email,
        'subject': 'Willkommen bei Govent!',
        'text': 'Bitte klicken Sie auf den folgenden Link, um Ihr Passwort einzurichten: http://example.com/setup-password'
    }
    try:
        response = requests.post('http://email-service:3001/send-email', json=email_payload)
        if response.status_code == 200:
            return jsonify(message="Einladungs-E-Mail erfolgreich gesendet."), 200
        else:
            return jsonify(message="Fehler beim Senden der E-Mail."), 500
    except requests.exceptions.RequestException as e:
        return jsonify(message=f"Fehler beim E-Mail-Service: {str(e)}"), 500

@app.route('/api/users/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user = get_jwt_identity()
    user = db.users.find_one({'username': current_user})

    if user['role'] != 'Admin':
        return jsonify(message="Zugriff verweigert."), 403

    # Überprüfen, ob der Benutzer existiert
    target_user = db.users.find_one({'_id': pymongo.ObjectId(user_id)})

    if not target_user:
        return jsonify(message="Benutzer nicht gefunden."), 404

    # Benutzer löschen
    db.users.delete_one({'_id': pymongo.ObjectId(user_id)})

    return jsonify(message="Benutzer erfolgreich gelöscht."), 200


@app.route('/api/setup_2fa', methods=['GET'])
@jwt_required()
def setup_2fa():
    user_id = get_jwt_identity()
    secret = pyotp.random_base32()
    # Speichere den Secret mit dem Benutzer in der DB
    db.users.update_one({'username': user_id}, {'$set': {'otp_secret': secret}}, upsert=True)
    return jsonify(secret=secret), 200

@app.route('/api/verify_otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    otp = data.get('otp')
    user_id = data.get('user_id')
    user = db.users.find_one({'username': user_id})
    if not user or 'otp_secret' not in user:
        return jsonify(message="Benutzer oder OTP-Secret nicht gefunden"), 404

    secret = user['otp_secret']
    totp = pyotp.TOTP(secret)
    if totp.verify(otp):
        return jsonify(message="OTP erfolgreich verifiziert"), 200
    else:
        return jsonify(message="Ungültiger OTP"), 401

@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify(message="Dies ist eine geschützte Route."), 200

@app.route('/api/add_user', methods=['POST'])
@jwt_required()
def add_user():
    # Überprüfen, ob der aktuelle Benutzer ein Admin oder HR ist
    current_user = get_jwt_identity()
    user = db.users.find_one({'username': current_user})
    if user['role'] not in ['Admin', 'HR']:
        return jsonify(message="Zugriff verweigert."), 403

    # Neue Benutzerdaten
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  # Chef, Mitarbeiter

    if not username or not password or not role:
        return jsonify(message="Fehlende Angaben."), 400

    # Benutzer bereits vorhanden?
    if db.users.find_one({'username': username}):
        return jsonify(message="Benutzer existiert bereits."), 400

    # Passwortanforderungen überprüfen
    if len(password) < 6:
        return jsonify(message="Passwort muss mindestens 6 Zeichen lang sein."), 400

    # Passwort hashen und Benutzer speichern
    hashed_password = generate_password_hash(password)
    db.users.insert_one({
        'username': username,
        'password': hashed_password,
        'role': role,
        'otp_secret': None  # wird später gesetzt
    })

    @app.route('/api/reset_password', methods=['POST'])
    @jwt_required()
    def reset_password():
        # Überprüfen, ob der aktuelle Benutzer ein Admin oder HR ist
        current_user = get_jwt_identity()
        user = db.users.find_one({'username': current_user})
        if user['role'] not in ['Admin', 'HR']:
            return jsonify(message="Zugriff verweigert."), 403

        # Daten des Benutzers, dessen Passwort zurückgesetzt werden soll
        data = request.get_json()
        username = data.get('username')
        new_password = data.get('new_password')

        if not username or not new_password:
            return jsonify(message="Fehlende Angaben."), 400

        # Überprüfen, ob Benutzer existiert
        target_user = db.users.find_one({'username': username})
        if not target_user:
            return jsonify(message="Benutzer nicht gefunden."), 404

        # Neues Passwort hashen und speichern
        if len(new_password) < 6:
            return jsonify(message="Passwort muss mindestens 6 Zeichen lang sein."), 400

        hashed_password = generate_password_hash(new_password)
        db.users.update_one({'username': username}, {'$set': {'password': hashed_password}})

        return jsonify(message="Passwort erfolgreich zurückgesetzt."), 200

    return jsonify(message="Benutzer erfolgreich hinzugefügt."), 201


@app.route('/api/change_password', methods=['POST'])
@jwt_required()
def change_password():
    current_user = get_jwt_identity()
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password or len(new_password) < 6:
        return jsonify(message="Das neue Passwort muss mindestens 6 Zeichen lang sein."), 400

    # Passwort des aktuellen Benutzers ändern
    hashed_password = generate_password_hash(new_password)
    db.users.update_one({'username': current_user}, {'$set': {'password': hashed_password}})

    return jsonify(message="Passwort erfolgreich geändert."), 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
