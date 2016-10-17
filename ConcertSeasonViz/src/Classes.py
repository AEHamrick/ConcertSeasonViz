class Artist:
    """Init with name, country, activeSince, genre
    
    name & country are expected to be strings
    activeSince is YYYY-MM-DD and represents the founding date of the artist
    genre is string
    genre ID is numeric, populated once the database is involved
    """
    def __init__(self,name,country,activeSince,genre):
        self.name = name
        self.country = country
        self.activeSince = activeSince
        self.genre = genre
        
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name
        
    @property
    def country(self):
        return self.__country
    @country.setter
    def country(self,country):
        self.__country = country
        
    @property
    def activeSince(self):
        return self.__activeSince
    @activeSince.setter
    def activeSince(self,activeSince):
        self.__activeSince = activeSince
        
    @property
    def genre(self):
        return self.__genre
    @genre.setter
    def genre(self,genre):
        self.__genre = genre
        
    @property
    def genreID(self):
        return self.__genreID
    @genreID.setter
    def genreID(self,genreID):
        self.__genreID = genreID
        
    @property
    def artistID(self):
        return self.__artistID
    @artistID.setter
    def artistID(self,artistID):
        self.__artistID = artistID    
        
class Genre:
    """init with name only
    
    Represents a musical genre;
    name is expected to be a string
    ID is used by and populated from the database
    Parent is a string referring to another genre to establish a relationship; e.g.,
    Bluegrass may have Folk as its parent, likewise Baroque may have Classical, or 
    Southern Rock may have Rock.
    """
    def __init__(self,name):
        self.name = name
        
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name
        
    @property
    def ID(self):
        return self.__ID
    @ID.setter
    def ID(self,ID):
        self.__ID = ID
    
    @property
    def parent(self):
        return self.__parent
    @parent.setter
    def parent(self,parent):
        self.__parent = parent    
        
class Album:
    """init with name,type,releaseDate,artist, songs
    
    releaseDate expected to be YYYY-MM-DD 
    type is album type; expected values: LP, EP, Single, Live, Other
    songs is a list 3 element tuples in order of song name, playing time, track number
    """
    
    def __init__(self,name,albumType,releaseDate,artist):
        self.name = name
        self.albumType = albumType
        self.releaseDate = releaseDate
        self.artist = artist
        self.songs = []
        
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name
        
    @property
    def albumType(self):
        return self.__albumType
    @albumType.setter
    def albumType(self,albumType):
        self.__albumType = albumType
        
    @property
    def releaseDate(self):
        return self.__releaseDate
    @releaseDate.setter
    def releaseDate(self,releaseDate):
        self.__releaseDate = releaseDate
        
    @property
    def artist(self):
        return self.__artist
    @artist.setter
    def artist(self,artist):
        self.__artist = artist
        
    @property
    def songs(self):
        return self.__songs
    @songs.setter
    def songs(self,songs):
        self.__songs = songs
    def addsong(self,song):
        self.__songs.append(song)

class Venue:
    """name and state self explanatory; franchise optional, denotes e.g., House of Blues
    venueID used by database
    """
    
    def __init__(self,name,state):
        self.__name = name
        self.__state = state
            
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self,name):
        self.__name = name
        
    @property
    def state(self):
        return self.__state
    @state.setter
    def state(self,state):
        self.__state = state
        
    @property
    def franchise(self):
        return self.__franchise
    @franchise.setter
    def franchise(self,franchise):
        self.__franchise = franchise
        
    @property
    def venueID(self):
        return self.__venueID
    @venueID.setter
    def venueID(self,venueID):
        self.__venueID = venueID        
        
class Concert:
    
    """venueID and artistID taken from the respective UIDs of the database tables"""
    
    def __init__(self,date,venueID,artistID):
        self.__venueID = venueID
        self.__artistID = artistID
        self.__date = date
        
    @property
    def venueID(self):
        return self.__venueID
    @venueID.setter
    def venueID(self,venueID):
        self.__venueID = venueID 
        
    @property
    def artistID(self):
        return self.__artistID
    @artistID.setter
    def artistID(self,artistID):
        self.__artistID = artistID 
        
    @property
    def date(self):
        return self.__date
    @date.setter
    def date(self,date):
        self.__date = date                     

class Utility(object):
    """Bucket for utility functionality that may be repeated otherwise"""
    def __init__(self):
        self._testXML = r'C:\Users\Evan\Desktop\Library.xml'
    
    @property
    def testXML(self):
        return self._testXML