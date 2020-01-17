from flask import Flask, jsonify, request
from books import Books
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{root}:{jose1766}@localhost:8080/{api_books}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Book(db.Model):

	#Establece el nombre de la tabla
	__tablename__ = 'books'
	__table_args__ = {'extend_existing': True}
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(80), nullable=False)
	description = db.Column(db.Text, nullable=False)
	author = db.Column(db.String(150), nullable=False)
	launching = db.Column(db.String(150), nullable=False)


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
	title = request.json['title']
	description = request.json['title']
	author = request.json['author']
	launching = request.json['launching']

	if request.method == 'POST':
		new_book = Book(
			title=title,
			description=description,
			author=author,
			launching=launching
		)

		return jsonify({"message": "The book is added"})

	else:
		return jsonify({"message": "The book can't added"})


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