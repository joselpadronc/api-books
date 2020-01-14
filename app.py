from flask import Flask, jsonify, request
from books import Books

app = Flask(__name__)

books_saved = Books

@app.route('/')
def index():
	return jsonify({"ping": "pong"})


@app.route('/api/books', methods=["GET"])
def  get_books():
	return jsonify({"message": "Lista de Libros guardados"}, {"books": books_saved})


@app.route('/api/books/', methods=["GET", "POST"])
def add_book():
	book_data = {
		"title": request.json['title'],
		"description": request.json['description'],
		"author": request.json['author'],
		"launching": request.json["launching"]
	}
	books_saved.append(book_data)

	return jsonify({"message": "Lista de Libros guardados"}, {"books": books_saved})

if __name__ == "__main__":
	app.run(debug=True, port=8080)