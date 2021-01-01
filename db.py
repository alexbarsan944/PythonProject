import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='songstorage'
)

mycursor = mydb.cursor()


def add(filename, artist, song, date, tags):
    query = f'INSERT INTO songs VALUES ("{filename}", "{artist}", "{song}", "{date}", "{tags}");'
    mycursor.execute(query)
    mydb.commit()
    pass

def remove(song_id):
    query = f'delete from songs where id = {song_id}'
    mycursor.execute(query)
    mydb.commit()
    pass

def query_db(**criteria):
    query_criteria = {}
    format_exists = False
    query_format = None
    for i in criteria:
        if criteria[i] is not None and i is not 'format':
            query_criteria[i] = criteria[i]
        if i is 'format':
            format_exists = True
            query_format = f'AND FileName LIKE "%.{criteria[i]}"'

    where_statement = []
    for k, v in query_criteria.items():
        where_statement.append(k + '=' + '"' + v + '"')

    where_statement = ' and '.join(where_statement)
    if format_exists:
        where_statement += query_format

    query = f'select * from songs where {where_statement}'
    mycursor.execute(query)
    myresult = mycursor.fetchall()

    if not myresult:
        print('No data')
    for row in myresult:
        print(row)
