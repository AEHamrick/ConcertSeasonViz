import csv
import re
import os
import os.path
import urllib
import time
from Classes import *
from Helper import FindGenreSpanningArtists
from bs4 import BeautifulSoup
import cPickle
#from bsddb.test.test_pickle import cPickle
def ParseLibForArtists(inputXML, cleanup = False, writeGenreReport = False):
    """Takes a string path to an iTunes XML library, parses out a list of artists
    
    If optional field writeGenreReport is true, a CSV report of artists with songs in 
    multiple genres will be written; see details in Helper.FindGenreSpanningArtists
    
    If optional field cleanup is True, the list will be scrubbed according to the
    following criteria:
    
    """
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
    U = Utility()
    
    libraryFile = open(inputXML).readlines()
    artists = list() #list of named tuples as defined in classes.py 
    seenArtists = list() #list of artist names in string form; use for uniqueness
    tagRegex = "<string>(.+)</string>"
    songInfoKey = "\t\t<dict>"
    songCloseInfoKey = "\t\t</dict>"
    artistKey = "\t\t\t<key>Artist</key>"
    genreKey =  "\t\t\t<key>Genre</key>"
    currentArtist = ""
    currentGenre = "" #both of these can theoretically be blank
    allArtists = list() # to pass to FindGenreSpanningArtists
    readSongInfoFlag = False
    for line in libraryFile:
        if songInfoKey in line:
            readSongInfoFlag = True
        elif songCloseInfoKey in line:
            
            allArtists.append(Artist(name = currentArtist, genre = currentGenre))        
            if currentArtist not in seenArtists and "metal" in currentGenre.lower():
                #limiting scope to one genre for the moment for ease of observation
                seenArtists.append(currentArtist)
                artists.append(Artist(name = currentArtist, genre = currentGenre))
                readSongInfoFlag = False
            currentArtist = ""
            currentGenre = ""
        elif readSongInfoFlag == True :
            if artistKey in line:
                currentArtist =  re.search(tagRegex,line).group(1)
            if genreKey in line:
                currentGenre = re.search(tagRegex,line).group(1)
                
    if writeGenreReport == True:
        FindGenreSpanningArtists(allArtists)
    
    return(artists)       


def ParseFromMetalArchives(artists):
    
    """In wider use will probably need one of these per archival site rather than relying on one
    widely general music encyclopedia
    <div id="band_stats">
            <dl class="float_left">
                <dt>Country of origin:</dt>
                <dd><a href="http://www.metal-archives.com/lists/GB">United Kingdom</a></dd>
                <dt>Location:</dt>
                <dd>Coventry, England</dd>
                <dt>Status:</dt>
                <dd class="split_up">Split-up</dd>
                <dt>Formed in:</dt>
                <dd>1986</dd> 
            </dl>
            <dl class="float_right">
                <dt>Genre:</dt>
                <dd>Death Metal</dd>
                <dt>Lyrical themes:</dt>
                <dd>War, Loss, Sacrifice, Brotherhood, Warhammer 40,000</dd>
                <dt>Last label:</dt>
                <dd><a href="http://www.metal-archives.com/labels/Metal_Blade_Records/3">Metal Blade Records</a></dd>
            </dl>
            <dl style="width: 100%;" class="clear">
                <dt>Years active:</dt>
                <dd>
                                                                    
                            1986-2016                                    </dd>
            </dl>
        </div>    
    """ 
    U = Utility()
    #P = Pickler
    serializedArtistList = []
    notFoundArtists = []
    parsedArtists = [] 
    baseURL = U.testURLs[0]
    #first, see if an earlier processing attempt aborted or was interrupted, check for serialized web scraping resuilts
    if os.path.isfile(U.serializeArtistFile):
        
        decision = raw_input("Serialize file exists from previous run.\n (R)esume, (I)gnore, (D)elete? (Default: Ignore)")
        if decision.lower() == "d":
            os.remove(U.serializeArtistFile)
        elif decision.lower() == "r":
            #Determine which artists have been processed already, remove them from the artist list parameter to bypass
            #processing them over again then .append the deserialized list to the result set
            deSerialized = cPickle.load(open(U.serializeArtistFile, 'rb'))
            #print type(deSerialized)
            #print type(deSerialized[0])
            
            serializedArtistList = [artist.name for artist in deSerialized]
            artists = [artist for artist in artists if artist.name not in serializedArtistList]
            parsedArtists += deSerialized
            print len(deSerialized)
            print deSerialized[1]
            
            print "Resuming from serialized file after these", len(parsedArtists), "\n".join(serializedArtistList)
    for currentArtist in artists:
        artistPageURL = baseURL + currentArtist.name.replace(" ","_")
        html = urllib.urlopen(artistPageURL).read()
        if "error 404" in html.lower() or "may refer to:" in html.lower(): 
            #"may refer to" indicates two + bands with the same name
            notFoundArtists.append(currentArtist)
        else:
            print "Trying to parse:",currentArtist.name,"from",artistPageURL
            soup = BeautifulSoup(html,"lxml")
            bandStats = soup.find("div",id="band_stats").find_all("dd")
            parsedArtist = Artist(currentArtist.name,country = bandStats[0].find("a").contents[0].decode('utf8'),
                                    activeSince = bandStats[3].contents[0].decode('utf-8'), albums= [])

            print "Country:", parsedArtist.country
            print "Active since:", parsedArtist.activeSince
            
            discographyURL = soup.find("div",id="band_tab_discography").find("a")['href']
            discogHTML = urllib.urlopen(discographyURL).read().decode('utf-8','ignore')
            if "error 404" in discogHTML.lower():
                notFoundArtists.append(currentArtist)
            else:
                discogSoup = BeautifulSoup(discogHTML,"lxml")
                discogRows = discogSoup.find_all("tr") 
                print "\tAlbums:"
                for i in range(1,len(discogRows)):
                    
                    currentFields = discogRows[i].find_all("td")
                    currentAlbum = Album(currentFields[0].find("a").contents[0],
                                         currentFields[1].contents[0],
                                         currentFields[2].contents[0])
                    print"\t\t",currentAlbum.year, "\t",currentAlbum.albumType, "\t\t" ,currentAlbum.name.encode("utf-8","ignore")
                    parsedArtist.albums.append(currentAlbum)
                    currentAlbum = None
                parsedArtists.append(parsedArtist)    
                print parsedArtist
                raw_input("Pausing")
                parsedArtist = None
                time.sleep(10)
        if len(parsedArtists) >0 and len(parsedArtists) % 10 == 0: 
            #testing
            break
    with open(U.serializeArtistFile,"wb+") as serializeFile:
        
        cPickle.dump(parsedArtists,serializeFile, cPickle.HIGHEST_PROTOCOL)
    if len(notFoundArtists) >0:
        with open(U.artistErrorReport, "wb+") as errorReport:
            reportWriter = csv.writer(errorReport, delimiter = ",", quoting=csv.QUOTE_MINIMAL)
            for artist in notFoundArtists:
                reportWriter.writerow(artist.name)
    raw_input("Pausing after serializing and artist scraping...")