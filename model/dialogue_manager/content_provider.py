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

    if state is None and act is not None:
        # output = act
        print("action: ", act[0])

    elif act is None and state is not None:
        event, actor, qType = ref.queryLookup(event)

        cause_event = ref.queryRelations(event, "cause")

        print("cause_event: ", cause_event)

        if cause_event is not None:
            for evs in cause_event:
                causeList.append(assembleSentence(evs, state[0]))

                # if len(causeList) > 1:
                #     return "; ".join(causeList[:-1]) + " and " + causeList[len(causeList) - 1]
                #
                # elif len(causeList) == 1:
                #     return causeList[0]

        print("causeList: ", causeList)
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


def assembleSentence(event, answer):
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

        return "state", [actor, out_state, answer]

    elif qType == "action":
        act, obj, scene = actor.queryAction(None, event)

        out_obj = formatMultipleItems(obj)

        # output = "Because " + actor.name.title() + " " + action[0] + " " + out_obj

        return "action", [actor, act[0], out_obj, answer]

    elif qType == "desire":
        des, obj, scene = actor.queryDesire(None, event)

        out_obj = formatMultipleItems(obj)

        # output = "Because " + actor.name.title() + " desired to " + des[0] + " " + out_obj

        return "desire", [actor, des[0], out_obj, answer]

    elif qType == "feeling":
        feel, obj, scene = actor.queryFeeling(None, event)

        out_obj = formatMultipleItems(obj)

        # output = "Because " + actor.name.title() + " felt " + des[0] + " towards " + out_obj

        return "feeling", [actor, feel[0], out_obj, answer]

    elif qType == "attribute":
        act, attr, scene = actor.queryAttribute(None, None, event)

        if type(attr) is str:
            propType, out_prop = assembleProp(attr, scene + "ext")

            return "attribute", [actor, act[0], attr, propType, out_prop, answer]

        elif type(attr) is list:
            temp = []
            for items in attr:
                propType, out_prop = assembleProp(attr, scene + "ext")
                temp.append(actor, act[0], attr, propType, out_prop, answer)

            return "attribute", temp

        else:
            propType, out_prop = assembleProp(attr, scene + "ext")

            return "attribute", [actor, act[0], attr, propType, out_prop, answer]

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
            return "perProperty", [actor, out_prop, answer]

    elif qType == "purpose":
        try:
            act, obj, scene = actor.queryPurpose(None, None, event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemPurpose")

        return "purpose", [actor, act[0], obj, answer]

    return "unknown", None


def producePronoun(actor):
    pronoun = "it"
    if actor.gender:
        if actor.gender == "female":
            pronoun = "she"
        elif actor.gender == "male":
            pronoun = "he"

    return pronoun


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


def generateHintsForRelRel(ansList):
    actor, rel, char = ansList
    hintChoices =  []
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
        [" related to the " + propType + " of the " + attr.name + " " + actor.name.title() + " " + act + ". Say something about " + actor.name.title() + "'s " + attr.name + ".",
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


def generateHintsForType(ansList):
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
