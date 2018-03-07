import model.story_world.classes.Item as Item
import model.story_world.entities as Entity
import model.externals.wordnet as WordNet

def assignPropBySeating(actor, scene):
    if Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList[
        "corner of the room"].name, None) != (None, None, None) and actor.name != "Wanda":
        Entity.charList[actor.name.lower()].hasPerProperty("noisy", scene)
        Entity.charList[actor.name.lower()].hasPerProperty("rough", scene)
        # return elabFor

    elif Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList["front row"].name, None) != (None, None, None):
        #print(Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList["front row"].name))
        #print("True for: ", Entity.charList[actor.name.lower()].name)
        grades = Item.Item("grades")
        shoes = Item.Item("shoes")

        Entity.charList[actor.name.lower()].hasAttribute(grades, WordNet.getVerbList("have", negator=None),
                                                         scene).hasPerProperty("good", scene + "ext")
        Entity.charList[actor.name.lower()].hasAttribute(shoes, WordNet.getVerbList("wear", negator=None),
                                                         scene).hasAppProperty("not muddy", scene + "ext")

    elif actor.name == "Wanda":
        # print("True for: ", Entity.charList[actor.name.lower()].name)
        shoes = Item.Item("shoes")

        actor.hasAttribute(shoes, WordNet.getVerbList("wear", negator=None), scene).hasAppProperty("muddy", scene + "ext")

    else:
        return None


def checkIfPersonIsPoor(actor, scene):
    # print(Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["boggins heights"].name)[0].name)
    # print(Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["frame house"].name)[0].name)

    if Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["boggins heights"].name, None) != (None, None, None) and \
                    Entity.charList[actor.name.lower()].queryLocation("live",
                                                                      Entity.locList["frame house"].name, None) != (None, None, None):
        Entity.charList[actor.name.lower()].hasPerProperty("poor", scene)
    else:
        return None
