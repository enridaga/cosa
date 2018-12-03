
def saveGraph(dic, output):
    f = open(output,'w')
    f.write(str(dic))
    f.close()

def loadGraph(input):
    f = open(input,'r')
    data=f.read()
    f.close()
    return eval(data)
    
def shitHappens():
    print "It does indeed!"