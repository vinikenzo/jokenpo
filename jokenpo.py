from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import os

app = Flask(__name__)

SERVER   = os.environ.get('DB_SERVER',   'sql-server-jokenpo-rm559982.database.windows.net')
DATABASE = os.environ.get('DB_NAME',     'db-jokenpo')
USERNAME = os.environ.get('DB_USER',     'sqladmin')
PASSWORD = os.environ.get('DB_PASSWORD', 'SUA_SENHA_AQUI')
DRIVER   = 'ODBC+Driver+18+for+SQL+Server'

connection_string = (
    f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}:1433/{DATABASE}"
    f"?driver={DRIVER}&Encrypt=yes&TrustServerCertificate=no&Connection+Timeout=30"
)

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class Match(db.Model):

    __tablename__ = 'partida'

    id = db.Column(db.Integer, primary_key=True)
    resultado = db.Column(db.String(50))
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))

user_score = 0
computer_score = 0
rounds = 0

@app.route('/')
def index():
    return "Bem-vindo ao Jogo de Jokenpô! Use a rota /play para jogar."

@app.route('/play', methods=['POST'])
def play_game():

    global user_score, computer_score, rounds

    user_choice = request.json.get('choice', '').lower()

    if user_choice not in ['pedra', 'papel', 'tesoura']:

        return jsonify({
            'error': 'Escolha inválida. Escolha entre pedra, papel ou tesoura.'
        }), 400

    computer_choice = random.choice([
        'pedra',
        'papel',
        'tesoura'
    ])

    result = determine_winner(
        user_choice,
        computer_choice
    )

    if result == "Voce":
        user_score += 1

    elif result == "Computador":
        computer_score += 1

    rounds += 1

    player_id = request.json.get('player_id')

    if player_id:

        new_match = Match(
            resultado=result,
            player_id=player_id
        )

        db.session.add(new_match)
        db.session.commit()

    return jsonify({
        'result': result,
        'computer_choice': computer_choice,
        'score': {
            'user': user_score,
            'computer': computer_score,
            'rounds': rounds
        }
    })


def determine_winner(user_choice, computer_choice):

    if user_choice == computer_choice:
        return "Empate"

    elif (
        (user_choice == "pedra" and computer_choice == "tesoura") or
        (user_choice == "tesoura" and computer_choice == "papel") or
        (user_choice == "papel" and computer_choice == "pedra")
    ):

        return "Voce"

    else:

        return "Computador"


@app.route('/reset', methods=['POST'])
def reset_score():

    global user_score, computer_score, rounds

    user_score = 0
    computer_score = 0
    rounds = 0

    return jsonify({
        'message': 'Placar resetado!'
    })

@app.route('/players', methods=['POST'])
def create_player():

    data = request.json

    player = Player(
        nome=data['nome']
    )

    db.session.add(player)
    db.session.commit()

    return jsonify({
        'id': player.id,
        'nome': player.nome
    })

@app.route('/players', methods=['GET'])
def get_players():

    players = Player.query.all()

    result = []

    for p in players:

        result.append({
            'id': p.id,
            'nome': p.nome
        })

    return jsonify(result)


@app.route('/matches', methods=['GET'])
def get_matches():

    matches = Match.query.all()

    result = []

    for m in matches:

        result.append({
            'id': m.id,
            'resultado': m.resultado,
            'player_id': m.player_id
        })

    return jsonify(result)

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=80)
