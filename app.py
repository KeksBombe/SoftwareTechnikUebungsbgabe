from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(data_dir, "movies.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Movie(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
@app.route('/movies', methods=['GET'])
def get_all_movies():
    movies = Movie.query.all()
    return jsonify([movie.to_dict() for movie in movies]), 200
@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Filmname fehlt'}), 400
    new_movie = Movie(name=data['name'])
    try:
        db.session.add(new_movie)
        db.session.commit()
        return jsonify(new_movie.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Film konnte nicht hinzugefügt werden'}), 500 
@app.route('/movies/<movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie:
        return jsonify(movie.to_dict()), 200
    else:
        return jsonify({'error': 'Film nicht gefunden'}), 404
@app.route('/movies/name/<movie_name>', methods=['GET'])
def get_movies_by_name(movie_name):
    movies = Movie.query.filter(Movie.name.ilike(movie_name)).all()
    return jsonify([movie.to_dict() for movie in movies]), 200 
@app.route('/movies/id/<movie_id>', methods=['DELETE'])
def delete_movie_by_id(movie_id):
    movie = Movie.query.filter_by(id=movie_id).first() 
    if movie:
        try:
            db.session.delete(movie)
            db.session.commit()
            return '', 204
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Film konnte nicht gelöscht werden'}), 500
    else:
        return jsonify({'error': 'Film nicht gefunden'}), 404