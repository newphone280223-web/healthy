from flask import Flask, render_template, request, jsonify
from database import db
from scanner import GeminiScanner
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db.init_app(app)
scanner = GeminiScanner()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan')
def scan_page():
    return render_template('scan.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
