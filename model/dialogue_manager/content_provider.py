import random
import re

import distance

import model.story_world.entities as Entity
import model.story_world.story_scenes as ref


def formatMultipleItems(listAnswer):
    if len(listAnswer) > 1 and type(listAnswer) is not str:
        out = ", ".join(listAnswer[:-1]) + " and " + listAnswer[len(listAnswer) - 1]
    elif type(listAnswer) is str:
        out = listAnswer
    else:
        out = listAnswer[0]

    return out


def confirmCharacter(actor, questType, person=None, relationship=None, action=None, location=None, item=None,
                     propType=None):
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
        # 2 - What
        # 3 - Why
        if questType == 0:
            return whoQuestion(Entity.charList[names[val[0]]], person, relationship)
        if questType == 1:
            return whereQuestion(Entity.charList[names[val[0]]], action, location)
        if questType == 2:
            return whatQuestion(Entity.charList[names[val[0]]], item, propType, action)
        if questType == 3:
            return whyQuestion(Entity.charList[names[val[0]]], action)

    elif match_length < 3:
        return "unknown", None
    else:
        return "confirmation", Entity.charList[names[val[0]]]


def whoQuestion(actor, person, relationship):
    try:
        char, rel = actor.queryRelationship(person, relationship)
    except Exception as e:
        print(e)
        return "unknown", None

    if relationship is None and person is None:
        charType = actor.charType

        output = formatMultipleItems(charType)

        # output = actor.name.title() + " is a " + output

        return "type", [actor, output]

    elif person is None and relationship is not None:
        # output = actor.name.title() + "'s " + relationship + " is " + char.name.title()
        # print(actor.name.title() + "'s " + relationship + " is " + char.name.title())
        return "relationship_name", [actor, relationship, char]

    elif relationship is None and person is not None:
        # output = char.name.title() + " is " + actor.name.title() + "'s " + out_rel

        return "relationship_rel", [actor, rel, char]

    else:
        # output = "I don't know"
        return "unknown", None


def whatQuestion(actor, item, propType, action):
    prop = []

    try:
        act, item, event = actor.queryAttribute(action, Entity.itemList[item].name, None)
    except Exception as e:
        print(e)
        return "unknown", None

    if action is None and item is not None:
        if propType == "appearance":
            for properties in item.appProp:
                prop.append(properties[0])

        elif propType == "amount":
            for properties in item.amtProp:
                prop.append(properties[0])

        if prop is not None:
            out_prop = formatMultipleItems(prop)

            if propType == "appearance":
                # output = actor.name.title() + "'s " + item.name + " is " + out_prop

                return "item_appearance", [actor, item.name, out_prop]
            else:
                # output = actor.name.title() + " has " + out_prop + " " + item.name

                return "item_amount", [actor, item.name, out_prop]

    elif action is None and item is None:
        prop = []
        if propType == "appearance":
            for properties in actor.appProp:
                prop.append(properties[0])

            if prop is not None:
                out_prop = formatMultipleItems(prop)

                # output = actor.name.title() + "'s appearance is " + out_prop

                return "actor_appearance", [actor, out_prop]

        elif propType == "property":
            for properties in actor.perProp:
                prop.append(properties[0])

            if prop is not None:
                out_prop = formatMultipleItems(prop)

                # output = actor.name.title() + "'s personality is " + out_prop

                return "actor_personality", [actor, out_prop]

    else:
        return "unknown", None

    return "unknown", None


def whereQuestion(actor, action, location):
    try:
        action, loc, event = actor.queryLocation(action, location)
    except Exception as e:
        print(e)
        return "unknown", None

    if location is None and loc is not None:
        # if actor.name == Entity.charList["students"].name or actor.name == Entity.charList[
        #     "people"].name or actor.name == \
        #         Entity.charList["girls"].name:
        #     conj_verb = conjugator.conjugate(action, number=conjugator.PLURAL, tense=conjugator.PRESENT_TENSE)
        # else:
        #     conj_verb = conjugator.conjugate(action, number=conjugator.SINGULAR, tense=conjugator.PRESENT_TENSE)

        if type(location) is str:
            output = actor.name.title() + " " + action[0] + " in " + loc
            print(output)

            return "location", [actor, action, loc]
        else:
            output = actor.name.title() + " " + action[0] + " in " + loc.name
            print(output)

            return "location", [actor, action[0], loc.name]

    else:  # output = "I don't know"
        return "unknown", None


