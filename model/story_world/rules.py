import model.story_world.entities as ent
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

def assignPropBySeating(actor, scene):
    if ent.charList[actor.name.lower()].queryLocation("sit", ent.locList["boggins heights"].name) is not None and actor.name != "Wanda":
        ent.charList[actor.name.lower()].hasProperty("noisy", scene)
        ent.charList[actor.name.lower()].hasProperty("rough", scene)
        # return elabFor

    elif ent.charList[actor.name.lower()].queryLocation("sit", ent.locList["front row"].name) is not None:
        ent.charList[actor.name.lower()].hasAttribute(ent.itemList["grades"].hasProperty("good", scene), getVerbList("have", negator=None), scene)
        ent.charList[actor.name.lower()].hasAttribute(ent.itemList["shoes"].hasProperty("not muddy", scene), getVerbList("wear", negator=None), scene)

    elif actor.name == "Wanda":
        actor.hasAttribute(ent.itemList["shoes"].hasProperty("muddy", scene), getVerbList("wear", negator=None), scene)

    else:
        return None

def checkIfPersonIsPoor(actor, scene):
    if ent.charList[actor.name.lower()].queryLocation("live", ent.locList["boggins heights"].name) is not None and ent.charList[actor.name.lower()].queryLocation("live", ent.itemList["frame house"].name) is not None:
            ent.charList[actor.name.lower()].hasProperty("poor", scene)
    else:
        return None