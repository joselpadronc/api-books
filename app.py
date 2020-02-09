import os
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from json_serializable import JSONSerializable
from books import Books

dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/db_books.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
JSONSerializable(app)


def error_handler(err, msg, detail=None):
	return jsonify(err=err, msg=msg, detail=detail)


@app.errorhandler(500)
def internal_server_error(e):
	return error_handler(500, 'Internal Server Error', str(e))


@app.errorhandler(400)
def bad_request(e):
	return error_handler(400, 'Bad request', str(e))


@app.errorhandler(404)
def not_found(e):
	return error_handler(404, 'Not Found endpoint', str(e))


class Books(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80))
	description = db.Column(db.String(255))
	author = db.Column(db.String(100))
	launching = db.Column(db.String(100))



@app.route('/')
def index():
	return jsonify({"ping": "pong"})

	
#Obtener la lista de libros
@app.route('/api/books', methods=["GET"])
def  get_books():
	try:
		return jsonify(ok=True, items=Books.query.all())
        except Exception as e:
		abort(500)


#Buscar libro
@app.route('/api/books/<int:book_id>', methods=["GET"])
def search_book(book_id):
	
	if request.method == 'GET':
		book_found = Books.query.filter_by(id=book_id).first()

		return jsonify(
			{
				"title":book_found.title,
				"description":book_found.description,
				"author":book_found.author,
				"launching":book_found.launching
			}
		)
	
	else:
		return jsonify({"message": "Book not found"})



#Publicar nuevo libro
@app.route('/api/books/', methods=["POST"])
def add_book():

	if request.method == 'POST':
		new_book = Books(
			title				= request.json["title"],
			description = request.json["description"],
			author			= request.json["author"],
			launching		= request.json["launching"]
		)
	
		db.session.add(new_book)
		db.session.commit()

		return jsonify({"message": "The book is added"})
	
	else:
		return jsonify({"message": "The book isn\'t added"})


#Eliminar un libro
@app.route('/api/books/<int:book_id>', methods=["DELETE"])
def remove_book(book_id):

	if request.method == 'POST':
		book_found = Books.query.filter_by(id=book_id).first()

		db.session.delete(book_found)
		db.session.commit()

		return jsonify({"message":"Book deleted"})
	
	else:
		return jsonify({"message": "Book not found"})


#Actulizar o editar un libro
@app.route('/api/books/<int:book_id>', methods=["GET", "PUT"])
def update_book(book_id):

	if request.method == 'PUT':
		book_found = Books.query.filter_by(id=book_id).first()
	
		book_found.title       = request.json["title"]
		book_found.description = request.json["description"]
		book_found.author      = request.json["author"]
		book_found.launching   = request.json["launching"]

		db.session.add(book_found)
		db.session.commit()

		return jsonify(
			{
				"title": book_found.title,
				"description": book_found.description,
				"author": book_found.author,
				"launching": book_found.launching
			}
		)
	
	else:
		return jsonify({"message": "Book not found"})


if __name__ == "__main__":
	db.create_all()
	app.run(debug=True, port=8080)
