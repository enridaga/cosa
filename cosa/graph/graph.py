def save(dic, output):
    f = open(output,'w')
    f.write(str(dic))
    f.close()

def load(input):
    f = open(input,'r')
    data=f.read()
    f.close()
    return eval(data)
    
def shitHappens():
    print "It does indeed!"