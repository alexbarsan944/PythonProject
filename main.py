def add_song(song_name_path, artist, song, date, tags):  # returns id of the song
    from shutil import copy
    import db

    dst = 'Storage'
    try:
        copy(song_name_path, dst)
    except:
        print("File already exists in Storage")

    filename = song_name_path.split('/')[1]
    db.add(filename, artist, song, date, tags)

    pass


# add_song("songs/11 Anne.flac", 'Santigold', "Anne", "2008-04-29", 'indie rock')


def remove_song(song_id):
    import db
    db.remove(2)
    pass


remove_song(1)


def modificare_metadate(song_id):
    pass


def create_savelist(output_path):
    pass


def search(**criteria):
    import db

    artist = None
    song_name = None
    date = None
    tags = None
    format = None

    for i in criteria.keys():
        if i.lower() == 'artist':
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

    db.query_db(artist=artist, song_name=song_name, date=date, tags=tags, format=format)
    pass


# search(artist='santigold', date='2012-04-24', format='flac')


def play(song_name):
    pass
