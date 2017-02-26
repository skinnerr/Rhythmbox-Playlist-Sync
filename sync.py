from xml.dom import minidom
import os.path
import urllib
import itertools
import shutil


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
    all_file_paths = list()

    xmldoc = minidom.parse(rbox_playlist_path)
    allplaylists = xmldoc.getElementsByTagName('rhythmdb-playlists')[0]
    playlists = allplaylists.getElementsByTagName('playlist')
    for pl in playlists:
        plname = pl.getAttribute('name')
        if plname in playlists_to_sync:
            fpaths = list()
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
                fpaths.append(fpath)
            all_file_paths.append(fpaths)
    return all_file_paths


def sync_files(dest, file_paths_to_sync):
    nsynced = 0
    files_on_device = os.listdir(dest)
    for src in file_paths_to_sync:
        fname = src.split('/')[-1]
        if fname not in files_on_device:
            print 'not on device:', fname
            try:
                shutil.copy(src, dest)
            except:
                print 'oops, exception'

    return


def sync(directory_path, playlist_names, file_paths):

    uniq_file_paths = list(set(itertools.chain(*file_paths))) #TODO: maybe not necessary to list()
    print 'Unique file paths to sync:', len(uniq_file_paths)

    sync_files(directory_path, uniq_file_paths)

    #sync_playlists(directory_path, playlist_names, file_paths)

####################################################################
####################################################################
####################################################################

playlists = ['Nature Sounds']
rb_path = 'playlists.xml'
sync_path = 'music/'
nested_song_path_list = parse_rbox_playlists(rb_path, playlists)

sync(sync_path, playlists, nested_song_path_list)
