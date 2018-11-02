from flask import Flask
from markov_bullshit_generator import network

app = Flask(__name__)

@app.route("/")
def hello():
    n=network()
    return n.generatePhrase()
