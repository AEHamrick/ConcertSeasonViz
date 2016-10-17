from itunesParse import *
from Classes import *

U = Utility()


print U.testXML
testArtistList = ParseLibForArtists(U.testXML)

print testArtistList
