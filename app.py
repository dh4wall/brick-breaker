from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from auth import login_user, register_user, logout_user
from database import get_high_scores, update_high_score
from game import start_game
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key")

@app.route('/')
def index():
    if 'user_id' in session:
        high_scores = get_high_scores()
        return render_template('index.html', logged_in=True, high_scores=high_scores)
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = login_user(email, password)
        if user:
            session['user_id'] = user['id']
            session['username'] = user['name']
            return redirect(url_for('index'))
        return render_template('login.html', error="Invalid credentials")
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if register_user(name, email, password):
            return redirect(url_for('index'))
        return render_template('register.html', error="Email already exists")
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/play')
def play():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    high_scores = get_high_scores()
    return render_template('game.html', high_scores=high_scores)

@app.route('/game/update', methods=['POST'])
def update_game():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    data = request.json
    game_state = start_game(data)
    if game_state.get('state') == 'game_over':
        update_high_score(session['user_id'], game_state['score'])
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)