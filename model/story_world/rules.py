from nltk.corpus import wordnet

import model.story_world.entities as Entity


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
    if Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList[
        "boggins heights"].name) is not None and actor.name != "Wanda":
        Entity.charList[actor.name.lower()].hasProperty("noisy", scene)
        Entity.charList[actor.name.lower()].hasProperty("rough", scene)
        # return elabFor

    elif Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList["front row"].name) is not None:
        Entity.charList[actor.name.lower()].hasAttribute(Entity.itemList["grades"].hasProperty("good", scene),
                                                         getVerbList("have", negator=None), scene)
        Entity.charList[actor.name.lower()].hasAttribute(Entity.itemList["shoes"].hasProperty("not muddy", scene),
                                                         getVerbList("wear", negator=None), scene)

    elif actor.name == "Wanda":
        actor.hasAttribute(Entity.itemList["shoes"].hasProperty("muddy", scene), getVerbList("wear", negator=None),
                           scene)

    else:
        return None


def checkIfPersonIsPoor(actor, scene):
    if Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["boggins heights"].name) is not None and \
                    Entity.charList[actor.name.lower()].queryLocation("live",
                                                                      Entity.itemList["frame house"].name) is not None:
        Entity.charList[actor.name.lower()].hasProperty("poor", scene)
    else:
        return None