def whyQuestion(actor, action):
    act, obj, event = actor.queryAction(action, None)
    state, event = actor.queryState(action, None)

    causeList = []

    if state is None:
        # output = act
        print("action: ", act[0])

    elif act is None:
        index = ref.queryLookup(event)
        event, actor, qType = ref.getEventFromLookup(index)

        cause_event = ref.queryRelations(event, "cause")

        print("cause_event: ", cause_event)

        if cause_event is not None:
            for evs in cause_event:
                causeList.append(assembleSentence(evs, "cause"))

                # if len(causeList) > 1:
                #     return "; ".join(causeList[:-1]) + " and " + causeList[len(causeList) - 1]
                #
                # elif len(causeList) == 1:
                #     return causeList[0]

        return "cause", causeList

    else:
        # return "I don't know"

        return "unknown", None


def assembleProp(attr, event):
    appProp, event = attr.queryProperty(None, "appearance", event)
    print("appProp: ", appProp)
    amtProp, event = attr.queryProperty(None, "amount", event)
    perProp, event = attr.queryProperty(None, "personality", event)

    if perProp is None and amtProp is None:
        out_app = formatMultipleItems(appProp)

        return "appearance", out_app

    elif appProp is None and perProp is None:
        out_amt = formatMultipleItems(amtProp)

        return "amount", out_amt

    elif amtProp is None and appProp is None:
        out_per = formatMultipleItems(perProp)

        return "personality", out_per


def assembleSentence(event, sentenceType):
    try:
        index = ref.queryLookup(event)
        event, actor, qType = ref.getEventFromLookup(index)
        actor = Entity.charList[actor.lower()]
    except Exception as e:
        print(e)
        return "unknown", None

    out_obj = ""
    out_state = ""

    if sentenceType == "cause":
        if qType == "state":
            state, event = actor.queryState(None, event)

            out_state = formatMultipleItems(state[0])

            # output = "Because " + actor.name.title() + " was " + out_state

            return "cause_state", [actor, out_state]

        elif qType == "action":
            action, obj, event = actor.queryAction(None, event)

            out_obj = formatMultipleItems(obj[0])

            # output = "Because " + actor.name.title() + " " + action[0] + " " + out_obj

            return "cause_action", [actor, action[0], out_obj]

        elif qType == "desire":
            des, obj = actor.queryDesire(None, event)

            out_obj = formatMultipleItems(obj)

            # output = "Because " + actor.name.title() + " desired to " + des[0] + " " + out_obj

            return "cause_desire", [actor, random.choice(des), out_obj]

        elif qType == "feeling":
            feel, obj = actor.queryFeeling(None, event)

            out_obj = formatMultipleItems(obj)

            # output = "Because " + actor.name.title() + " felt " + des[0] + " towards " + out_obj

            return "cause_feeling", [actor, random.choice(feel), out_obj]

        elif qType == "attribute":
            action, attr, scene = actor.queryAttribute(None, None, event)

            attrList = []

            for entries in attr:
                qType, attr_prop = assembleProp(entries, event)
                if qType == "appearance":
                    # attrList.append(actor.name.title() + "'s " + entries + " looks " + attr_prop)
                    attrList.append("item_appearance", [actor, entries, attr_prop])

                elif qType == "amount":
                    # attrList.append(actor.name.title() + " has " + attr_prop + " " + entries)
                    attrList.append("item_amount", [actor, entries, attr_prop])

                elif qType == "personality":
                    # attrList.append(actor.name.title() + "'s " + entries + " is " + attr_prop)
                    attrList.append("item_personality", [actor, entries, attr_prop])

            # if len(attrList) > 1 and type(attrList) is not str:
            #     out_list = ", ".join(attrList[:-1]) + " and " + attrList[len(attrList) - 1]
            #
            # elif len(attr) == 1:
            #     out_list = attrList

            # output = "Because " + out_list

            return "cause_attribute", attrList
