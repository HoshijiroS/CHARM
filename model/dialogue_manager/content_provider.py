import random
import re

import distance

import model.story_world.entities as Entity
import model.story_world.story_scenes as ref
import model.externals.wordnet as WordNet


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
        action, loc, event = actor.queryLocation(action, location, None)
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
        event, actor, qType = ref.queryLookup(event)

        cause_event = ref.queryRelations(event, "cause")

        print("cause_event: ", cause_event)

        if cause_event is not None:
            for evs in cause_event:
                causeList.append(assembleSentence(evs))

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
    amtProp, event = attr.queryProperty(None, "amount", event)
    perProp, event = attr.queryProperty(None, "personality", event)

    if perProp is None and amtProp is None and appProp:
        out_app = formatMultipleItems(appProp)

        return "appearance", out_app

    elif appProp is None and perProp is None and amtProp:
        out_amt = formatMultipleItems(amtProp)

        return "amount", out_amt

    elif amtProp is None and appProp is None and perProp:
        out_per = formatMultipleItems(perProp)

        return "personality", out_per

    return None, None


def assembleSentence(event):
    try:
        event, actor, qType = ref.queryLookup(event)
        actor = Entity.charList[actor.lower()]
        actor = Entity.itemList[actor.lower()]
        actor = Entity.locList[actor.lower()]
    except Exception as e:
        print(e)
        #return "unknown", None

    print("qType: ", qType)
    out_obj = ""
    out_state = ""

    if qType == "state":
        state, scene = actor.queryState(None, event)

        out_state = formatMultipleItems(state[0])

        # output = "Because " + actor.name.title() + " was " + out_state

        return "state", [actor, out_state]

    elif qType == "action":
        act, obj, scene = actor.queryAction(None, event)

        out_obj = formatMultipleItems(obj)

        # output = "Because " + actor.name.title() + " " + action[0] + " " + out_obj

        return "action", [actor, act[0], out_obj]

    elif qType == "desire":
        des, obj, scene = actor.queryDesire(None, event)

        out_obj = formatMultipleItems(obj)

        # output = "Because " + actor.name.title() + " desired to " + des[0] + " " + out_obj

        return "desire", [actor, des[0], out_obj]

    elif qType == "feeling":
        feel, obj, scene = actor.queryFeeling(None, event)

        out_obj = formatMultipleItems(obj)

        # output = "Because " + actor.name.title() + " felt " + des[0] + " towards " + out_obj

        return "feeling", [actor, feel[0], out_obj]

    elif qType == "attribute":
        act, attr, scene = actor.queryAttribute(None, None, event)

        if type(attr) is str:
            propType, out_prop = assembleProp(attr, scene + "ext")

            return "attribute", [actor, act[0], attr, propType, out_prop]

        elif type(attr) is list:
            temp = []
            for items in attr:
                propType, out_prop = assembleProp(attr, scene + "ext")
                temp.append(actor, act[0], attr, propType, out_prop)

            return "attribute", temp

        else:
            propType, out_prop = assembleProp(attr, scene + "ext")

            return "attribute", [actor, act[0], attr, propType, out_prop]

        return "attribute", [actor, act[0], attr]

    elif qType == "appProperty":
        prop = []

        try:
            prop, scene = actor.queryProperty(None, "appearance", event)
        except Exception as e:
            # print("Error: ", e, " on ", time, "charAppearance")
            a = 1

        try:
            prop, scene = actor.queryProperty(None, "appearance", event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemAppearance")

        try:
            prop, scene = actor.queryProperty(None, "appearance", event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, "locationAppearance")

        if prop:
            out_prop = formatMultipleItems(prop)
            return "appProperty", [actor, prop]

    elif qType == "perProperty":
        prop = []

        try:
            prop, scene = actor.queryProperty(None, "personality", event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " actorPersonality")

        try:
            prop, scene = actor.queryProperty(None, "personality", event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemPersonality")

        try:
            prop, scene = actor.queryProperty(None, "personality", event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, "locationPersonality")

        if prop:
            out_prop = formatMultipleItems(prop)
            return "perProperty", [actor, out_prop]

    elif qType == "purpose":
        try:
            act, obj, scene = actor.queryPurpose(None, None, event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemPurpose")

        return "purpose", [actor, act[0], obj]

    return "unknown", None


def generateHintsForRelName(ansList):
    actor, rel, char = ansList

    wordCount = len(char[0].name.split())
    if wordCount == 1:
        words = "word"
    else:
        words = "words"

    hintChoices = [
        "the first name of " + actor.name.title() + "'s " + rel + " starts with " + char[0].name[:1] + ".",
        "the name of " + actor.name.title() + "'s " + rel + " is composed of " + str(wordCount) + " " + words + ".",
        "the first name of " + actor.name.title() + "'s " + rel + " has the letter " + char[0].name[2] + "."]

    return hintChoices


def generateHintsForRelRel(ansList):
    actor, rel, char = ansList
    hintChoices =  []

    if [x for x in rel if x == "classmate"] or rel == "classmate":
        hintChoices.extend([
            actor.name.title() + " and " + char.name.title() + " go to the same school. What kind of relationship do you think they have?",
            actor.name.title() + " and " + char.name.title() + " are being taught by the same teacher. So, what do you think is their relationship with each other?",
            actor.name.title() + " and " + char.name.title() + " attend the same classes. What is their relationship to each other then?"
        ])

    if [x for x in rel if x == "friend"] or rel == "friend":
        hintChoices.extend([
            actor.name.title() + " and " + char.name.title() + " talk to each other sometimes. Maybe they are a little more than acquaintances? What can their relationship be?",
            actor.name.title() + " and " + char.name.title() + " can even become best friends if they spend more time together. So, what do you think is their relationship?",
            actor.name.title() + " likes to talk to " + char.name.title() + ". What are they to each other?"
        ])

    if [x for x in rel if x == "best friend"] or rel == "best friend":
        hintChoices.extend([
            actor.name.title() + " and " + char.name.title() + " are always together. Maybe they are a little more than friends? What are they to each other?",
            actor.name.title() + " and " + char.name.title() + " go to school together. So, what do you think is their relationship?",
            actor.name.title() + " and " + char.name.title() + " even share items. What can their relationship be?"
        ])

    if [x for x in rel if x == "father"] or rel == "father":
        hintChoices.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
            actor.name.title() + " and " + char.name.title() + " are relatives. So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
            char.name.title() + " provides for " + actor.name.title() + "'s needs. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
        ])

    if [x for x in rel if x == "daughter"] or rel == "daughter":
        hintChoices.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
            actor.name.title() + " and " + char.name.title() + " are relatives. So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
            actor.name.title() + " loves " + char.name.title() + " very much. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
        ])

    if [x for x in rel if x == "brother"] or rel == "brother":
        hintChoices.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
            actor.name.title() + " and " + char.name.title() + " have the same surname! So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
            char.name.title() + " and " + actor.name.title() + " are relatives. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
        ])

    if [x for x in rel if x == "sister"] or rel == "sister":
        hintChoices.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
            actor.name.title() + " and " + char.name.title() + " have the same surname! So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
            char.name.title() + " and " + actor.name.title() + " are relatives. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
        ])

    if [x for x in rel if x == "teacher"] or rel == "teacher":
        hintChoices.extend([
            actor.name.title() + " respects " + char.name.title() + " very much. Maybe they also see each other at school. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
            actor.name.title() + " learns a lot from listening to " + char.name.title() + ". So, who do you think is " + char.name.title() + " to " + actor.name.title() + "?",
            "you can consider " + char.name.title() + " as " + actor.name.title() + "'s second mother. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
        ])

    if [x for x in rel if x == "student"] or rel == "student":
        hintChoices.extend([
            char.name.title() + " respects " + actor.name.title() + " very much. Maybe they also see each other at school. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
            char.name.title() + " learns a lot from listening to " + actor.name.title() + ". So, who do you think is " + char.name.title() + " to " + actor.name.title() + "?",
            "you can consider " + actor.name.title() + " as " + char.name.title() + "'s second mother. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
        ])

    if [x for x in rel if x == "neighbor"] or rel == "neighbor":
        hintChoices.extend([
            char.name.title() + " and " + actor.name.title() + " live in the same neighborhood. What do you think is their relationship with each other?",
            actor.name.title() + " lives near " + char.name.title() + ". So, who do you think is " + actor.name.title() + " to " + char.name.title() + "?",
            "there is a possibility that " + actor.name.title() + "'s and " + char.name.title() + "'s houses are only beside each other! So, what do you think is their relationship?"
        ])

    return hintChoices


