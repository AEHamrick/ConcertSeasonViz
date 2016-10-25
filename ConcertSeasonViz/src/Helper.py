import csv
from Classes import Utility

def FindGenreSpanningArtists(artistTuples):
    """This helper function reports on artists in the library that have songs
        across several genres; there are situations where this could be intentional but it's much
        more likely to be the result of badly tagged or mistagged mp3s. Fixing ID3 metadata directly 
        is out of the scope of this project so instead we create a report of genre spanning artists 
        to examine and fix if necessary.
        
        The report is comma delimited in the form of Artist, genre 1, genre 2, ...,genre n
    
    """
    U = Utility()
    
    uniqueDict = {}
    nonUniqueDict = {}
    for currentArtist in artistTuples:
        if currentArtist.name not in nonUniqueDict:
            nonUniqueDict[currentArtist.name] = [currentArtist.genre]
        elif currentArtist.name in nonUniqueDict:
            nonUniqueDict[currentArtist.name] = nonUniqueDict[currentArtist.name
                                                ] + [currentArtist.genre]    
    for key, value in nonUniqueDict.iteritems():
        if len(set(value)) >1: #only interested in cases with more than one item in the value list
            sortedValues = sorted(set(value),key = lambda s: s.lower())
            uniqueDict[key] = ", ".join(sortedValues)
    with open(U._reportLocation + "testCSV.csv","wb+") as genreReport:
        reportWriter = csv.writer(genreReport, delimiter = ",", quoting=csv.QUOTE_MINIMAL)
        reportWriter.writerow(["Artist name","Genre 1", "Genre 2", "Genre X"])
        for key, value in uniqueDict.iteritems():
            fieldList = value.split(",")
            fieldList.insert(0,key)
            reportWriter.writerow(fieldList)
    #raw_input("pausing")    
    print "finished writing genre report"