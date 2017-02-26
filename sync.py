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
    all_file_paths = list()
    ordered_playlist_names = list() # Order of playlists in xml file not same as playlists_to_sync

    xmldoc = minidom.parse(rbox_playlist_path)
    allplaylists = xmldoc.getElementsByTagName('rhythmdb-playlists')[0]
    playlists = allplaylists.getElementsByTagName('playlist')
    for pl in playlists:
        plname = pl.getAttribute('name')
        if plname in playlists_to_sync:
            ordered_playlist_names.append(plname)
            fpaths = list()
            targets = pl.getElementsByTagName('location')
            for target in targets:
                target = target.firstChild.data
                target = urllib.unquote(target.encode('utf-8'))
                fpath = target[7:]
                if not os.path.exists(fpath):
                    print 'File not found:', fpath
                    continue
                fpaths.append(fpath)
            all_file_paths.append(fpaths)

    return [ordered_playlist_names, all_file_paths]


def sync_files(dest, file_paths_to_sync):
    print 'Syncing files...'
    nsynced = 0
    files_on_device = os.listdir(dest)
    for src in file_paths_to_sync:
        fname = src.split('/')[-1]
        if fname not in files_on_device:
            try:
                shutil.copy(src, dest)
                nsynced += 1
            except IOError as e:
                print 'Unable to copy to device:', src
                print '    ', e.message

    return nsynced


def sync_playlists(dest, playlists, file_paths):
    for playlist_name, files in zip(playlists, file_paths):
        pl_fn = '%s/%s.m3u' % (dest, playlist_name)
        print 'Writing playlist', pl_fn
        pl_file = open(pl_fn, 'w')
        for file in files:
            fname = file.split('/')[-1]
            pl_file.write('%s\n' % fname)
        pl_file.close()

    return


def sync(directory_path, playlist_names, file_paths):

    # Enumerate local files to sync
    uniq_file_paths = list(set(itertools.chain(*file_paths))) #TODO: maybe not necessary to list()
    print 'Unique file paths to sync:', len(uniq_file_paths)

    # Copy files to device
    nsynced = sync_files(directory_path, uniq_file_paths)
    print 'Number of files synced:', nsynced

    # Write playlist files on device
    sync_playlists(directory_path, playlist_names, file_paths)

####################################################################
####################################################################
####################################################################

playlists = ['Nature Sounds']
rb_path = 'playlists.xml'
sync_path = 'music'
[playlists, nested_song_path_list] = parse_rbox_playlists(rb_path, playlists)

sync(sync_path, playlists, nested_song_path_list)
