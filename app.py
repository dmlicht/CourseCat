#! usr/local/bin/python

from flask import Flask, session, g, config, render_template, request
from flask.ext.wtf import Form, TextField, ValidationError, Required


DEBUG = True
app = Flask(__name__)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'devkey'


class SubmitForm(Form):
    name = TextField('Name', description='Short title of course/tutorial')
    url = TextField('URL', description='Where can the course/tutorial be found on the web?')

@app.route('/', methods = ('GET', 'POST',))
def home():
	form = SubmitForm()
	return render_template('home.html', form=form)

if __name__ == '__main__':
    app.run(port=5001)