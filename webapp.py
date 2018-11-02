from flask import Flask
from markov_bullshit_generator import network

app = Flask(__name__)

@app.route("/")
def hello():
    n=network()
    return n.generatePhrase()

if __name__ == "__main__":
    app.run(host='0.0.0.0')
