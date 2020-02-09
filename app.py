import os
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from json_serializable import JSONSerializable
from books import Books

dbdir = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/db_books.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbdir
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
JSONSerializable(app)

with app.app_context():
	db.init_app(app)
	db.create_all()


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
	
	
	def save(self):
		db.session.add(self)
		db.session.commit()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()

		
@app.route('/')
def index():
	return jsonify({"ping": "pong"})

	
#Obtener la lista de libros
@app.route('/api/books', methods=["GET"])
def  get_books():
	try:
		return jsonify(ok=True, items=Books.query.all())
        except Exception as e:
		return abort(500, e)


#Buscar libro
@app.route('/api/books/id/<int:book_id>', methods=["GET"])
def search_book(book_id):
	try:
		return jsonify(ok=True, item=Books.query.filter_by(id=book_id).first())
	except Exception as e:
		return abort(404, e)


#Publicar nuevo libro
@app.route('/api/books', methods=["POST"])
def add_book():
	try:
		new_book = Books(
			title			= request.json["title"],
			description 		= request.json["description"],
			author			= request.json["author"],
			launching		= request.json["launching"]
		)
	
		new_book.save()

		return jsonify({"message": "The book is added"})
	exect Exception as e:
		return abort(400, e)

	
#Actulizar o editar un libro
@app.route('/api/books/<int:book_id>', methods=["PUT"])
def update_book(book_id):
	try:
		book_found = Books.query.filter_by(id=book_id).first()
	
		book_found.title       = request.json["title"]
		book_found.description = request.json["description"]
		book_found.author      = request.json["author"]
		book_found.launching   = request.json["launching"]

		book_found.save()

		return jsonify(book_found)
	except Exception as e:
		return abort(404, e)

	
#Eliminar un libro
@app.route('/api/books/<int:book_id>', methods=["DELETE"])
def remove_book(book_id):
	try:
		book_found = Books.query.filter_by(id=book_id).first()
		
		book_found.delete()

		return jsonify({"message":"Book deleted"})
	except Exception as e:
		return abort(404, e)


if __name__ == "__main__":
	app.run(debug=True, port=8080)
