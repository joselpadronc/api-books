from flask import Flask, jsonify, request
from books import Books
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{root}:{jose1766}@localhost:8080/{api_books}'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

books_saved = Books

@app.route('/')
def index():
	return jsonify({"ping": "pong"})

	
#Obtener la lista de libros
@app.route('/api/books', methods=["GET"])
def  get_books():
	return jsonify({"message": "Lista de Libros guardados"}, {"books": books_saved})


#Buscar libro
@app.route('/api/books/<int:book_id>', methods=["GET"])
def search_book(book_id):
	book_found = [book for book in books_saved if book["id"] == book_id]
	
	if len(book_found) > 0:
		return jsonify({"message": "Este es el libro que buscas"}, book_found)

	else:
		return jsonify({"message": "The book not found"})



#Publicar nuevo libro
@app.route('/api/books/', methods=["GET", "POST"])
def add_book():
	book_data = {
		"id": request.json['id'],
		"title": request.json['title'],
		"description": request.json['description'],
		"author": request.json['author'],
		"launching": request.json["launching"]
	}
	books_saved.append(book_data)

	return jsonify({"message": "Lista de Libros guardados"}, {"books": books_saved})


#Eliminar un libro
@app.route('/api/books/<int:book_id>', methods=["GET", "DELETE"])
def remove_book(book_id):
	book_found = [book for book in books_saved if book["id"] == book_id]
	
	if len(book_found) > 0:
		books_saved.remove(book_found[0])
		return jsonify({"message": "The book is deleted"}, books_saved)

	else:
		return jsonify({"message": "The book not found"})


#Actulizar o editar un libro
@app.route('/api/books/<int:book_id>', methods=["GET", "PUT"])
def update_book(book_id):
	book_found = [book for book in books_saved if book["id"] == book_id]
	
	if len(book_found) > 0:
		book_found[0]['title'] = request.json['title']
		book_found[0]['description'] = request.json['description']
		book_found[0]['author'] = request.json['author']
		book_found[0]['launching'] = request.json['launching']

		return jsonify({"message": "The book is updated"}, books_saved)

	else:
		return jsonify({"message": "The book not found"})



if __name__ == "__main__":
	app.run(debug=True, port=8080)