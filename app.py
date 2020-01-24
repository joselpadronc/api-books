import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields
from books import Books

dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/db_books.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Books(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	description = db.Column(db.String(255))
	author = db.Column(db.String(100))
	launching = db.Column(db.String(100))


class BookSchema(Schema):
	id = fields.Int()
	title = fields.Str()
	description = fields.Str()
	author = fields.Str()
	launching = fields.Str()

@app.route('/')
def index():
	return jsonify({"ping": "pong"})

	
#Obtener la lista de libros
@app.route('/api/books', methods=["GET"])
def  get_books():
	books_list = Books.query.all()
	
	book_schema = BookSchema(many=True)
	results = book_schema.dump(books_list)

	return jsonify(results)


#Buscar libro
@app.route('/api/books/<int:book_id>', methods=["GET"])
def search_book(book_id):
	book_found = Books.query.filter_by(id=book_id).first()

	print("query done", book_found.title)
	return jsonify(
		{"title":book_found.title,
		"description":book_found.description,
		"author":book_found.author,
		"launching":book_found.launching}
	)



#Publicar nuevo libro
@app.route('/api/books/', methods=["POST"])
def add_book():

	if request.method == 'POST':
		new_book = Books(
			title=request.json["title"],
			description=request.json["description"],
			author=request.json["author"],
			launching=request.json["launching"]
		)
	
		db.session.add(new_book)
		db.session.commit()

		return jsonify({"message": "The book is added"})
	
	else:
		return jsonify({"message": "The book isn\'t added"})


#Eliminar un libro
@app.route('/api/books/<int:book_id>', methods=["DELETE"])
def remove_book(book_id):
	book_found = Books.query.filter_by(id=book_id).first()

	db.session.delete(book_found)
	db.session.commit()

	print("query done", book_found.title)
	return jsonify({"message":"Book deleted"})


#Actulizar o editar un libro
@app.route('/api/books/<int:book_id>', methods=["GET", "PUT"])
def update_book(book_id):
	book_found = Books.query.filter_by(id=book_id).first()
		
	book_found.title      = request.json["title"]
	book_found.description= request.json["description"]
	book_found.author     = request.json["author"]
	book_found.launching  = request.json["launching"]

	db.session.add(book_found)
	db.session.commit()

	print("Book updated", book_found.title)
	return jsonify(
		{"title": book_found.title,
     "description": book_found.description,
     "author": book_found.author,
     "launching": book_found.launching}
	)


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True, port=8080)
