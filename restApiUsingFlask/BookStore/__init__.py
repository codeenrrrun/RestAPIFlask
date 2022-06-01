import markdown
import os
import shelve
from flask import Flask, g
from flask_restful import Resource, Api, reqparse
import requests

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

def get_author_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("author.db")
    return db
def get_books_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("books.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '\\readme.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class AuthorList(Resource):
    def get(self):
        shelf = get_author_db()
        keys = list(shelf.keys())

        authors = []

        for key in keys:
            authors.append(shelf[key])

        return {'message': 'Success', 'data': authors}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('author_id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('phone_number', required=True)
        parser.add_argument('birth_date', required=True)
        parser.add_argument('death_date')


        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_author_db()
        shelf[args['author_id']] = args

        return {'message': 'Author registered', 'data': args}, 201


class Books(Resource):
    def get(self):
        shelf = get_books_db()
        keys = list(shelf.keys())

        books = []
        for key in keys:
            books.append(shelf[key])

        return {'message': 'Success', 'data': books}, 200
    
    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('book_id', required=True)
        parser.add_argument('title', required=True)
        parser.add_argument('author_id', required=True)
        parser.add_argument('publisher', required=True)
        parser.add_argument('publish_date', required=True)
        parser.add_argument('category_id', required=True)
        parser.add_argument('price', required=True)
        parser.add_argument('sold_count', required=True)



        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_books_db()
        shelf[args['book_id']] = args

        return {'message': 'Book registered', 'data': args}, 201



class BookOperation(Resource):
    def get(self, book_id):
            shelf = get_books_db()

            # If the key does not exist in the data store, return a 404 error.
            print("entered")
            if not (book_id in shelf):
                return {'message': 'Book not found', 'data': {}}, 404

            return {'message': 'Book found', 'data': shelf[book_id]}, 200
    def delete(self, book_id):
        shelf = get_books_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (book_id in shelf):
            return {'message': 'Book not found', 'data': {}}, 404

        del shelf[book_id]
        return '', 204

class AuthorOperation(Resource):
    def get(self, author_id):
            shelf = get_books_db()

            data = []
            for object in list(shelf.values()):
                if object['author_id']==author_id:
                    data.append(object)
            if len(data)==0:
                return {'message': 'Author not found', 'data': {}}, 404

            return {'message': 'Author  found', 'data': data}, 200
    def delete(self, author_id):
        shelf = get_books_db()
        data = []
        for object in list(shelf.values()):
            if object['author_id']==author_id:
                data.append(object['book_id'])
        if len(data)==0:
            return {'message': 'Author not found', 'data': {}}, 404
        for bookId in data:
            del shelf[bookId]
        return '', 204

@app.route("/getAllAuthors")
def getAllAuthors():
    shelf = get_author_db()
    data = []
    for object in list(shelf.values()):
        data.append(object['name'])
    return  {'message': str(len(data))+' Authors  found', 'data': data}, 200

@app.route("/getAllCategories")
def getAllCategories():
    shelf = get_books_db()
    data = []
    for object in list(shelf.values()):
        data.append(object['category_id'])
    return  {'message': str(len(set(data)))+' Categories  found', 'data': list(set(data))}, 200

@app.route("/getMostBooksSoldByAuthor/<string:author_id>")
def getMostBooksSoldByAuthor(author_id):
    shelf = get_books_db()
    maxSoFar = -float("inf")
    bookName = "Not Found"
    for object in list(shelf.values()):
        if object['author_id']==author_id:
            if maxSoFar<int(object['sold_count']):
                maxSoFar = int(object['sold_count'])
                bookName = object['title']
    return  {'message': 'Most Sold Book Detail of given author.', 'data': {"Book Name :":bookName,"Sold Count:":maxSoFar}}, 200

@app.route("/getMostBooksSoldByCategoryId/<string:category_id>")
def getMostBooksSoldByCategory(category_id):
    shelf = get_books_db()
    maxSoFar = -float("inf")
    bookName = "Not Found"
    for object in list(shelf.values()):
        if object['category_id']==category_id:
            if maxSoFar<int(object['sold_count']):
                maxSoFar = int(object['sold_count'])
                bookName = object['title']
    return  {'message': 'Most Sold Book Detail of given category_id.', 'data': {"Book Name :":bookName,"Sold Count:":maxSoFar}}, 200

@app.route("/searchBookByTitle/<string:title>")
def searchBookByTitle(title):
    shelf = get_books_db()
    data = []
    for object in list(shelf.values()):
        if title in object['title']:
            data.append(object)
    return  {'message': 'Book Detail of given partial title', 'data': data}, 200

@app.route("/searchBookByAuthor/<string:author_name>")
def searchBookByAuthor(author_name):
    shelf = get_books_db()
    Final_data = []
    r = requests.get(url = 'http://127.0.0.1//authors')
    data = r.json()
    for authorObj in data["data"]:
        if author_name in authorObj["name"]:
            for bookObj in list(shelf.values()):
                if bookObj['author_id']==authorObj['author_id']:
                    Final_data.append(bookObj|{"Author Name: ":authorObj['name']})
    return  {'message': 'Book Detail of given partial Author Name', 'data': Final_data}, 200

@app.route("/searchBookByAuthor/<string:author_name>/<string:title>")
def searchBookByAuthorAndTitle(author_name,title):
    shelf = get_books_db()
    Final_data = []
    r = requests.get(url = 'http://127.0.0.1//authors')
    data = r.json()
    for authorObj in data["data"]:
        if author_name in authorObj["name"]:
            for bookObj in list(shelf.values()):
                if bookObj['author_id']==authorObj['author_id'] and title in bookObj['title']:
                    Final_data.append(bookObj|{"Author Name: ":authorObj['name']})
    return  {'message': 'Book Detail of given partial Author Name and partial Title Name', 'data': Final_data}, 200


api.add_resource(AuthorList, '/authors')
api.add_resource(Books, '/books')
api.add_resource(BookOperation, '/bookWithId/<string:book_id>')
api.add_resource(AuthorOperation, '/bookWithAuthorId/<string:author_id>')

