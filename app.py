from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(120))

    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

  #  def __repr__(self):
   #     return '<User {}>'.format(self.last_name)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    description = db.Column(db.String(140))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    author = db.relationship('Author', backref='books')

    def __init__(self, title, description, author_id):
        self.title = title
        self.description = description
        self.author_id = author_id

    #def __repr__(self):
     #   return '<Post {}>'.format(self.title)


class AuthorSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('first_name', 'last_name', 'id')


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True)


class BookSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'description', 'author_id', 'id')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

#create author
@app.route("/author", methods=["POST"])
def add_author():
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    new_author = Author(first_name, last_name)

    db.session.add(new_author)
    db.session.commit()
    author = Author.query.first()
    output = author_schema.dump(author).data

    return jsonify({'author': output})


@app.route("/book", methods=["POST"])
def add_book():
    title = request.json['title']
    description = request.json['description']
    author_id = request.json['author_id']

    new_book = Book(title, description, author_id)

    db.session.add(new_book)
    db.session.commit()
    book = Book.query.first()
    output = book_schema.dump(book).data

    return jsonify({'book': output})


#get all authors
@app.route("/author", methods=["GET"])
def get_author():
    all_authors = Author.query.all()
    result = authors_schema.dump(all_authors)
    return jsonify(result.data)

#get all authors
@app.route("/book", methods=["GET"])
def get_book():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result.data)

#update by id
@app.route("/author/<id>", methods=["PUT"])
def author_update(id):
    author = Author.query.get(id)
    first_name = request.json['first_name']
    last_name = request.json['last_name']

    author.first_name = first_name
    author.last_name = last_name

    db.session.commit()
    return author_schema.jsonify(author)


#delete by id
@app.route("/author/<id>", methods=["DELETE"])
def author_delete(id):
    author = Author.query.get(id)
    db.session.delete(author)
    db.session.commit()

    return author_schema.jsonify(author)


if __name__ == '__main__':
    app.run(port=7887)
