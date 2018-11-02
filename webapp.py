from flask import Flask, request, redirect
from jinja2 import Template
from markov_bullshit_generator import network
import redis
import os

app = Flask(__name__)

@app.route("/")
def hello():
    f=open("template.html")
    template = f.read()
    f.close()
    n=network()
    T = Template(template)
    return T.render(phrase=n.generatePhrase())

@app.route("/upvote")
def getUpvote():
    r = redis.from_url(os.environ.get("REDIS_URL"),db=1)
    r.incr(request.form.get("quote"))
    return redirect("/")

@app.route("/downvote")
def getDownvote():
    r = redis.from_url(os.environ.get("REDIS_URL"),db=1)
    r.decr(request.form.get("quote"))
    return redirect("/")

@app.route("/best")
def getBest():
    r = redis.from_url(os.environ.get("REDIS_URL"),db=1)
    #l=r.keys(pattern="*")
    ret="<table>"
    for k in r.scan_iter():
        ret+="<tr><td>"+k.decode("utf-8")+"</td></tr>"
    ret+="</table>"
    return ret

if __name__ == "__main__":
    app.run(host='0.0.0.0')
