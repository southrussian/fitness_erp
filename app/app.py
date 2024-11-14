from flask import Flask, request, render_template
from models import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello world'


if __name__ == '__main__':
    app.run(debug=True, port=6000)
