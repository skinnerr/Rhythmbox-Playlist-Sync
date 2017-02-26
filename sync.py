from xml.dom import minidom
import os.path
import urllib
import itertools


def parse_rbox_playlists(rbox_playlist_path, playlists_to_sync):
    """
    Parses the RhythmBox playlists.xml file.
    Input
        rbox_playlist_path: path to xml file
        playlists_to_sync:  list of strings with playlist names
    """

    # Parameters to return
    n_files = 0
    n_files_found = 0
    all_file_names = list()

    xmldoc = minidom.parse(rbox_playlist_path)
    allplaylists = xmldoc.getElementsByTagName('rhythmdb-playlists')[0]
    playlists = allplaylists.getElementsByTagName('playlist')
    for pl in playlists:
        plname = pl.getAttribute('name')
        if plname in playlists_to_sync:
            fnames = list()
            print 'Playlist:', plname
            targets = pl.getElementsByTagName('location')
            for target in targets:
                target = target.firstChild.data
                target = urllib.unquote(target.encode('utf-8'))
                fpath = target[7:]
                n_files += 1
                if not os.path.exists(fpath):
                    print 'File not found:', fpath
                    continue
                n_files_found += 1
                fname = fpath.split('/')[-1]
                fnames.append(fname)
            all_file_names.append(fnames)
    return all_file_names


def sync(directory_path, playlist_names, file_names):

    uniq_file_names = list(set(itertools.chain(*file_names)))
    print uniq_file_names
    print len(uniq_file_names)

    sync_files(directory_path, uniq_file_names)

    sync_playlists(directory_path, playlist_names, file_names)

####################################################################
####################################################################
####################################################################

playlists = ['Nature Sounds']
rb_path = 'playlists.xml'
nested_song_list = parse_rbox_playlists(rb_path, playlists)

sync_path = 'music/'
sync(sync_path, playlists, nested_song_list)
