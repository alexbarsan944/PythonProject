import re
from shutil import copy

import db


def add_song(song_name_path, artist, song, date, tags, format):  # returns id of the song

    dst = 'Storage'
    try:
        copy(song_name_path, dst)
        filename = song_name_path.split('/')[1]
        db.add(filename, artist, song, date, tags, format)
    except:
        print("File already exists in Storage")

    pass


# add_song("songs/05 Creator.flac", 'Santigold', "Creator", "2008-04-29", 'rock', 'flac')


def remove_song(song_id):
    db.remove(song_id)
    pass


# remove_song(17)


def modificare_metadate(song_id, **criteria):
    db.update_row(song_id, **criteria)
    pass


# modificare_metadate('15', tags='indie', song='Anne')


def create_savelist(output_path, **criteria):
    from zipfile import ZipFile

    if not output_path.endswith('.zip'):
        print('output_path not zip')
        exit(0)

    query_result = db.query_db(**criteria)
    if query_result == 0:
        print('No data found')
    else:
        files = []
        for row in query_result:
            files.append(row[1])

        zipObj = ZipFile(output_path, 'w')

        for f in files:
            print(f)
            zipObj.write('Storage/' + f)

        zipObj.close()
        print('Files added succesfully')
    pass


# create_savelist('playlist.zip', format='flac')


def search(**criteria):
    import db

    artist = None
    song_name = None
    date = None
    tags = None
    format = None
    id = None

    for i in criteria.keys():
        if i.lower() == 'id':
            id = criteria[i]
        elif i.lower() == 'artist':
            artist = criteria[i]
        elif i.lower() == 'song_name':
            song_name = criteria[i]
        elif i.lower() == 'date':
            date = criteria[i]
        elif i.lower() == 'tags':
            tags = criteria[i]
        elif i.lower() == 'format':
            format = criteria[i]
        else:
            print('`', i, '`', 'is an invalid argument.')
            exit(0)

    ret_value = db.query_db(id=id, artist=artist, song_name=song_name, date=date, tags=tags, format=format)
    for row in ret_value:
        print(row)
    return ret_value
    pass


# search(id='16')


def play(song_name):
    import miniaudio
    stream = miniaudio.stream_file('Storage/' + song_name)
    with miniaudio.PlaybackDevice() as device:
        device.start(stream)
        input("Audio file playing in the background. Enter to stop playback: ")

    pass


# play('02 Disparate Youth.flac')


while True:
    input_command = input('Enter command. (H for help): ')

    if input_command.lower() == 'h':
        print('Examples: ')
        print("play 02 Disparate Youth.flac ")
        print("search id=16, format=flac ")
        print("create_savelist - path, **criteria")
        print("modificare_metadate('15', tags='indie', song='Anne')")
        print("add_song - songs/07 The Riot's Gone.flac, santigold, riot's gone, 2008, indie, flac ")

        pass

    if input_command.lower() == 'play':
        song_name = input("Enter song name: ")
        play(song_name)
    elif input_command.lower() == 'search':
        t = input('Enter parameters: id, artist, song_name, date, tags, format: ').strip(' ')
        t = re.split('[=,]', "".join(t.split()))
        t = {t[i]: t[i + 1] for i in range(0, len(t), 2)}
        search(**t)
    elif input_command.lower() == 'create_savelist':  # Done
        p = input('Enter path: ')
        t = input('Enter parameters: id, artist, song_name, date, tags, format: ')
        t = re.split(', |=', t)
        t = {t[i]: t[i + 1] for i in range(0, len(t), 2)}
        create_savelist(p, **t)
    elif input_command.lower() == 'modificare_metadate':
        p = input('Enter id: ')
        t = input('Enter parameters: id, artist, song_name, date, tags, format: ')
        t = re.split(', |=', t)
        t = {t[i]: t[i + 1] for i in range(0, len(t), 2)}
        modificare_metadate(p, **t)
    elif input_command.lower() == 'add_song':
        t = input('Enter parameters: path, artist, title, year, tags, format: ')
        t = re.split(', |=', t)
        add_song(t[0], t[1], t[2], t[3], t[4], t[5])
    elif input_command.lower() == 'remove':
        t = input('ID to remove: ')
        remove_song(t)
    else:
        print('Invalid command. Try again. ')
