import re

import distance

import model.story_world.entities as Entity
from model.conjugator import conjugator


def confirmCharacter(actor, person, relationship, action, location, type):
    names = {}
    val = []

    for key, value in Entity.charList.items():
        size = distance.lcsubstrings(actor.lower(), key)
        if bool(size):
            size = max(size, key=len)
            length = len(size)
            if length < 10:
                length = "0" + str(length)
            else:
                length = str(length)

            names.update({length + key: key})
            val.append(length + key)

    val.sort(reverse=True)
    match_length = int(re.findall('\d+', val[0])[0])

    if match_length == len(Entity.charList[names[val[0]]].name):
        # 0 - Who
        # 1 - Where
        if type == 0:
            return whoQuestion(Entity.charList[names[val[0]]], person, relationship)
        if type == 1:
            return whereQuestion(Entity.charList[names[val[0]]], action, location)

    elif match_length < 3:
        return "I don't know."
    else:
        return "Do you mean " + Entity.charList[names[val[0]]].name.title() + "?"


def whoQuestion(actor, person, relationship):
    output = ""

    if relationship is None and person is None:
        charType = actor.type
        if len(charType) > 1 and type(charType) is not str:
            output = ", ".join(charType[:-1]) + " and " + charType[len(charType) - 1]
        else:
            output = charType[0]

        output = actor.name.title() + " is a " + output

    elif person is None:
        answer = actor.queryRelationship(person, relationship)
        output = actor.name.title() + "'s " + relationship + " is " + answer

    elif relationship is None:
        rel = actor.queryRelationship(person, relationship)
        if len(rel) > 1 and type(rel) is not str:
            out_rel = ", ".join(rel[:-1]) + " and " + rel[len(rel) - 1]
        else:
            out_rel = rel

        output = person + " is " + actor.name.title() + "'s " + out_rel

    else:
        output = "I don't know."

    return output


def whatQuestion(actor, item, action):
    if item is None and action is None:
        if Entity.charList[actor.lower()] is not None:
            props = Entity.charList[actor.lower()].prop
            output = ", ".join(props[:-1]) + ", and " + props[len(props) - 1]

    elif Entity.charList[actor.lower()] is not None and Entity.charList[actor.lower()].queryAttribute(item,
                                                                                                      action) is not None:
        attribute, scene = Entity.charList[actor.lower()].queryAttribute(item, action)
        output = actor.title() + " " + action + " " + attribute.prop[0][0] + " " + item

    return output


def whereQuestion(actor, action, location):
    output = ""

    if actor.queryLocation(action, location) is not None:
        location, scene = actor.queryLocation(action, location)
        if actor.name == Entity.charList["students"].name or actor.name == Entity.charList[
            "people"].name or actor.name == \
                Entity.charList["girls"].name:
            conj_verb = conjugator.conjugate(action, number=conjugator.PLURAL, tense=conjugator.PRESENT_TENSE)
        else:
            conj_verb = conjugator.conjugate(action, number=conjugator.SINGULAR, tense=conjugator.PRESENT_TENSE)

        if type(location) is str:
            output = actor.name.title() + " " + conj_verb + " in " + location
        else:
            output = actor.name.title() + " " + conj_verb + " in " + location.name

    else:
        output = "I don't know."

    return output
