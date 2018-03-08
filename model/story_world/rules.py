import model.story_world.classes.Item as Item
import model.story_world.entities as Entity
import model.externals.wordnet as WordNet


def assignPropBySeating(actor, scene):
    if Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList["corner of the room"].name, None) != (None, None, None) and actor.name != "Wanda":
        Entity.charList[actor.name.lower()].hasPerProperty("noisy", scene)
        Entity.charList[actor.name.lower()].hasPerProperty("rough", scene)

    elif Entity.charList[actor.name.lower()].queryLocation("sit", Entity.locList["front row"].name, None) != (None, None, None):
        grades = Item.Item("grades")
        shoes = Item.Item("shoes")

        Entity.charList[actor.name.lower()].hasAttribute(grades, WordNet.getVerbList("have", negator=None), scene)
        grades.hasPerProperty("good", scene + "aext")

        Entity.charList[actor.name.lower()].hasAttribute(shoes, WordNet.getVerbList("wear", negator=None), scene)
        shoes.hasAppProperty("not muddy", scene + "bext")

        return grades, shoes

    elif actor.name == "Wanda":
        shoes = Item.Item("shoes")

        actor.hasAttribute(shoes, ("wear", WordNet.getVerbList("wear", negator=None)), scene)
        shoes.hasAppProperty("muddy", scene + "ext")

        return shoes

    else:
        return None


def checkIfPersonIsPoor(actor, scene):
    if Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["boggins heights"].name, None) != (None, None, None) and \
                    Entity.charList[actor.name.lower()].queryLocation("live", Entity.locList["frame house"].name, None) != (None, None, None):

        Entity.charList[actor.name.lower()].hasPerProperty("poor", scene)
    else:
        return None
