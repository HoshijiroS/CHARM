from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

def getVerbList(verb, negator=None):
    if negator is not None:
        dummy = [negator + "_" + x.name().split(".")[0] for x in wordnet.synset(verb + '.v.01').lemmas()]
        return list(set(dummy))
    else:
        dummy = [x.name().split(".")[0] for x in wordnet.synset(verb + '.v.01').lemmas()]
        return list(set(dummy))


def getAdjList(adj, negator=None):
    if negator is not None:
        dummy = [negator + "_" + x.name().split(".")[0] for x in wordnet.synsets(adj)]
        return list(set(dummy))
    else:
        dummy = [x.name().split(".")[0] for x in wordnet.synsets(adj)]
        return list(set(dummy))


def getSimilarAdjList(adj, negator=None):
    if negator is not None:
        getAdj = [x for x in wordnet.synsets(adj) if x.name().endswith('.s.01')][0]
        return list(set([negator + "_" + x.name().split('.')[0] for x in getAdj.similar_tos()]))
    else:
        getAdj = [x for x in wordnet.synsets(adj) if x.name().endswith('.s.01')][0]
        return list(set([x.name().split('.')[0] for x in getAdj.similar_tos()]))


def getDefinition(word, verb=None):
    syns = ""

    if verb == "Yes":
        try:
            syns = wordnet.synset(word + '.v.01')
            return syns.definition()
        except Exception as e:
            print("Error on getDefintion: ", e)
    else:
        try:
            syns = wordnet.synsets(word)[0]
            return syns.definition()
        except Exception as e:
            print("Error on getDefinition: ", e)

    return None