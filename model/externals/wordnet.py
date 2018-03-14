from nltk.corpus import wordnet

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


def getDefinition(word):
    syns = wordnet.synsets(word)

    print(syns[0].definition())

    return syns[0].definition()