import mysql.connector
import database_infos

def connect_to_database():
    """Establishes connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host = database_infos.host,
            user = database_infos.user,
            password = database_infos.password,
            database = database_infos.database
        )
        return connection
    except mysql.connector.Error as err:
        print(f'Error: {err}')
        return None

def add_book(cursor):
    """Adds a new book to the library"""
    title = input('Enter Book Name: ').strip()
    author_name = input('Enter Author Name : ').strip()
    try:
        cursor.execute('''
            insert into books (book_name, author)
            values (%s, %s)
        ''', (title, author_name))
        cursor.execute('select LAST_INSERT_ID();')
        book_id = cursor.fetchone()[0]
        print(f'Book added successfully with ID: {book_id}')
    except mysql.connector.Error as err:
        print(f'Error: {err}')

def issue_book(cursor, connection):
    """Issues a book to a student."""
    student_name = input('Enter your name: ').strip()
    student_id = input('Enter your ID number: ').strip()
    book_title = input('Enter the Book name: ').strip()
    try:
        cursor.execute('''
        select book_id from books
        where book_name = %s and available = 'yes'
        ''', (book_title,))
        result = cursor.fetchone()
        if result:
            book_id = result[0]
            cursor.execute('''
            insert into issue_details(book_id, student_id, student_name)
            values (%s, %s, %s)
            ''', (book_id, student_id, student_name))
            cursor.execute('''
            update books 
            set available = 'no'
            where book_id = %s
            ''', (book_id, ))
            connection.commit()
            print(f'Book with ID: {book_id} has been issued to {student_name}.')
        else:
            print(f'Book: {book_title} is not available.')

    except mysql.connector.Error as err:
        print(f'Error: {err}')

def return_book(cursor, connection):
    """Returns a book to the library."""
    student_name = input('Enter your name: ').strip()
    book_title = input('Enter Book name to be returned: ').strip()
    try:
        cursor.execute('''
        select book_id from books
        where book_name = %s and available = 'no'
        ''', (book_title,))
        result = cursor.fetchone()
        if result:
            book_id = book[0]
            cursor.execute("""
                UPDATE books SET available = 'yes'
                WHERE book_id = %s
            """, (book_id,))
            cursor.execute("""
                DELETE FROM issue_details
                WHERE book_id = %s AND student_name = %s
            """, (book_id, student_name))
            connection.commit()
            print('The Book has been returned')
        else:
            print('Either the book is not issued or does not exist.')
    except mysql.connector.Error as err:
        print(f'Error: {err}')

def display_books(cursor):
    """Displays all books in the library."""
    try:
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        if books:
            for book in books:
                print(f'Book ID: {book[0]}, Name: {book[1]}, Author: {book[2]}, Available: {book[3]}')
        else:
            print('No Books in the library.')
    except con.Error as err:
        print(f"Error: {err}")

def delete_book(cursor, connection):
    """Removes a book from the library."""
    book_id = input('Enter Book ID you want to delete: ').strip()
    try:
        cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
        connection.commit()
        print('Book has been deleted successfully.')
    except con.Error as err:
        print(f"Error: {err}")


def search_book(cursor):
    """Searches for books by title."""
    book_title = input('Enter Book name: ').strip()
    try:
        cursor.execute("""
            SELECT * FROM books
            WHERE book_name LIKE %s
        """, (f"%{book_title}%",))
        books = cursor.fetchall()
        for book in books:
            print(f'Book ID: {book[0]}, Name: {book[1]}, Author: {book[2]}, Available: {book[3]}')
    except con.Error as err:
        print(f"Error: {err}")


def user_choice(cursor, connection):
    """Processes user input and calls respective functions."""
    while True:
        print(
            '\t1. Add book  2. Issue book  3. Return book  4. Display books  5. Delete book  6. Search a book  7. Exit')
        user_choice = input('Enter your choice: ').strip()
        if user_choice == '1':
            add_book(cursor)
        elif user_choice == '2':
            issue_book(cursor, connection)
        elif user_choice == '3':
            return_book(cursor, connection)
        elif user_choice == '4':
            display_books(cursor)
        elif user_choice == '5':
            delete_book(cursor, connection)
        elif user_choice == '6':
            search_book(cursor)
        elif user_choice == '7':
            print('The process ended successfully. Goodbye!')
            break
        else:
            print('Please choose from the options above.')


if __name__ == '__main__':
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor(buffered=True)

            # Creates a table in the selected database
            cursor.execute("""
                create table if not exists books(
                    book_id int auto_increment primary key,
                    book_name varchar(255),
                    author varchar(255),
                    available varchar(255) default 'yes'
                );
            """)

            cursor.execute("""
                create table if not exists issue_details(
                    book_id int not null,
                    student_id varchar(255),
                    student_name varchar(255) not null,
                    foreign key (book_id) references books(book_id)
                );
            """)


            print('Welcome to the Library Management System.')
            user_choice(cursor, connection)
        finally:
            cursor.close()
            connection.close()
    else:
        print('Failed to establish a connection to the database.')