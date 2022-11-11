#python3
#Flask version:0.12.2
#Jinja2: 2.10
from flask import Flask, request
from jinja2 import Template
app = Flask(__name__)
@app.route("/")
def index():
    name = request.args.get('name', 'guest')
    t = Template("Hello " + name)
    return t.render()
if __name__ == "__main__":
    app.run('0.0.0.0');