def generateHintsForLocation(ansList):
    actor, action, loc = ansList
    hintChoices = []

    temp = Entity.locList[loc.lower()].appProp
    if temp:
        for properties in temp:
            hintChoices.append(
                "the place where " + actor.name.title() + action + " is " + properties + ".")

    else:
        wordCount = len(loc.split())
        if wordCount == 1:
            words = "word"
        else:
            words = "words"

        hintChoices.extend([
            "the name of the place where " + actor.name.title() + " " + action + " starts with " + loc[:1] + ".",
            "the name of the place where " + actor.name.title() + " " + action + " is composed of " + str(wordCount) + " " + words + ".",
            "the name of the place where " + actor.name.title() + " " + action + " has the letter " + loc[2] + "."])

    return hintChoices


def generateHintsForAppProp(ansList):
    actor, prop = ansList
    hintChoices = []
    temp = []

    for items in prop:
        if "not" in items:
            temp.append((items, WordNet.getSimilarAdjList(items, negator="not")))
        else:
            temp.append((items, WordNet.getSimilarAdjList(items, negator=None)))

    for entries in temp:
        adj, synonyms = entries

        for synonym in synonyms:
            if synonym != adj:
                hintChoices.append("I think it's because " + actor.name.title() + " is __. The word in the blank starts with " + adj[
                    0] + " and its synonym is " + synonym + ". Can you complete the sentence?")

    return hintChoices


