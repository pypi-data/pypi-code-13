"""
.. module:: views
   :synopsis: flask views for demo and api.

.. moduleauthor:: Jai Chaudhary <jai.chaudhary.iitd@gmail.com>


"""

from flask import render_template
from flask import request
from flask import jsonify
from piglatintranslation import app

from .pig_latin_translation import translate_text

@app.route('/', methods=['GET','POST'])
@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == "POST" and request.form['text'] != "":
        return render_template('index.html',
            default_text=request.form['text'],
            translation=translate_text(request.form['text']))

    default_text = 'Where is the toilet?'
    return render_template('index.html',
        default_text=default_text,
        translation=translate_text(default_text))

@app.route('/api/translate', methods=['POST'])
def translate():
    return jsonify({
        'text' : translate_text(request.form['text']),})