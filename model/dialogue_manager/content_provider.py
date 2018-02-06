import model.story_world.entities as Entity
from model.conjugator import conjugator


def whoQuestion(actor, person, relationship):
    if relationship is None:
         if Entity.charList[actor.lower()] is not None:
            type = Entity.charList[actor.lower()].type
            output = ", ".join(type[:-1]) + ", and " + type[len(type) - 1]
            output = actor.capitalize() + " is a " + output
            return output

    else:
        if Entity.charList[actor.lower()] is not None:
            print("Yo")
            answer = Entity.charList[actor.lower()].queryRelationship(person, relationship)
            print("Answer: " + answer)
            output = actor.capitalize() + "'s " + relationship + " is " + answer + "."
            return output

# def whatQuestion(actor):
#    if ent.charList[actor.lower()] is not None:
#        output = ent.charList[actor.lower()].prop
#        return output

def whatQuestion(actor, item, action):
    # print(ent.charList[actor.lower()].attr)
    if item is None and action is None:
        if Entity.charList[actor.lower()] is not None:
            props = Entity.charList[actor.lower()].prop
            output = ", ".join(props[:-1]) + ", and " + props[len(props) - 1]
            return output

    elif Entity.charList[actor.lower()] is not None and Entity.charList[actor.lower()].queryAttribute(item,
                                                                                                      action) is not None:
        attribute, scene = Entity.charList[actor.lower()].queryAttribute(item, action)
        output = actor.capitalize() + " " + action + " " + attribute.prop[0][0] + " " + item
        # output = attribute.prop[0][0]
        return output
    else:
        return "I don't know."

def whereQuestion(actor, action, location):
    if Entity.charList[actor.lower()] is not None and Entity.charList[actor.lower()].queryLocation(action, location) is not None:
        location, scene = Entity.charList[actor.lower()].queryLocation(action, location)
        if actor == Entity.charList["students"].name or actor == Entity.charList["people"].name or actor == Entity.charList["girls"].name:
            conj_verb = conjugator.conjugate(action, number=conjugator.PLURAL, tense=conjugator.PRESENT_TENSE)
        else:
            conj_verb = conjugator.conjugate(action, number=conjugator.SINGULAR, tense=conjugator.PRESENT_TENSE)

        output = actor.capitalize() + " " + conj_verb + " in " + location.name + "."
        return output
    else:
        return "I don't know"

#def whyQuestion(actor, query):
#    if ent.charLIst[actor.lower()] is not None:
#        if