def generatePumpsForAppProp(ansList):
    actor, prop = ansList
    hintChoices = []

    hintChoices.extend(["I think it's related to " + actor.name.title() + "'s appearance. Can you describe " + actor.name.title() + "'s appearance?"])

    return hintChoices


def generatePromptsForAppProp(correctAnswer):
    actor, prop = correctAnswer
    hintChoices = []

    hintChoices.extend(["What makes a person " + prop + "? Can you give me some examples?",
                        "Do you know anyone who is " + prop + "? What makes them " + prop + "? Can you describe?"])

    return hintChoices


def generateHintsForAttr(ansList):
    actor, act, attr, propType, prop = ansList
    hintChoices = []

    hintChoices.extend(
        [" related to the " + propType + " of the " + attr.name + " " + actor.name.title() + " " + act + "."])

    return hintChoices


def generateElabForAttr(ansList):
    actor, act, attr, propType, prop = ansList
    propDefs = []
    actDefs = []

    if type(prop) is list and propType == "appearance":
        for properties in prop:
            propDefs.append(WordNet.getDefinition(properties))

    else:
        propDefs.append(WordNet.getDefinition(prop))

    actDefs = WordNet.getDefinition(act, "Yes")

    hintChoices = []

    pronoun = "it"
    if actor.gender == "female":
        pronoun = "she"
    elif actor.gender == "male":
        pronoun = "he"

    hintChoices.extend([" related to the " + attr.name + " " + actor.name.title() + " " + act + ". Since " +
                        pronoun + " " + act + " " + attr.name + " that is " + random.choice(propDefs) + ". "])

    print("hintChoices: ", hintChoices)
    return hintChoices
