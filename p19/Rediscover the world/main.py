from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route('/')
def index():
    n = random.randint(0, 25000)
    return render_template('index.html', n=n)

@app.route('/about')
def about():
    return f"<h2>About me</h2>"

@app.route('/Yevhen')
def Yevhen():
    return f"<h3> Dota </h3>"


@app.route('/login')
def login():
    n = 3 + 2497
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)

