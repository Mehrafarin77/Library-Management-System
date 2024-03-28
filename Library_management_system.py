import mysql.connector as con
import database_infos

# Now we make a connection to our database
connection = con.connect(
    host = database_infos.host,
    user = database_infos.user,
    password = database_infos.password,
    database = database_infos.database,
)

# To be able to write sql queries
cursor = connection.cursor(buffered=True)

# Creates a table in the selected database
# cursor.execute("""
#     create table books(
#         book_id int auto_increment primary key,
#         book_name varchar(255),
#         author varchar(255),
#         available varchar(255) default 'yes'
#     );
# """)

# cursor.execute("""
#     create table issue_details(
#         book_id int not null,
#         student_id int auto_increment primary key,
#         student_name varchar(255) not null,
#         foreign key (book_id) references books(book_id)
#     );
# """)

def add_book():
    """Adds a book which the user has entered its infos"""
    title = input('Enter Book name: ').strip()
    author_name = input('Enter Author name: ').strip()
    cursor.execute(f"""
        insert into books (book_name, author)
        values ('{title}', '{author_name}');
    """)
    recent_book_id = cursor.execute(f"""
    select book_id from books where book_name = '{title}' and author = '{author_name}';
    """)
    result = cursor.fetchone()
    print(f'Book added successfully with ID of: {result[0]}')


def issue_book():
    """Lends the book with the infos which user has entered"""
    student_name = input('Enter your name: ').strip()
    # student_id = input('Enter your user number: ').strip()
    book_title = input('Enter the Book name: ').strip()
    cursor.execute(f"""
        select book_id from books where book_name = '{book_title}' and available = 'yes';
    """)
    result = cursor.fetchone()
    if result is not None:
        book_id = result[0]
        cursor.execute(f"""
            insert into issue_details 
            values ('{book_id}', '{student_name}');
        """)
        cursor.execute(f"""
            update books set available = 'no' where book_id = '{book_id}';
        """)
        print(f'Book with ID: {book_id} has been issued to {student_name}.')
    else:
        print(f'Book: {book_title} is not Available.')

def return_book():
    """Return a book with user_entered infos which the user borrowed"""
    student_name = input('Enter your name: ').strip()
    student_id = input('Enter your student number: ').strip()
    book_name = input('Enter Book name to be returned: ').strip()
    cursor.execute(f"""
        select available from books where book_name = '{book_name}'; 
    """)
    books = cursor.fetchall()
    issued_book = False
    for book in books:
        if book[-1] == 'no':
            issued_book = True
    if issued_book:
        cursor.execute(f"""
            update books set available = 'yes' where book_name = '{book_name}'
        """)
    print('The Book has been returned')


def display_books():
    """Displays all books in the library"""
    cursor.execute("""
        select * from books
    """)
    books = cursor.fetchall()
    for book in books:
        print(f'Book ID: {book[0]}, Name: {book[1]}, Author: {book[2]}, Availbale: {book[-1]}')

def delete_book():
    """Remove a book from the library"""
    bookID = input('Enter Book ID you want to delete: ').strip()
    cursor.execute('select book_id from books')
    books_ids = cursor.fetchall()
    cursor.execute(f"""
        delete from books 
        where book_id = '{bookID}';
    """)
    print('Book has been deleted successfully.')

def find_book():
    book_title = input('Enter Book name: ').strip()
    cursor.execute(f"""
        select * from books 
        where book_name like '%{book_title}%';
    """)
    books = cursor.fetchall()
    for book in books:
        print(f'Book ID: {book[0]}, Name: {book[1]}, Author: {book[2]}, Availbale: {book[-1]}')


continue_with_the_app = True
def user_choosing_process():
    """User can make choice and a functionality will get selected respectively"""
    global continue_with_the_app
    print('\t1. Add book  2. Issue book  3. Return book  4. Display books  5. Delete book  6. Search a book  7.Exit')
    user_choice = input('Enter your choice: ')
    if user_choice == '1':
        add_book()
    elif user_choice == '2':
        issue_book()
    elif user_choice == '3':
        return_book()
    elif user_choice == '4':
        display_books()
    elif user_choice == '5':
        delete_book()
    elif user_choice == '6':
        find_book()
    elif user_choice == '7':
        print('The process ended successfully. Goodbye!')
        continue_with_the_app = False
    else:
        print('Please choose from the list above.')
        print('\t1. Add book  2. Issue book  3. Return book  4. Display books  5. Delete book  6. Exit')
        user_choice = input('Enter your choice: ')
    return continue_with_the_app


if __name__ == '__main__':
     username = input('Enter your username: ').strip()
     password = input('Enter your password: ').strip()
     if username == 'root' and password == 'mehrafarin81':
         print('Welcome to Mehrafarin\'s Library management system :)')
         while continue_with_the_app:
             user_choosing_process()
     else:
         print('You are not a user.')


connection.commit()
cursor.close()