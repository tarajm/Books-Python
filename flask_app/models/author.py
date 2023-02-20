from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    db = 'books_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []

    

#Get All Method (READ ALL)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        authors = []
        results = connectToMySQL(cls.db).query_db(query)
        for row in results:
            authors.append(cls(row))
        return authors


#Get One Method (READ One)
    @classmethod
    def get_one(cls, data):
        pass

#Create Method/SAVE method
    @classmethod
    def save(cls, data):
        query = "INSERT INTO authors (name) VALUES (%(name)s);"
        return connectToMySQL(cls.db).query_db(query, data)


#Update Method
    @classmethod
    def update(cls, data):
        pass

#Delete Method
    @classmethod
    def delete(cls, data):
        pass

#Unfavorited authors method - referenced in the books.py file (route)
#look up an author and see if that author is NOT in the list of favorites by book ID
#this filters out id's that don't match up or dont' have favorites
#returns a list of authors that are NOT favorited onto the book
    @classmethod
    def unfavorited_authors(cls, data):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s);"
        authors = []
        results = connectToMySQL(cls.db).query_db(query, data)
        for row in results:
            authors.append(cls(row))
        return authors
    
    @classmethod
    def add_favorites(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)
        

#class method to get all the favorited stuff
#reverse SQL query

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        #create instance of author on one row
        author = cls(results[0])

        for row in results:
            if row['books.id'] == None:
                break

            data = {
                "id" : row['books.id'],
                "title" : row['title'],
                "num_of_pages" : row['num_of_pages'],
                "created_at": row['books.created_at'],
                "updated_at": row['books.updated_at']
            }
            author.favorite_books.append(book.Book(data))
        return author
    
    
    