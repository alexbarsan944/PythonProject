import db
from shutil import copy


def add_song(song_name_path, artist, song, date, tags):  # returns id of the song

    dst = 'Storage'
    try:
        copy(song_name_path, dst)
        filename = song_name_path.split('/')[1]
        db.add(filename, artist, song, date, tags)
        print('File added in Storage')
    except:
        print("File already exists in Storage")

    pass


# add_song("songs/02 Disparate Youth.flac", 'Santigold', "Disparate youth", "2008-04-29", 'indie rock')


def remove_song(song_id):
    db.remove(song_id)
    pass


# remove_song(14)


def modificare_metadate(song_id, **criteria):
    db.update_row(song_id, **criteria)
    pass


# modificare_metadate('15', tags='indie', song='anne')


def create_savelist(output_path, **criteria):
    from zipfile import ZipFile

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

    return db.query_db(id=id, artist=artist, song_name=song_name, date=date, tags=tags, format=format)
    pass


print(search(id='16'))


def play(song_name):
    import miniaudio
    stream = miniaudio.stream_file(song_name)
    with miniaudio.PlaybackDevice() as device:
        device.start(stream)
        input("Audio file playing in the background. Enter to stop playback: ")

    pass

# play('Storage/02 Disparate Youth.flac')
