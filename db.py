import mysql.connector
import os

mydb = mysql.connector.connect(  # used to connect to DB
    host='localhost',
    user='root',
    passwd='',
    database='songstorage'
)

mycursor = mydb.cursor()


def get_id(filename):
    """Function used to get the ID of a given filename"""\

    query = f'select id from songs where filename = "{filename}"'
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    if not myresult:
        return 0
    return myresult
    pass


def get_filename(id):
    """Function used to get the filename of a given ID"""
    query = f'select filename from songs where id = {id}'
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    if not myresult:
        return 0
    return myresult
    pass


def add(filename, artist, song, date, tags, format):
    """Function used to add a song in the DB"""

    if get_id(filename) is not 0:
        print("Filename already exists in DB")
    else:
        query = f'INSERT INTO songs (filename, artist, song, date, tags, format) VALUES ("{filename}", "{artist}", "{song}", "{date}", "{tags}", "{format}");'
        mycursor.execute(query)
        mydb.commit()
        print('File added in DB and Storage')

    pass


def remove(song_id):
    """Function used to remove a song from the DB given the song ID"""

    filename = get_filename(song_id)
    if filename is not 0:
        query = f'delete from songs where id = {song_id}'
        mycursor.execute(query)
        mydb.commit()
        print('File removed from DB')
        if os.path.exists('Storage/' + filename[0][0]):
            os.remove('Storage/' + filename[0][0])
            print('File removed from Storage')
        else:
            print("The file does not exist")
    else:
        print("The file does not exist")

    pass


def query_db(**criteria):
    """Function used to query the DB given keyword args"""

    query_criteria = {}
    for i in criteria:
        if criteria[i] is not None:
            query_criteria[i] = criteria[i]

    where_statement = []
    for k, v in query_criteria.items():
        where_statement.append(k + '=' + '"' + v + '"')

    where_statement = 'where ' + ' and '.join(where_statement)

    query = f'select * from songs {where_statement}'
    # print(query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    if not myresult:
        return 'No data found'
    return myresult


def update_row(id, **criteria):
    """Function used to update a row in the DB given an ID and keyword args"""

    if query_db(id=id) is not 0:  # if exists updatable row
        set_values = ''
        for i in criteria:
            if criteria[i] is not None:
                set_values += i + ' = ' + '"' + criteria[i] + '"' + ', '

        set_values = set_values[:-2]
        query = f"UPDATE songs SET {set_values} WHERE id = {id};"
        # print(query)
        mycursor.execute(query)
        mydb.commit()
        print(f'Row with id = {id} updated successfully')
    else:
        print('ID not found.')
        return 0
    pass

# update_row()
