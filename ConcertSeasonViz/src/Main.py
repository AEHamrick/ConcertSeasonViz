from Parsing import *
from Classes import *
import cPickle
U = Utility()


print U.testXML
allArtists = ParseLibForArtists(U.testXML)
allArtists.sort(key = lambda tup: tuple(tup[0].lower()))
print len(allArtists), " artists parsed"
if (raw_input("Print artist list?").lower() == "y"):
    for i in range(0,len(allArtists)):
        print "Artist name",allArtists[i].name

allGenres = set([artist.genre for artist in allArtists])
allGenres = sorted(allGenres)

#for genre in allGenres:
#    print genre

ParseFromMetalArchives(allArtists)

