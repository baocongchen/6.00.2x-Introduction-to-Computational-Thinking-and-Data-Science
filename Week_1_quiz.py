import string
PATH_TO_FILE = 'words.txt'
def loadWords():
    inFile = open(PATH_TO_FILE, 'r', 0)
    line = inFile.readline()
    wordlist = string.split(line,',')
    print "  ", len(wordlist), "words loaded."
    return wordlist


