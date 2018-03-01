from nltk.corpus import wordnet

import model.story_world.classes.Item as Item
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
    location = Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList["front row"].name)

    if Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList[
        "corner of room"].name) is not None and actor.name != "Wanda":
        Entity.charList[actor.name.lower()].hasPerProperty("noisy", scene)
        Entity.charList[actor.name.lower()].hasPerProperty("rough", scene)
        # return elabFor

    elif Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList["front row"].name) is not None:
        grades = Item.Item("grades")
        shoes = Item.Item("shoes")

        Entity.charList[actor.name.lower()].hasAttribute(grades, getVerbList("have", negator=None),
                                                         scene).hasPerProperty("good", scene + "ext")
        Entity.charList[actor.name.lower()].hasAttribute(shoes, getVerbList("wear", negator=None),
                                                         scene).hasAppProperty("not muddy", scene + "ext")

    elif actor.name == "Wanda":
        shoes = Item.Item("shoes")

        actor.hasAttribute(shoes, getVerbList("wear", negator=None), scene).hasAppProperty("muddy", scene + "ext")


    else:
        return None


def checkIfPersonIsPoor(actor, scene):
    # print(Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["boggins heights"].name)[0].name)
    # print(Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["frame house"].name)[0].name)

    if Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["boggins heights"].name) is not None and \
                    Entity.charList[actor.name.lower()].queryLocation("live",
                                                                      Entity.locList["frame house"].name) is not None:
        # print("True")
        Entity.charList[actor.name.lower()].hasPerProperty("poor", scene)
    else:
        return None
