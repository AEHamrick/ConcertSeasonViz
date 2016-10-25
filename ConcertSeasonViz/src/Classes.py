from collections import namedtuple

#Artist = namedtuple("Artist","name ID country activeSince genre genreID")

class Artist(namedtuple("Artist",["name", "ID", "country", "activeSince", "genre", "genreID", "albums"])):
    def __new__(cls, name, ID=None, country=None, activeSince=None, genre=None, genreID=None, albums=[]):
        return super(Artist, cls).__new__(cls, name, ID, country, activeSince, genre, genreID, albums)

class Album(namedtuple("Album",["name", "albumType", "year"])):
    def __new__(cls, name, albumType=None, year=None):
        return super(Album, cls).__new__(cls, name, albumType, year)


class Utility(object):
    """Bucket for utility functionality that may be repeated otherwise"""
    def __init__(self):
        self._testXML = 'C:\Users\Evan\Desktop\Library.xml'
        self._reportLocation = 'C:\Temp\\'
        self._genresOfInterest = ["Metal","Rock","Electronic","Folk "]
        self._testURLs = ["http://www.metal-archives.com/bands/"]
        self._tempPath = "C:\Temp\\"
        self._serializeArtistFile = self._tempPath + "serializedArtists.list"
        self._artistErrorReport = self._tempPath + "artistErrorReport.csv"
        self._albums = []
        
        
    @property
    def testXML(self):
        return self._testXML
    
    @property
    def reportLocation(self):
        return self._reportLocation
    
    @property
    def genresOfInterest(self):
        return self._genresOfInterest
    
    @property 
    def testURLs(self):
        return self._testURLs
    @property
    def serializeArtistFile(self):
        return self._serializeArtistFile 
    @property
    def artistErrorReport(self):
        return self._artistErrorReport