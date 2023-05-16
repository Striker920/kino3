from main import db
from datetime import datetime
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    descriptions = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255), nullable=False)
    reviews = db.relationship("Review", back_populates="movie")
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_date = db.Column(db.DateTime, default = datetime.utcnow)
    score = db.Column(db.Integer, nullable=True)
    movie_id = db.Column(db.Integer, db.ForeignKey("movie", onedelete="CASCADE"))
    movie = db.relationship("Movie", back_populates="reviews")