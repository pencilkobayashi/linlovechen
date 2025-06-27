from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/notes', methods=['GET', 'POST'])
def handle_notes():
    if request.method == 'POST':
        content = request.json.get('content')
        if not content:
            return jsonify({'error': 'Content is required'}), 400
        
        note = Note(content=content)
        db.session.add(note)
        db.session.commit()
        return jsonify({'id': note.id}), 201
    
    notes = Note.query.order_by(Note.created_at.desc()).all()
    return jsonify([{
        'id': note.id,
        'content': note.content,
        'created_at': note.created_at.isoformat()
    } for note in notes])

if __name__ == '__main__':
    app.run(debug=True)