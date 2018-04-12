import random
import re

import distance

import model.externals.wordnet as WordNet
import model.story_world.classes.Item as item_type
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

        # output = actor.name.title() + " is a " + output

        return "type", [actor, charType]

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
    act = ""

    try:
        act, item, event = actor.queryAttribute(action, Entity.itemList[item].name, None)
    except Exception as e:
        a = 1

    if action is None and item is not None:
        if propType == "appearance":
            for properties in item.appProp:
                prop.extend(properties[0])

        elif propType == "amount":
            for properties in item.amtProp:
                prop.extend(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

        if propType == "appearance":
            # output = actor.name.title() + "'s " + item.name + " is " + out_prop

            return "item_appearance", [actor, act, item, prop]
        else:
            # output = actor.name.title() + " has " + out_prop + " " + item.name

            return "item_amount", [actor, act, item, prop]

    elif actor and propType:
        prop = []
        if propType == "appearance":
            for properties in actor.appProp:
                prop.extend(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

                # output = actor.name.title() + "'s appearance is " + out_prop

            return "actor_appearance", [actor, prop]

        elif propType == "personality":
            for properties in actor.perProp:
                prop.extend(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

                # output = actor.name.title() + "'s personality is " + out_prop

            return "actor_personality", [actor, prop]

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
            # output = actor.name.title() + " " + action[0] + " in " + loc

            return "location", [actor, action, loc]
        else:
            # output = actor.name.title() + " " + action[0] + " in " + loc.name

            return "location", [actor, action[0], loc.name]

    else:  # output = "I don't know"
        return "unknown", None


def whyQuestion(actor, action):
    act, obj, event = actor.queryAction(action, None)
    state, event = actor.queryState(action, None)

    causeList = []

    if state is None and act is not None:
        # output = act
        print("action: ", act[0])

    elif act is None and state is not None:
        event, actor, qType = ref.queryLookup(event)

        cause_event = ref.queryRelations(event, "cause")

        if cause_event is not None:
            if type(cause_event) is list:
                for evs in cause_event:
                    container = assembleSentence(evs, state[0])
                    if type(container) is list:
                        for entries in container:
                            causeList.append(entries)
                    else:
                        causeList.append(container)
            else:
                container = assembleSentence(cause_event, state[0])
                if type(container) is list:
                    for entries in container:
                        causeList.append(entries)
                else:
                    causeList.append(container)

                    # if len(causeList) > 1:
                    #     return "; ".join(causeList[:-1]) + " and " + causeList[len(causeList) - 1]
                    #
                    # elif len(causeList) == 1:
                    #     return causeList[0]

        return causeList

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


def assembleSentence(event, answer, genType=None, turnType=None, ansType=None):
    actor = ""
    qType = ""

    print("event1: ", event)
    try:
        event, actor, qType = ref.queryLookup(event)
    except Exception as e:
        print("Error on assembleSentence: ", e)

    try:
        actor = Entity.charList[actor.lower()]
    except Exception as e:
        print("Error on assembleSentence: ", e)

    try:
        actor = Entity.itemList[actor.lower()]
    except Exception as e:
        print("Error on assembleSentence: ", e)

    try:
        actor = Entity.locList[actor.lower()]
    except Exception as e:
        print("Error on assembleSentence: ", e)

    pronoun = producePronoun(actor)
    pronoun_obj = producePronoun(actor, genType="objPro")

    if qType == "state":
        state, scene = actor.queryState(None, event)

        out_state = formatMultipleItems(state[0])

        container = []
        if genType == "sentence":
            container.append(actor.name.title() + " was " + out_state)

            if turnType == "prompt":
                container.extend([" What causes a person to be " + state + "? Can you tell me?",
                                  " What about " + actor.name.title() + "'s " + ansType + "caused "
                                  + pronoun_obj + " to be " + out_state + "?",
                                  ])
            return container

        return "state", [actor, out_state, answer]

    elif qType == "action":
        act, obj, scene = actor.queryAction(None, event)

        out_obj = formatMultipleItems(obj)

        if genType == "sentence":
            return actor.name.title() + " " + act[0] + " " + out_obj

        return "action", [actor, act[0], out_obj, answer]

    elif qType == "desire":
        des, obj, scene = actor.queryDesire(None, event)

        out_obj = formatMultipleItems(obj)

        if genType == "sentence":
            return actor.name.title() + " desired to " + des[0] + " " + out_obj

        return "desire", [actor, des[0], out_obj, answer]

    elif qType == "feeling":
        feel, obj, scene = actor.queryFeeling(None, event)

        out_obj = formatMultipleItems(obj)

        if genType == "sentence":
            return actor.name.title() + " felt " + feel[0] + " towards " + out_obj

        return "feeling", [actor, feel[0], out_obj, answer]

    elif qType == "attribute":
        act, attr, scene = actor.queryAttribute(None, None, event)
        out_sent = []

        if type(attr) is str:
            propType, out_prop = assembleProp(attr, scene + "ext")
            sent_prop = formatMultipleItems(out_prop)

            if genType == "sentence":
                if propType == "amount":
                    return actor.name.title() + " " + act[0] + " " + sent_prop + " " + attr
                else:
                    return actor.name.title() + " " + act[0] + " a " + attr + " that is " + sent_prop

            return "attribute", [actor, act[0], attr, propType, out_prop, answer]

        elif type(attr) is list:
            temp = []
            for items in attr:
                propType, out_prop = assembleProp(items, scene + "ext")
                temp.append([actor, act[0], items, propType, out_prop, answer])
                sent_prop = formatMultipleItems(out_prop)
                if propType == "amount":
                    container = actor.name.title() + " " + act[0] + " " + sent_prop + " " + attr.name
                    out_sent.append(container)
                else:
                    container = actor.name.title() + " " + act[0] + " a " + attr.name + " that is " + sent_prop
                    out_sent.append(container)

            if genType == "sentence":
                out_attrs = formatMultipleItems(out_sent)
                return out_attrs

            return "multiple_attribute", temp

        elif type(attr) is item_type:
            propType, out_prop = assembleProp(attr, scene + "ext")

            if genType == "sentence":
                if propType == "amount":
                    return actor.name.title() + " " + act[0] + " " + out_prop + " " + attr.name

                else:
                    return actor.name.title() + " " + act[0] + " a " + attr.name + " that is " + out_prop

            return "attribute", [actor, act[0], attr, propType, out_prop, answer]

        else:
            if genType == "sentence":
                return actor.name.title() + " " + act[0] + " " + attr.name

            return "attribute", [actor, act[0], attr, answer]

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

            if genType == "sentence":
                return actor.name.title() + " looks " + out_prop

            return "appProperty", [actor, prop, answer]

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

            container = []
            if genType == "sentence":
                container.append(actor.name.title() + " is " + out_prop)

                if turnType == "prompt":
                    container.extend([". What is the " + ansType + " of someone who is " + out_prop + "?",
                                      ". What about " + actor.name.title() + "'s " + ansType + " makes " + pronoun_obj
                                      + " " + out_prop + "?",
                                      ". So maybe what causes " + pronoun_obj + " to be " + out_prop
                                      + " has something to do with " + pronoun_obj + " " + ansType + "."
                                      ])

                    return container

                elif turnType == "pump":
                    container.extend([". What is the appearance of someone who is " + out_prop + "?",
                                      " and " + pronoun_obj + " " + ansType + " is the reason."])

                    return container

                return container[0]

            return "perProperty", [actor, prop, answer]

    elif qType == "purpose":
        act = ""
        obj = ""
        try:
            act, obj, scene = actor.queryPurpose(None, None, event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemPurpose")

        if genType == "sentence":
            return actor.name + " " + act[0] + " " + obj

        return "purpose", [actor, act[0], obj, answer]

    elif qType == "location":
        act = ""
        loc = ""
        try:
            act, loc, scene = actor.queryLocation(None, None, event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemPurpose")

        if genType == "sentence":
            return actor.name + " " + act[0] + " in " + loc.name

        return "location", [actor, act[0], loc, answer]

    return "unknown", None


def producePronoun(actor, genType=None):
    pronoun = ""

    if actor.gender:
        if genType == "objPro":
            pronoun = "its"
            if actor.gender == "female":
                pronoun = "her"
            elif actor.gender == "male":
                pronoun = "him"
            elif actor.gender == "collective":
                pronoun = "their"
        else:
            pronoun = "it"
            if actor.gender == "female":
                pronoun = "she"
            elif actor.gender == "male":
                pronoun = "he"
            elif actor.gender == "collective":
                pronoun = "they"

    return pronoun


def generateHintForRelName(ansList):
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


def replenishHintsB(actor, char):
    hintTemplateB = []

    hintTemplateB.extend([" What kind of relationship do you think they have?",
                          " So, what do you think is their relationship with each other?",
                          " What is their relationship to each other then?",
                          " What can their relationship be?",
                          " So, what do you think is their relationship?",
                          " What are they to each other?",
                          " So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?"
                          ])

    return hintTemplateB


def generateHintForRelRel(ansList):
    actor, rel, char = ansList
    hintChoices = []
    hintTemplateA = []
    hintTemplateC = []

    hintTemplateC.extend([" Who can " + char.name.title() + " be to " + actor.name.title() + "?",
                          " So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?"
                          ])

    if [x for x in rel if x == "classmate"] or rel == "classmate":
        hintTemplateA.extend([
            actor.name.title() + " and " + char.name.title() + " go to the same school.",
            actor.name.title() + " and " + char.name.title() + " are being taught by the same teacher.",
            actor.name.title() + " and " + char.name.title() + " attend the same classes."
        ])

        hintTemplateB = replenishHintsB(actor, char)

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintTemplateB.remove(r)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "friend"] or rel == "friend":
        hintTemplateA.extend([
            actor.name.title() + " and " + char.name.title() + " talk to each other sometimes. Maybe they are a little more than acquaintances?",
            actor.name.title() + " and " + char.name.title() + " can even become best friends if they spend more time together.",
            actor.name.title() + " likes to talk to " + char.name.title() + "."
        ])

        hintTemplateB = replenishHintsB(actor, char)

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintTemplateB.remove(r)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "best friend"] or rel == "best friend":
        hintTemplateA.extend([
            actor.name.title() + " and " + char.name.title() + " are always together. Maybe they are a little more than friends?",
            actor.name.title() + " and " + char.name.title() + " go to school together.",
            actor.name.title() + " and " + char.name.title() + " even share items."
        ])

        hintTemplateB = replenishHintsB(actor, char)

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintTemplateB.remove(r)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "father"] or rel == "father":
        hintTemplateA.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house.",
            actor.name.title() + " and " + char.name.title() + " are relatives.",
            char.name.title() + " provides for " + actor.name.title() + "'s needs."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "daughter"] or rel == "daughter":
        hintTemplateA.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house.",
            actor.name.title() + " and " + char.name.title() + " are relatives.",
            actor.name.title() + " loves " + char.name.title() + " very much."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "brother"] or rel == "brother":
        hintTemplateA.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house.",
            actor.name.title() + " and " + char.name.title() + " have the same surname!",
            char.name.title() + " and " + actor.name.title() + " are relatives."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "sister"] or rel == "sister":
        hintTemplateA.extend([
            actor.name.title() + " and " + char.name.title() + " live in the same house.",
            actor.name.title() + " and " + char.name.title() + " have the same surname!",
            char.name.title() + " and " + actor.name.title() + " are relatives."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "teacher"] or rel == "teacher":
        hintTemplateA.extend([
            actor.name.title() + " respects " + char.name.title() + " very much. Maybe they also see each other at school.",
            actor.name.title() + " learns a lot from listening to " + char.name.title() + ".",
            "you can consider " + char.name.title() + " as " + actor.name.title() + "'s second mother."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "student"] or rel == "student":
        hintTemplateA.extend([
            char.name.title() + " respects " + actor.name.title() + " very much. Maybe they also see each other at school.",
            char.name.title() + " learns a lot from listening to " + actor.name.title() + ".",
            "you can consider " + actor.name.title() + " as " + char.name.title() + "'s second mother."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "neighbor"] or rel == "neighbor":
        hintTemplateA.extend([
            char.name.title() + " and " + actor.name.title() + " live in the same neighborhood.",
            actor.name.title() + " lives near " + char.name.title() + ".",
            "there is a possibility that " + actor.name.title() + "'s and " + char.name.title() + "'s houses are only beside each other!"
        ])

        hintTemplateB = replenishHintsB(actor, char)

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintTemplateB.remove(r)

            hintChoices.append(hints + r)

    return hintChoices


def generateHintForLocation(ansList):
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
            "the name of the place where " + actor.name.title() + " " + action + " is composed of " + str(
                wordCount) + " " + words + ".",
            "the name of the place where " + actor.name.title() + " " + action + " has the letter " + loc[2] + "."])

    return hintChoices


def generateHintForAppProp(ansList):
    actor, prop = ansList
    hintChoices = []
    temp = []

    print("prop: ", prop)
    for items in prop:
        if "not" in items:
            cont = (items, WordNet.getSimilarAdjList(items, negator="not"))
            temp.append(cont)
        else:
            cont = (items, WordNet.getSimilarAdjList(items, negator=None))
            temp.append(cont)

    for entries in temp:
        adj, synonyms = entries

        for synonym in synonyms:
            if synonym != adj:
                hintChoices.append(
                    "I think it's because " + actor.name.title() + " is __. The word in the blank starts with " + adj[
                        0] + " and its synonym is " + synonym + ". Can you complete the sentence?")

    return hintChoices


def generatePumpForAppProp(ansList):
    actor, prop = ansList
    hintChoices = []

    hintChoices.extend([
        "I think it's related to " + actor.name.title() + "'s appearance. Can you describe " + actor.name.title() + "'s appearance?"])

    return hintChoices


def generatePromptForAppProp(correctAnswer):
    actor, prop = correctAnswer
    hintChoices = []
    randTemplateA = []
    randTemplateB = []

    randTemplateA.extend(["What makes a person " + prop + "?",
                          "Do you know anyone who is " + prop + "?"])

    randTemplateB.extend([" Can you give me some examples?",
                          " What makes them " + prop + "? Can you describe?"])

    for hints in randTemplateB:
        r = random.choice(randTemplateA)
        randTemplateA.remove(r)

        hintChoices.append(r + hints)

    return hintChoices


def generatePromptForAttr(ansList, correctAnswer):
    actor, act, attr, propType, prop = ansList
    actorAns, propAns = correctAnswer
    pronoun = producePronoun(actor)
    hintChoices = []

    hintChoices.extend(
        [
            " related to the " + propType + " of the " + attr.name + " " + actor.name.title() + " " + act + ". Say something about " + actor.name.title() + "'s " + attr.name + ".",
            "Why do you think will a person become " + propAns + " because of the " + attr.name + " " + pronoun + " " + act + "?",
            "Do you know anyone who is " + propAns + "? What is the " + propType + " of the " + attr.name + " they " + act + "?"
        ])

    return hintChoices


def generateElabForAttr(ansList):
    actor, act, attr, propType, prop = ansList
    pronoun = producePronoun(actor)
    propDefs = []

    if type(prop) is list and propType == "appearance":
        for properties in prop:
            propDefs.append(WordNet.getDefinition(properties))

    else:
        propDefs.append(WordNet.getDefinition(prop))

    hintChoices = []

    hintChoices.extend([" related to the " + attr.name + " " + actor.name.title() + " " + act + ". Since " +
                        pronoun + " " + act + " " + attr.name + " that is " + random.choice(propDefs) + ". "])

    return hintChoices


def replenishHintsC(actor):
    hintTemplateC = []

    hintTemplateC.extend(["I think the role of " + actor.name.title() + " in the story",
                          "I think " + actor.name.title() + "'s role in the story"])

    return hintTemplateC


def generateHintForType(ansList):
    actor, charType = ansList
    hintTemplateA = []
    hintTemplateB = []
    hintChoices = []

    hintTemplateA.extend([" What do you think is the word?",
                          " So, can you guess the word?",
                          " Can you give me the correct word to describe " + actor.name.title() + "'s role?",
                          " What is the role of " + actor.name.title() + " in the story?"
                          ])

    for entries in charType:
        wordCount = len(entries)
        wordCount = str(wordCount)

        if wordCount == 1:
            letter = " letter"
        else:
            letter = " letters"

        definition = WordNet.getDefinition(entries)
        if definition:
            hintTemplateB.append(" is a word that means " + definition + ".")

        hintTemplateB.extend([" is a word that starts with " + entries[:1] + " and has " + wordCount + letter + ".",
                              " is a word that has the letter " + entries[2] + " and has " + wordCount + letter + "."
                              ])

    hintTemplateC = replenishHintsC(actor)

    for hints in hintTemplateB:
        if not hintTemplateC:
            hintTemplateC = replenishHintsC(actor)

        r = random.choice(hintTemplateC)
        s = random.choice(hintTemplateA)

        hintTemplateC.remove(r)

        hintChoices.append(r + hints + s)

    return hintChoices


def generateElabForItem(ansList):
    causeList = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    act, attr, event = actor.queryAttribute(None, item.name, None)
    cause_event = ref.queryRelations(event, "cause")

    if cause_event:
        if type(cause_event) is list:
            for evs in cause_event:
                temp = []

                sent = assembleSentence(evs, attr, genType="sentence")
                if type(sent) is list:
                    for entries in sent:
                        temp.append(entries)
                else:
                    temp.append(sent)

                for entries in temp:
                    causeList.append(entries)
        else:
            temp = []

            sent = assembleSentence(cause_event, attr, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

    for entries in causeList:
        hintChoices.append(
            "because " + entries + ", " + actor.name.title() + "'s " + item.name + " look a certain way.")

    return hintChoices


def generatePumpForItem(ansList):
    events = []
    hintTemplateA = []
    hintTemplateB = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    act, attr, event = actor.queryAttribute(None, item.name, None)
    cause_event = ref.queryRelations(event, "cause")
    pronoun = producePronoun(actor, genType="objPro")

    if type(attr) is not str:
        attr = attr.name

    hintTemplateA.extend(
        [" So, what do you think is the appearance of " + actor.name.title() + "'s " + attr + "?",
         " What does " + actor.name.title() + "'s " + attr + " look like?"])

    if cause_event:
        if type(cause_event) is list:
            for evs in cause_event:
                events.append(ref.queryLookup(evs))
        else:
            events.append(ref.queryLookup(cause_event))

    for evs in events:
        event, actor, qType = evs

        hintTemplateB.extend(
            ["the reason why " + actor + "'s " + attr + " look like that is related to "
             + pronoun + " " + qType + "."])

    for hints in hintTemplateB:
        r = random.choice(hintTemplateA)

        hintChoices.append(hints + r)

    return hintChoices


def generateElabForAppearance(ansList):
    reasonList = []
    causeList = []
    hintChoices = []
    actor, out_prop = ansList
    pronoun_obj = producePronoun(actor, genType="objPro")

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "appearance", None)
        reason_event = ref.queryRelations(event, "reason")
        cause_event = ref.queryRelations(event, "cause")

        if reason_event:
            def_prop = WordNet.getDefinition(props)
            if type(reason_event) is list:
                for reasons in reason_event:
                    temp = (def_prop, reasons)
                    reasonList.append(temp)
            else:
                temp = (def_prop, reason_event)
                reasonList.append(temp)

        if cause_event:
            def_prop = WordNet.getDefinition(props)
            if type(cause_event) is list:
                for causes in cause_event:
                    temp = (def_prop, causes)
                    causeList.append(temp)
            else:
                temp = (props, cause_event)
                causeList.append(temp)

    if reasonList:
        for causes in reasonList:
            temp = []
            def_prop, event = causes
            sent = assembleSentence(event, out_prop, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append(
                        "you should describe " + actor.name.title() + "'s appearance. " + entries + " because " + pronoun_obj + " appearance is " +
                        def_prop + ".")

    if causeList:
        for causes in causeList:
            def_prop, event = causes
            sent = assembleSentence(event, out_prop, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append(
                        "since " + actor.name.title() + "'s appearance is " + def_prop + ", " + entries + ".")

    temp = []
    actor, out_prop = ansList
    for props in out_prop:
        ans_props, event = actor.queryProperty(props, "appearance", None)
        sent = assembleSentence(event, ans_props, genType="sentence")

        def_prop = WordNet.getDefinition(props)

        if type(sent) is list:
            for entries in sent:
                temp.append(entries)
        else:
            temp.append(sent)

        for entries in temp:
            if def_prop:
                hintChoices.append(
                    entries + " because " + actor.name.title() + "'s appearance is " + def_prop
                    + ". Describe " + actor.name.title() + "'s appearance.")

    return hintChoices


def generatePromptForAppearance(ansList):
    reasonList = []
    causeList = []
    hintChoices = []
    actor, out_prop = ansList
    pronoun_obj = producePronoun(actor, genType="objPro")

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "appearance", None)
        reason_event = ref.queryRelations(event, "reason")
        cause_event = ref.queryRelations(event, "cause")

        if reason_event:
            if type(reason_event) is list:
                for reasons in reason_event:
                    temp = (props, reasons)
                    reasonList.append(temp)
            else:
                temp = (props, reason_event)
                reasonList.append(temp)

        if cause_event:
            if type(cause_event) is list:
                for causes in cause_event:
                    temp = (props, causes)
                    causeList.append(temp)
            else:
                temp = (props, cause_event)
                causeList.append(temp)

    if reasonList:
        for causes in reasonList:
            hintTemplateA = []
            hintTemplateB = []

            out_prop, event = causes
            results = assembleSentence(event, out_prop, genType="sentence", turnType="prompt", ansType="appearance")
            sent = results[0]
            results.remove(sent)

            hintTemplateA.extend([" because of " + pronoun_obj + " appearance"])

            hintTemplateB.extend(results)

            i = 0
            length = len(hintTemplateB)
            while i < length:
                s = random.choice(hintTemplateB)
                hintTemplateB.remove(s)

                if hintTemplateA:
                    r = random.choice(hintTemplateA)
                    hintTemplateA.remove(r)
                    hintChoices.append(sent + r + s)

                else:
                    hintChoices.append(sent + s)

                i = i + 1

    return hintChoices


def generatePumpForAppearance(ansList):
    causeList = []
    hintChoices = []
    hintTemplateA = []
    hintTemplateB = []
    actor, out_prop = ansList

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "appearance", None)
        cause_event = ref.queryRelations(event, "reason")

        if cause_event:
            if type(cause_event) is list:
                for causes in cause_event:
                    temp = (props, causes)
                    causeList.append(temp)
            else:
                temp = (props, cause_event)
                causeList.append(temp)

    if causeList:
        for causes in causeList:
            out_prop, event = causes
            results = assembleSentence(event, out_prop, genType="sentence", turnType="pump", ansType="appearance")
            sent = results[0]
            results.remove(sent)

            hintTemplateB.extend([" Can you describe " + actor.name.title() + "'s appearance?",
                                  " Tell me about " + actor.name.title() + "'s appearance."])

            hintTemplateA.extend(results)

            i = 0
            length = len(hintTemplateA)
            while i < length:
                r = random.choice(hintTemplateA)
                hintTemplateA.remove(r)

                if hintTemplateB:
                    s = random.choice(hintTemplateB)
                    hintTemplateB.remove(s)
                    hintChoices.append(sent + r + s)

                else:
                    hintChoices.append(sent + r)

                i = i + 1

    return hintChoices


def generateElabForPersonality(ansList):
    reasonList = []
    causeList = []
    hintChoices = []
    actor, out_prop = ansList
    pronoun_obj = producePronoun(actor, genType="objPro")

    # if type(out_prop) is list:
    #    for items in out_prop

    print("out_prop: ", out_prop)

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "personality", None)
        reason_event = ref.queryRelations(event, "reason")
        cause_event = ref.queryRelations(event, "cause")

        if reason_event:
            def_prop = WordNet.getDefinition(props)
            if type(reason_event) is list:
                for reasons in reason_event:
                    temp = (def_prop, reasons)
                    reasonList.append(temp)
            else:
                temp = (def_prop, reason_event)
                reasonList.append(temp)

        if cause_event:
            def_prop = WordNet.getDefinition(props)
            if type(cause_event) is list:
                for causes in cause_event:
                    temp = (def_prop, causes)
                    causeList.append(temp)
            else:
                temp = (def_prop, cause_event)
                causeList.append(temp)

    if reasonList:
        for causes in reasonList:
            temp = []
            def_prop, event = causes
            sent = assembleSentence(event, out_prop, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append(
                        "you should describe " + actor.name.title() + "'s personality. " + entries + " because "
                        + pronoun_obj + " personality is " + def_prop + ".")

    if causeList:
        for causes in causeList:
            temp = []
            def_prop, event = causes
            sent = assembleSentence(event, out_prop, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append([
                        "Since " + actor.name.title() + "'s personality is " + def_prop + ", " + entries + ".",
                        "I think " + actor.name.title() + "'s personality is " + def_prop + ", " + entries + ". Describe "
                        + actor.name.title() + "'s personality."
                    ])

    temp = []

    for props in out_prop:
        def_prop = WordNet.getDefinition(props)

        if def_prop:
            hintChoices.append(
                "I think " + actor.name.title() + "'s personality is " + def_prop + ". Describe "
                + actor.name.title() + "'s personality.")

    return hintChoices


def generatePromptForPersonality(ansList):
    reasonList = []
    causeList = []
    hintChoices = []
    actor, out_prop = ansList
    pronoun_obj = producePronoun(actor, genType="objPro")

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "personality", None)
        print(actor.perProp)
        reason_event = ref.queryRelations(event, "reason")
        cause_event = ref.queryRelations(event, "cause")

        if reason_event:
            if type(reason_event) is list:
                for reasons in reason_event:
                    temp = (props, reasons)
                    reasonList.append(temp)
            else:
                temp = (props, reason_event)
                reasonList.append(temp)

        if cause_event:
            if type(cause_event) is list:
                for causes in cause_event:
                    temp = (props, causes)
                    causeList.append(temp)
            else:
                temp = (props, cause_event)
                causeList.append(temp)

    if reasonList:
        for causes in reasonList:
            hintTemplateA = []
            hintTemplateB = []

            out_prop, event = causes
            sent = assembleSentence(event, out_prop, genType="sentence")

            ans_prop = formatMultipleItems(out_prop)

            hintTemplateA.extend(
                [". So maybe what causes " + pronoun_obj + " to be " + ans_prop + " has something to do with " +
                 pronoun_obj + " personality.",
                 " because of " + pronoun_obj + " personality. "
                 ])

            hintTemplateB.extend([" What is the personality of someone who is " + ans_prop + "?",
                                  " What about " + actor.name.title() + "'s personality makes " + pronoun_obj
                                  + " " + ans_prop + "?"])

            i = 0
            while i < 2:
                r = random.choice(hintTemplateA)
                s = random.choice(hintTemplateB)
                hintTemplateB.remove(s)

                hintChoices.append(sent + r + s)

                i = i + 1

            hintTemplateA.clear()

    return hintChoices


def generatePumpForPersonality(ansList):
    causeList = []
    hintChoices = []
    hintTemplateA = []
    hintTemplateB = []
    actor, out_prop = ansList
    pronoun_obj = producePronoun(actor, genType="objPro")

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "personality", None)
        cause_event = ref.queryRelations(event, "reason")

        if cause_event:
            if type(cause_event) is list:
                for causes in cause_event:
                    temp = (props, causes)
                    causeList.append(temp)
            else:
                temp = (props, cause_event)
                causeList.append(temp)

    if causeList is not None:
        for causes in causeList:
            out_prop, event = causes
            sent = assembleSentence(causes, out_prop, genType="sentence")
            ans_prop = formatMultipleItems(out_prop)

            hintTemplateB.extend([" What is the personality of someone who is " + ans_prop + "?",
                                  " Can you describe " + actor.name.title() + "'s personality?"])

            hintTemplateA.extend([" " + actor.name.title() + " is "
                                  + ans_prop + " because of " + pronoun_obj + " personality.",
                                  sent + " and " + pronoun_obj + " personality is the reason."])

            i = 0
            while i < 2:
                r = random.choice(hintTemplateA)
                s = random.choice(hintTemplateB)
                hintTemplateB.remove(s)

                hintChoices.append(r + s)
                i = i + 1

    return hintChoices
