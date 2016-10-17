from bs4 import BeautifulSoup

def ParseLibForArtists(inputXML, cleanup = False):
    
    """Takes a string path to an iTunes XML library, parses out a list of artists
    
    If optional field cleanup is True, the list will be scrubbed according to the
    following criteria:
    
    """
    
    libraryXML = BeautifulSoup(open(inputXML),"xml")
    artists = [] #list of tuples of (artist, genre)
    
    
    #As of 2016 the XML structure of the iTunes library looks like this for any given song:
    #<?xml version="1.0" encoding="UTF-8"?>
    #<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    #<plist version="1.0">
    #<dict>
    #    <key>Major Version</key><integer>1</integer>
    #    <key>Minor Version</key><integer>1</integer>
    #    <key>Date</key><date>2016-10-16T20:19:12Z</date>
    #    <key>Application Version</key><string>12.5.1.21</string>
    #    <key>Features</key><integer>5</integer>
    #    <key>Show Content Ratings</key><true/>
    #    <key>Music Folder</key><string>file://localhost/D:/MP3s/</string>
    #    <key>Library Persistent ID</key><string>EC9072DBF8C755ED</string>
    #    <key>Tracks</key>
    #    <dict>
    #        <key>5862</key>
    #        <dict>
    #            <key>Track ID</key><integer></integer>
    #            <key>Name</key><string></string>
    #            <key>Artist</key><string></string>
    #            [...]
    #e.g., each song has its own <dict> tag and child elements but there are nested tags of
    #the same name with no further identifying attributes
    
    topLevelDict = libraryXML.find("dict").children[11].children()
    for tag in topLevelDict.findall("dict"):
        currentArtistName = tag.find("key",string="Artist").next_siblings().string()
        currentGenreName = tag.find("key",string="Genre").next_siblings().string()
        if currentArtistName != None and currentArtistName != "":
                #narrow genre scope for PoC
                if "metal" in currentGenreName.lower(): 
                    artists.append((currentArtistName,currentGenreName))
                else:
                    artists.append((currentArtistName,""))
                
            
