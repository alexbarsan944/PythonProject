import mysql.connector
import os

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='songstorage'
)

mycursor = mydb.cursor()


def get_id(filename):
    query = f'select id from songs where filename = "{filename}"'
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    if not myresult:
        return 0
    return myresult
    pass


def get_filename(id):
    query = f'select filename from songs where id = {id}'
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    if not myresult:
        return 0
    return myresult
    pass


def add(filename, artist, song, date, tags):
    if get_id(filename) is not 0:
        print("filename already exists in DB")
    else:
        query = f'INSERT INTO songs (filename, artist, song, date, tags) VALUES ("{filename}", "{artist}", "{song}", "{date}", "{tags}");'
        mycursor.execute(query)
        mydb.commit()
        print('File added in DB')
    pass


def remove(song_id):
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
    query_criteria = {}
    format_exists = False
    query_format = None
    for i in criteria:
        if criteria[i] is not None and i is not 'format':
            query_criteria[i] = criteria[i]
        elif criteria[i] is not None and i is 'format':
            format_exists = True
            query_format = f'AND FileName LIKE "%.{criteria[i]}"'

    where_statement = []
    for k, v in query_criteria.items():
        where_statement.append(k + '=' + '"' + v + '"')

    if format_exists and len(query_criteria) == 1:
        where_statement = 'where 1=1' + ' and '.join(where_statement)
    else:
        where_statement = 'where ' + ' and '.join(where_statement)

    if format_exists:
        where_statement += query_format

    query = f'select * from songs {where_statement}'
    # print(query)
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    if not myresult:
        return 'No data found'
    return myresult


def update_row(id, **criteria):
    if query_db(id=id) is not 0:  # if exists updatable row
        set_values = ''
        for i in criteria:
            if criteria[i] is not None:
                set_values += i + ' = ' + '"' + criteria[i] + '"' + ', '

        set_values = set_values[:-2]
        query = f"UPDATE songs SET {set_values} WHERE id = id;"
        mycursor.execute(query)
        mydb.commit()
        print(f'Row with id = {id} updated successfully')
    else:
        print('ID not found.')
        return 0
    pass

# update_row()
