from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    db = 'books_schema'
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.udpated_at = data['udpated_at']
        self.authors_who_favorited = []
        #this is a list of authors who favorited the book
    
#Get ALL Method (Read ALL)
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books;"
        books = []
        results = connectToMySQL(cls.db).query_db(query)
        for row in results:
            books.append(cls(row))
        return books

#Get ONE Method (Read ONE)
    @classmethod
    def get_one(cls,data):
        pass

#Create/Save method
    @classmethod
    def save(cls,data):
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"
        return connectToMySQL(cls.db).query_db(query, data)


#update method
    @classmethod
    def udpate(cls,data):
        pass


#deletemethod
    @classmethod
    def delete(cls,data):
        pass


#class method to grab all the books, add the favorites books, 
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        book = cls(results[0])
    
        for row in results:
        #instance where there are no fav id's and no favorited authors
            if row['authors.id'] == None:
                break
            data = {
                'id' : row['authors.id'],
                'name' : row['name'],
                'created_at' : row['authors.created_at'],
                'udpated_at' : row['authors.udpated_at']
            }
            book.authors_who_favorited.append(author.Author(data))
        return book


#opposite of what was written in authors

    @classmethod
    def unfavorited_books(cls, data):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        books = []
        for row in results:
            books.append(cls(row))
        print(books)
        return books