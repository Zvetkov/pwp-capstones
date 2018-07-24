isbn_list = []

class User(object):
    """
    User class.
    Expects user name and email as arguments.
    """
    def __init__(self, name, email):     
        self.name = name
        self.books = {}
        self.email = email
        
    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{user} email has been updated".format(user=self.name))

    def __repr__(self):
        return "User {username}, email: {email}, books read: {books}".format(username=self.name, email=self.email, books=len(self.books))

    def __eq__(self, other_user):
        if other_user == None:
            return self.name == None and self.email == None
        else:
            return self.name==other_user.name and self.email==other_user.email
    
    def read_book(self, book, rating=None):
        self.books[book]=rating
    
    #calculates average ratings user given to read books
    #if no books was rated - returns 0    
    def get_average_rating(self):
        num_ratings = 0
        rating_sum = 0
        for book in self.books:
            if self.books[book]!=None:
                num_ratings += 1
                rating_sum += self.books[book]
        if num_ratings==0:
            return 0
        else:
            return rating_sum/num_ratings
    
class Book:
    """
    Book class.
    Expects title of book and ISBN as arguments.
    """
    def __init__(self, title, isbn):

            self.title = title
            self.isbn = isbn
            isbn_list.append(isbn)
            self.ratings = []
        
    def __eq__(self, other_book):
        if other_book == None:
            return self.title == None and self.isbn == None
        else:
            return self.title == other_book.title and self.isbn == other_book.isbn
    
    def __hash__(self):
        return hash((self.title, self.isbn))
    
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self, new_isbn):
        self.isbn = new_isbn
        print("{title} ISBN has been updated".format(title=self.title))
        
    def add_rating(self, rating):
        if rating in range(0,5):
            self.ratings.append(rating)
        else:
            print("Invalid rating")
            
    def get_average_rating(self):
        return sum(self.ratings)/len(self.ratings)
        
class Fiction(Book):
    def __init__(self, title, isbn, author):
        super().__init__(title, isbn)
        self.author = author
    
    def get_author(self):
        return self.author
    
    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)
    
class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level
    
    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level
    
    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)

class TomeRater:
    def __init__(self):
        self.users = {}
        self.books = {}
    
    #Returns new book object with title and isbn passed as arguments
    #Checks if ISBN is unique using list of ISBNs for all books created    
    def create_book(self, title, isbn):
        if isbn in isbn_list:
            print("This ISBN is not unique.")
        else:
            return Book(title, isbn)
    
    #Same as above for fiction book object
    def create_novel(self, title, author, isbn):
        if isbn in isbn_list:
            print("This ISBN is not unique.")
        else:
            return Fiction(title, isbn, author)
    
    #Same as above for non-fiction book object
    def create_non_fiction(self, title, subject, level, isbn):
        if isbn in isbn_list:
            print("This ISBN is not unique.")
        else:
            return Non_Fiction(title, subject, level, isbn)
    
    #Adds book to user in users list of TomeRater object
    #Checks that user exist in users list. If not - prints message
    def add_book_to_user(self, book, email, rating=None):
        if self.users.get(email) == None:
            print("No user with email {email}!".format(email=email))
        else:
            self.users.get(email).read_book(book, rating)
            book.add_rating(rating)
            if book in self.books:
                self.books[book]+=1
            else:
                self.books[book]=1
                
    #Adds user to users list of TomeRater object.
    #Checks that email is valid(uses specified domain and contains @)        
    def add_user(self, name, email, user_books=None):
        if "@" in email and (".com" in email or ".edu" in email or ".org" in email):
            if self.users.get(email) != None:
                print("This email is taken or user already exist")
            else:                
                self.users[email] = User(name, email)
                if user_books != None:
                    for book in user_books:
                        self.add_book_to_user(book, email)
        else:
            print("This email is invalid or domain used is not supported. Please use .com, .org or .edu domain emails.")
                
    def print_catalog(self):
        for book in self.books:
            print(book)
            
    def print_users(self):
        for user in self.users:
            print(user)
    
    #returns book that was read most times by all users        
    def get_most_read_book(self):
        most_read=None
        read_count=0
        for book in self.books:
            if self.books[book]>read_count:
                read_count = self.books[book]
                most_read = book
        return most_read
    
    #returns book with highest average rating
    def highest_rated_book(self):
        highest_rated = None
        max_book_rating = 0
        for book in self.books:
            if book.get_average_rating() > max_book_rating:
                max_book_rating = book.get_average_rating()
                highest_rated = book
        return highest_rated
    
    #returns user that gave highest average ratings
    def most_positive_user(self):
        most_positive = None
        max_user_rating = 0
        for email in self.users:
            if self.users[email].get_average_rating() > max_user_rating:
                max_user_rating = self.users[email].get_average_rating()
                most_positive = self.users[email]
        return most_positive
            
        