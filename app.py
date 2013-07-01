#! usr/local/bin/python

from flask import Flask, session, g, config, render_template


DEBUG = True
app = Flask(__name__)

app.config.from_object(__name__)

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(port=5001)