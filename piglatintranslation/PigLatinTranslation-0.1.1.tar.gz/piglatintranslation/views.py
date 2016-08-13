from flask import render_template
from flask import request
from flask import jsonify
from app import app

from app.pig_latin_translation import translate_text

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/api/translate', methods=['POST'])
def translate():
    return jsonify({
        'text' : translate_text(request.form['text']),})