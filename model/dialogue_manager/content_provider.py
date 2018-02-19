import re

import distance

import model.story_world.entities as Entity
from model.conjugator import conjugator

def confirmCharacter(actor, questType, person=None, relationship=None, action=None, location=None, item=None, propType=None):
    names = {}
    val = []
    #print("person: ", person)
    #print("relationship: ", relationship)
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
        # 2 - What
        if questType == 0:
            return whoQuestion(Entity.charList[names[val[0]]], person, relationship)
        if questType == 1:
            return whereQuestion(Entity.charList[names[val[0]]], action, location)
        if questType == 2:
            return whatQuestion(Entity.charList[names[val[0]]], item, propType, action)
        if questType == 3:
            return whenQuestion(Entity.charList[names[val[0]]], action)

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

    elif person is None and relationship is not None and actor.queryRelationship(person, relationship) is not None:
        answer = actor.queryRelationship(person, relationship)
        output = actor.name.title() + "'s " + relationship + " is " + answer

    elif person is not None and relationship is None and actor.queryRelationship(person, relationship) is not None:
        #print("actor: ", actor.name)
        #print("person: ", person)
        #print("relationship: ", relationship)
        rel = actor.queryRelationship(person, relationship)
        if len(rel) > 1 and type(rel) is not str:
            out_rel = ", ".join(rel[:-1]) + " and " + rel[len(rel) - 1]
        else:
            out_rel = rel

        output = person.title() + " is " + actor.name.title() + "'s " + out_rel

    else:
        output = "I don't know."

    return output


def whatQuestion(actor, item, propType, action):
    output = ""
    prop = []

    print(actor.name, " items: ", actor.attr)
    print("Item: ", actor.queryAttribute(action, Entity.itemList[item].name))
    if action is None and item is not None and actor.queryAttribute(action, Entity.itemList[item].name) is not None:
        print("hey")
        item = actor.queryAttribute(action, Entity.itemList[item].name)

        if propType == "appearance":
            for properties in item.appProp:
                prop.append(properties[0])

        print("Properties: ", prop)
        #elif propType == "personality":
        #    prop = item.perProp
        #elif propType == "amount":
        #    prop = item.amtProp

        #print("property: ", prop)

        prop = [item for sublist in prop for item in sublist]

        if prop is not None:
            if len(prop) > 1 and type(prop) is not str:
                out_prop = ", ".join(prop[:-1]) + " and " + prop[len(prop) - 1]
            else:
                out_prop = prop[0]

            output = actor.name.title() + "'s " + item.name + " is " + out_prop

    elif action is None and item is None:
        prop = []
        if propType == "appearance":
            for properties in actor.appProp:
                prop.append(properties[0])

            if prop is not None:
                if len(prop) > 1:
                    out_prop = ", ".join(prop[:-1]) + " and " + prop[len(prop) - 1]
                else:
                    out_prop = prop[0]

                output = actor.name.title() + "'s appearance is " + out_prop

        elif propType == "property":
            for properties in actor.perProp:
                prop.append(properties[0])

            print("personality: ", actor.perProp)

            if prop is not None:
                if len(prop) > 1:
                    out_prop = ", ".join(prop[:-1]) + " and " + prop[len(prop) - 1]
                else:
                    out_prop = prop[0]

                output = actor.name.title() + "'s personality is " + out_prop

        elif propType == "amount":
            prop = actor.amtProp

    else:
        output = "I don't know"

    return output


def whereQuestion(actor, action, location):
    output = ""

    #print("actor: ", actor)
    if location is None and actor.queryLocation(action, location) is not None:
        location, scene = actor.queryLocation(action, location)
        #print("location: ", location)
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

def whenQuestion(actor, action):
    #print("action ", action)
    act = actor.queryAction(action)
    state = actor.queryState(action, None)

    # print("action: ", action)
    # print("state: ", actor.state)

    print("State: ", state)
    if act is not None:
        output = action
        print("action: ", action)

    elif state is not None:
        output = state
        print("state: ", state)

    else:
        output = "I don't know"

    return output