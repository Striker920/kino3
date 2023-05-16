from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField,FileAllowed,FileRequired
from pathlib import Path
from werkzeug.utils import secure_filename
from models import Movie, Review
BASEDIR = Path(__file__).parent
UPLOAD_FOLDER = BASEDIR / 'static' / 'images'
app = Flask(__name__)
db = SQLAlchemy(app)


@app.route('/')
def index():
    movies = Movie.query.order_by(Movie.id.desc()).all()
    return render_template(
        "index.html", movies = movies
    )
@app.route("/movie/<int:id>", methods=["GET","POST"])
def movie(id):
    movie = Movie.query.get(id)
    if movie.reviews:
        avg = round(sum(review.score for review in movie.reviews) / len(movie.reviews),2)
    else:
        avg = 0
    form = Review(score=10)
    if form.validate_on_submit():
        review = Review()
        review.name = form.name.data
        review.text = form.text.data
        review.score = form.score.data
        review.movie_id = movie.id
        db.session.add(review)
        db.session.commit()
        return redirect(url_for("movie", id=movie.id))
    return render_template("movie.html",
                           movie=movie,
                           avg = avg,
                           form=form)
@app.route('/addmovie', methods=['GET','POST'])
def add_movie():
    form = MovieForm()
    if form.validate_on_submit():
        movie = Movie()
        movie.title = form.title.data
        movie.descriptions = form.description.data
        image = form.image.data
        image_name = secure_filename(image.filename)
        UPLOAD_FOLDER.mkdir(exist_ok=True)
        image.save((UPLOAD_FOLDER / image_name))
        movie.image = image_name
        db.session.add(movie)
        db.session.commit()
        return redirect(url_for("movie", id=movie.id))
    return render_template('add_movie.html',
                           form=form)
@app.route('/reviews')
def reviews():
    reviews = Review.query.order_by(Review.created_date.desc()).all()
    return render_template("reviews.html",
                           reviews=reviews)
@app.route('/delete_reviews/<int:id>')
def delete_reviews(id):
    review = Review.query.get(id)
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for('reviews'))
class ReviewForm(FlaskForm):
    name = StringField("Ваше имя",
                        validators=[DataRequired(message="Поле не должно быть пустым")])
    text = TextAreaField("Текст отзыва",
                        validators=[DataRequired(message="Поле не должно быть пустым")])
    score = SelectField("Оценка",
                        choices=[(i,i) for i in range(1,11)])
    submit = SubmitField("Добавить отзыв")
class MovieForm(FlaskForm):
    title = StringField("Название",
                        validators=[DataRequired(message="Поле не должно быть пустым")])
    description = TextAreaField("Описание",
                        validators=[DataRequired(message="Поле не должно быть пустым")])
    image = FileField("Изображение",
                        validators=[FileRequired(message="Поле не должно быть пустым"),
                                    FileAllowed(["jpg","jpeg","png"],message="Неверный формат файла")])
    submit = SubmitField("Добавить файл")
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)