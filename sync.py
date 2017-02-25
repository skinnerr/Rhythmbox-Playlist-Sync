from xml.dom import minidom
import os.path
import urllib

toSync = ['Bump It', 'Bon Iver']

xmldoc = minidom.parse("playlists.xml")

allplaylists = xmldoc.getElementsByTagName("rhythmdb-playlists")[0]

playlists = allplaylists.getElementsByTagName("playlist")

c = 0
for playlist in playlists:
    name = playlist.getAttribute("name")
    if name in toSync:
        print name
        filenames = playlist.getElementsByTagName("location")
        for filename in filenames:
            fn = filename.firstChild.data
            fn = urllib.unquote(fn.encode('utf-8'))
            fn = fn[7:]
            if not os.path.exists(fn):
                print 'NOPE:', fn
            else:
                print 'YEP: ', fn
                c += 1
print 'Files found:', c
