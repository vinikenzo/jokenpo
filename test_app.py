import pytest
from jokenpo import app, determine_winner

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200

def test_determine_winner_empate():
    assert determine_winner('pedra', 'pedra') == 'Empate'

def test_determine_winner_voce():
    assert determine_winner('pedra', 'tesoura') == 'Você'

def test_determine_winner_computador():
    assert determine_winner('pedra', 'papel') == 'Computador'

def test_play_invalid_choice(client):
    response = client.post('/play', json={'choice': 'invalido'})
    assert response.status_code == 400

def test_reset(client):
    response = client.post('/reset')
    assert response.status_code == 200
