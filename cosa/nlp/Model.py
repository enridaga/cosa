
class Model:
    def word2vec = None
    def __init__(modelFile):
        try:
            word2vec = Word2VecModel.load(sc, modelpath)
        except Exception as e:
            sc.stop()
            exit()
    def similarToTerm(term, num):
        return word2vec.findSynonyms(term, num)
    def similarToText(text, num):
        
        
        