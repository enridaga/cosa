import csv
import datetime

def saveGraph(dic, output):
    f = open(output,'w')
    f.write(str(dic))
    f.close()

def loadGraph(input):
    f = open(input,'r')
    data=f.read()
    f.close()
    return eval(data)

def __getParent(code, dictionary):
    '''
    -check if the end stub is 80 or 10.
    -if 80, see if there is a 10 that uses the same base code, this is the parent
    -if not, move up the chain
    -if 10, just move up the chain
    '''
    hier = int(dictionary[code]["hierarchy"])

    if (hier <= 2):
        #print "hierarchy too low"
        return False

    if (dictionary[code]["codeSuffix"] == "80"):
        #See if there is another instance of this Goods Code with the suffix 10...
        parentCode = dictionary[code]["codeBase"] + "-10"
        if (parentCode in dictionary):
            #print "found a 10"
            return parentCode

    #if we are here, the "-10" suffix didn't work, just traverse up the tree
    nextHierarchy = hier - 2
    #Try this next block repeatedly until we find something or get down to 2, sometimes
    #you have to search up a couple of levels before you find something
    while (nextHierarchy >= 2):
        parentCode = code[:nextHierarchy]
        for x in range(10-nextHierarchy):
            parentCode = parentCode + "0"
        parentCode += "-80"
        if (parentCode in dictionary):
            #print "found a parent"
            return parentCode
        nextHierarchy -= 2

    #if we've made it this far, we didn't find a parent - technically this shouldn't happen, everything should have a parent
    print "****DIDNT FIND ANYTHING****"
    return False

def csv2graph(input, output):
    dictionary = {}
    with open(input, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        print "Building dictionary"
        for row in csvreader:
            #split on the first space and return the left chunk (to remove the trailing " 80")
            codeBase = row["Goods code"].split()[0]
            codeSuffix = row["Goods code"].split()[1]
            #replace space with dash, so "0101020305 80" becomes "0101020305-80"
            code = row["Goods code"].replace(' ', '-')
            dictionary[code] = {}
            dictionary[code]['row'] = row
            dictionary[code]['code'] = code
            dictionary[code]['hierarchy'] = row['Hier.Pos.']
            dictionary[code]["label"] = row["Description"]
            dictionary[code]["codeBase"] = codeBase
            dictionary[code]["codeSuffix"] = codeSuffix

    for key in dictionary:
        currentKey = key
        keepLooping = True
        while (keepLooping):
            parentKey = __getParent(currentKey, dictionary)
            if (parentKey):
                dictionary[currentKey]['parent'] = parentKey
                currentKey = parentKey
            else:
                dictionary[currentKey]['parent'] = False
                keepLooping = False

    graph = {'sub': []}
    for key in dictionary:
        dictionary[key].pop('hierarchy', None)
        dictionary[key].pop('codeBase', None)
        dictionary[key].pop('codeSuffix', None)
        if(dictionary[key]['parent'] == False):
            graph['sub'].append(dictionary[key])
        else:
            p = dictionary[key]['parent']
            if not 'sub' in dictionary[p]:
                dictionary[p]['sub'] = []
            dictionary[p]['sub'].append(dictionary[key])

    saveGraph(graph, output)
    
def shitHappens():
    print "It does indeed!"