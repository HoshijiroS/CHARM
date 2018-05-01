import random
import re

import distance

import model.externals.wordnet as WordNet
import model.story_world.classes.Item as item_type
import model.story_world.entities as Entity
import model.story_world.story_scenes as ref
from model.conjugator import conjugator
from nltk.corpus import wordnet as wordnet


def formatMultipleItems(listAnswer):
    out = ""

    try:
        if len(listAnswer) > 1 and type(listAnswer) is list:
            out = ", ".join(listAnswer[:-1]) + " and " + listAnswer[len(listAnswer) - 1]
    except Exception as e:
        print("Error in formatMultipleItems: ", e)

    if type(listAnswer) is str:
        out = listAnswer

    elif type(listAnswer) is item_type.Item:
        out = listAnswer.name

    else:
        out = listAnswer[0]

    return out


def determinePossessiveForm(actor):
    poss = "'s "

    try:
        if actor.gender == "collective":
            poss = "' "
    except Exception as e:
        print("Error on determinePossessive: ", e)

    return poss


def determineVerbForm(actor, verb, tense):
    if wordnet.synsets(verb, 'v'):
        try:
            if actor.gender == "collective":
                if tense == "present":
                    return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PRESENT_TENSE)
                else:
                    return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PAST_TENSE)

            else:
                if tense == "present":
                    return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PRESENT_TENSE)
                else:
                    return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PAST_TENSE)
        except Exception as e:
            print("Error in determineVerb: ", e)

        if actor.name.endswith('s'):
            if tense == "present":
                return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PRESENT_TENSE)
            else:
                return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PAST_TENSE)

        if tense == "present":
            return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PRESENT_TENSE)
        else:
            return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PAST_TENSE)

    return verb


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
            return whyQuestion(Entity.charList[names[val[0]]], action, item)

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

        # output = actor.name + " is a " + output

        return "type", [actor, charType]

    elif person is None and relationship is not None:
        # output = actor.name + poss + relationship + " is " + char.name.title()
        # print(actor.name + poss + relationship + " is " + char.name.title())
        return "relationship_name", [actor, relationship, char]

    elif relationship is None and person is not None:
        # output = char.name.title() + " is " + actor.name + poss + out_rel

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
                if type(properties[0]) is list and len(properties[0]) > 1:
                    prop.extend(properties[0])
                else:
                    prop.append(properties[0])

        elif propType == "amount":
            for properties in item.amtProp:
                if type(properties[0]) is list and len(properties[0]) > 1:
                    prop.extend(properties[0])
                else:
                    prop.append(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

        if propType == "appearance":
            if type(item) is str:
                item = item.name
            else:
                item = item.name
            # output = actor.name + poss + item.name + " is " + out_prop

            return "item_appearance", [actor, act, item, prop]
        else:
            # output = actor.name + " has " + out_prop + " " + item.name

            return "item_amount", [actor, act, item, prop]

    elif actor and propType:
        prop = []
        if propType == "appearance":
            for properties in actor.appProp:
                if type(properties[0]) is list and len(properties[0]) > 1:
                    prop.extend(properties[0])
                else:
                    prop.append(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

                # output = actor.name + "'s appearance is " + out_prop

            return "actor_appearance", [actor, prop]

        elif propType == "personality":
            for properties in actor.perProp:
                if type(properties[0]) is list and len(properties[0]) > 1:
                    prop.extend(properties[0])
                else:
                    prop.append(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

                # output = actor.name + "'s personality is " + out_prop

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
        action = determineVerbForm(actor, action[0], "past")

        if type(location) is str:
            # output = actor.name + " " + action[0] + " in " + loc

            return "location", [actor, action, loc]
        else:
            # output = actor.name + " " + action[0] + " in " + loc.name

            return "location", [actor, action, loc.name]

    else:  # output = "I don't know"
        return "unknown", None


def whyQuestion(actor, action, item):
    act, obj, act_event = actor.queryAction(action, item, None)
    state, state_event = actor.queryState(action, None)
    answer = ""

    causeList = []

    cause_event = None

    if state is None and act is not None:
        ans_event, actor, qType = ref.queryLookup(act_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = act[0]
        cause_event = ref.queryRelations(ans_event, "cause")

    elif act is None and state is not None:
        ans_event, actor, qType = ref.queryLookup(state_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = state[0]
        cause_event = ref.queryRelations(ans_event, "cause")

    propType = None
    prop = None

    if cause_event:
        if type(cause_event) is list:
            for evs in cause_event:
                if act:
                    #if type(obj) is item_type.Item:
                    #    propType, prop = assembleProp(obj, evs + "ext")
                    #temp = (actor, answer, obj, propType, prop)
                    temp = (actor, answer, obj, propType, prop)
                else:
                    temp = (actor, answer)
                container = assembleSentence(evs, answer=temp)
                if type(container) is list:
                    for entries in container:
                        if entries[1]:
                            causeList.append(entries)
                else:
                    print("container: ", container)
                    if container[1]:
                        causeList.append(container)
        else:
            if act:
                temp = (actor, answer, obj, propType, prop)
            else:
                temp = (actor, answer)
            container = assembleSentence(cause_event, answer=temp)
            if type(container) is list:
                for entries in container:
                    if entries[1]:
                        causeList.append(entries)
            else:
                if container[1]:
                    causeList.append(container)

                # if len(causeList) > 1:
                #     return "; ".join(causeList[:-1]) + " and " + causeList[len(causeList) - 1]
                #
                # elif len(causeList) == 1:
                #     return causeList[0]

        return "cause", causeList

    return "unknown", None


def assembleProp(attr, in_event):
    print("attribute in assembleProp: ", attr)
    print("event in assemble: ", in_event)
    appProp, event = attr.queryProperty(None, "appearance", in_event)
    amtProp, event = attr.queryProperty(None, "amount", in_event)
    perProp, event = attr.queryProperty(None, "personality", in_event)

    print("appProp, perProp, amtProp: ", appProp, amtProp, perProp)

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


def assembleSentence(event, genType=None, turnType=None, ansType=None, relType=None, answer=None):
    actor = ""
    qType = ""
    try:
        event, actor, qType = ref.queryLookup(event)
    except Exception as e:
        print("Error on assembleSentence on queryLookup: ", e)

    try:
        actor = Entity.charList[actor.lower()]
    except Exception as e:
        print("Error on assembleSentence on actor assignment: ", e)

    try:
        actor = Entity.itemList[actor.lower()]
    except Exception as e:
        print("Error on assembleSentence on item assignment: ", e)

    try:
        actor = Entity.locList[actor.lower()]
    except Exception as e:
        print("Error on assembleSentence on location assignment: ", e)

    pronoun_obj = producePronoun(actor, genType="objPro")
    poss = determinePossessiveForm(actor)

    verb = "is"

    try:
        if actor.gender == "collective":
            verb = "were"
        else:
            verb = "was"
    except Exception as e:
        print("Error in gender assembleSentence: ", e)

    if qType == "state":
        state, scene = actor.queryState(None, event)
        out_state = []

        if type(state[0]) is list:
            for states in state[0]:
                out_state.append(determineVerbForm(actor, states, "past"))
        else:
            out_state.append(determineVerbForm(actor, state[0], "past"))
        sent_state = formatMultipleItems(out_state)

        container = []
        if genType == "sentence":
            container.append(actor.name + " " + verb + " " + sent_state)

            if turnType == "prompt":
                container.extend([container[0] + " because of " + actor.name + poss +
                                  ansType + ". What is the " + ansType + " of " + actor.name.title + "?",
                                  container[0] + ". What about " + actor.name + poss + sent_state + " affected "
                                  + pronoun_obj + " " + ansType + "?",
                                  ])

                return container

            elif turnType == "pump":
                container.extend([
                    container[0] + ". What is the " + ansType + " of someone who is " + state + "?",
                    container[0] + ". Can you describe " + actor.name + poss + ansType + "?",
                    container[0] + ". Tell me about " + actor.name + poss + ansType + "."
                ])

                return container

            return container[0]

        if answer:
            return "state", [actor, state, answer]

        return "state", [actor, state]

    elif qType == "action":
        out_act, obj, scene = actor.queryAction(None, None, event)

        sent_act = []
        if type(out_act[0]) is list:
            for states in out_act[0]:
                sent_act.append(determineVerbForm(actor, states, "past"))
        else:
            sent_act.append(determineVerbForm(actor, out_act[0], "past"))
        act = formatMultipleItems(sent_act)

        out_obj = formatMultipleItems(obj)

        sentence_prop = out_obj
        prop = None
        propType = None

        if type(obj) is item_type.Item:
            propType, prop = assembleProp(obj, scene + "ext")

        if prop:
            output_prop = formatMultipleItems(prop)

        if propType == "appearance" or propType == "personality":
            sentence_prop = out_obj + " that is " + output_prop

        if propType == "amount":
            sentence_prop = output_prop + " " + out_obj

        container = []
        if genType == "sentence":
            container.append(actor.name + " " + act + " " + sentence_prop)

            if turnType == "prompt":
                hintTemplateA = []
                hintTemplateB = []

                if relType == "reason":
                    hintTemplateA.extend(
                        [container[0] + ". So maybe what causes " + pronoun_obj + " to " + act + " " + sentence_prop
                         + " has something to do with " + pronoun_obj + " " + ansType + ".",
                         container[0] + " and " + pronoun_obj + " " + ansType + " is the reason."
                         ])

                    res_prop = actor.perProp
                    out_prop = []
                    for items in res_prop:
                        out_prop.extend(items[0])

                    sent_prop = formatMultipleItems(out_prop)
                    if sent_prop and ansType == "personality":
                        hintTemplateB.append(" What is the " + ansType + " of someone who " + act
                                             + " a person who is " + sent_prop + "?")

                    hintTemplateB.extend([" What about " + actor.name + poss + ansType
                                          + " makes " + pronoun_obj + " " + act + " " + sentence_prop + "?"])

                else:
                    hintTemplateA.extend([
                        "maybe what causes " + pronoun_obj + " to " + act + " " + sentence_prop
                        + " has something to do with " + pronoun_obj + " " + ansType + " since " + container[0] + ".",
                        actor.name + poss + ansType + " causes " + pronoun_obj + " to " + act + " "
                        + sentence_prop + "."
                    ])

                    res_prop = actor.perProp
                    out_prop = []
                    for items in res_prop:
                        out_prop.extend(items[0])

                    sent_prop = formatMultipleItems(out_prop)
                    if sent_prop and ansType == "personality":
                        hintTemplateB.append(" What is the " + ansType + " of someone who " + act
                                             + " a person who is " + sent_prop + "?")

                    hintTemplateB.extend([" What about " + actor.name + poss + ansType
                                          + " makes " + pronoun_obj + " " + act + " " + sentence_prop + "?"])

                for hints in hintTemplateA:
                    if hintTemplateB:
                        r = random.choice(hintTemplateB)
                        hintTemplateB.remove(r)
                        container.append(hints + r)
                    else:
                        container.append(hints)

                return container

            elif turnType == "pump":
                hintTemplateA = []
                hintTemplateB = []

                if relType == "reason":
                    hintTemplateB.extend(
                        [" What is the " + ansType + " of someone who is " + act + " " + sentence_prop + "?",
                         " Can you describe " + actor.name + poss + ansType + "?",
                         " Tell me about " + actor.name + poss + ansType + "."
                         ])

                    hintTemplateA.extend([container[0] + " and " + actor.name + " " + act + " " + sentence_prop
                                          + " because of " + pronoun_obj + " " + ansType + ".",
                                          container[
                                              0] + " and " + pronoun_obj.title() + " " + ansType + " is the reason."])

                else:
                    hintTemplateB.extend(
                        [" What is the " + ansType + " of someone who is " + act + " " + sentence_prop + "?",
                         " Can you describe " + actor.name + poss + ansType + "?"])

                    hintTemplateA.extend([actor.name + " " + act + " " + sentence_prop
                                          + " because of " + pronoun_obj + " " + ansType + ".",
                                          actor.name + poss + ansType + " is the reason why " + container[
                                              0] + "."])

                for hints in hintTemplateB:
                    r = random.choice(hintTemplateA)
                    container.append(r + hints)

                return container

            return container[0]

        if answer:
            return "action", [actor, out_act, out_obj, propType, prop, answer]

        return "action", [actor, out_act, out_obj, propType, prop]

    elif qType == "desire":
        out_des, obj, scene = actor.queryDesire(None, None, event)

        sent_des = []
        if type(out_des[0]) is list:
            for states in out_des[0]:
                sent_des.append(states)
        else:
            sent_des.append(out_des[0])
        des = formatMultipleItems(sent_des)

        out_obj = formatMultipleItems(obj)

        container = []
        if genType == "sentence":
            container.append(actor.name + " desired to " + des + " " + out_obj)

            if turnType == "prompt":
                hintTemplateA = []
                hintTemplateB = []

                if relType == "reason":
                    hintTemplateA.extend(
                        [container[0] + ". So maybe what causes " + pronoun_obj + " to desire to " + des + " " + out_obj
                         + " has something to do with " + pronoun_obj + " " + ansType + ".",
                         container[0] + " and " + pronoun_obj + " " + ansType + " is the reason."
                         ])

                    res_prop = actor.perProp
                    out_prop = []
                    for items in res_prop:
                        out_prop.extend(items[0])

                    sent_prop = formatMultipleItems(out_prop)
                    if sent_prop and ansType == "personality":
                        hintTemplateB.append(" What is the " + ansType + " of someone who desires to " + des
                                             + " a person who is " + sent_prop + "?")

                    hintTemplateB.extend([" What about " + actor.name + poss + ansType
                                          + " makes " + pronoun_obj + " desire to " + des + " " + out_obj + "?"])

                else:
                    hintTemplateA.extend([
                        "maybe what causes " + pronoun_obj + " to desire to " + des + " " + out_obj
                        + " has something to do with " + pronoun_obj + " " + ansType + " since " + container[0] + ".",
                        actor.name + poss + ansType + " causes " + pronoun_obj + " to desire to " + des + " "
                        + out_obj + "."
                    ])

                    res_prop = actor.perProp
                    out_prop = []
                    for items in res_prop:
                        out_prop.extend(items[0])

                    sent_prop = formatMultipleItems(out_prop)
                    if sent_prop and ansType == "personality":
                        hintTemplateB.append(" What is the " + ansType + " of someone who desires to " + des
                                             + " a person who is " + sent_prop + "?")

                    hintTemplateB.extend([" What about " + actor.name + poss + ansType
                                          + " makes " + pronoun_obj + " desire to " + des + " " + out_obj + "?"])

                for hints in hintTemplateA:
                    if hintTemplateB:
                        r = random.choice(hintTemplateB)
                        hintTemplateB.remove(r)
                        container.append(hints + r)
                    else:
                        container.append(hints)

                return container

            elif turnType == "pump":
                hintTemplateA = []
                hintTemplateB = []

                if relType == "reason":
                    hintTemplateB.extend(
                        [" What is the " + ansType + " of someone who desires to " + des + " " + out_obj + "?",
                         " Can you describe " + actor.name + poss + ansType + "?",
                         " Tell me about " + actor.name + poss + ansType + "."])

                    hintTemplateA.extend(
                        [container[0] + " and " + actor.name + " desires to " + des + " " + out_obj
                         + " because of " + pronoun_obj + " " + ansType + ".",
                         container[
                             0] + " and " + pronoun_obj.title() + " " + ansType + " is the reason."])

                else:
                    hintTemplateB.extend(
                        [" What is the " + ansType + " of someone who desires to " + des + " " + out_obj + "?",
                         " Can you describe " + actor.name + poss + ansType + "?"])

                    hintTemplateA.extend([actor.name + " desires to " + des + " " + out_obj
                                          + " because of " + pronoun_obj + " " + ansType + ".",
                                          actor.name + poss + ansType + " is the reason why " + container[
                                              0] + "."])

                for hints in hintTemplateB:
                    r = random.choice(hintTemplateA)
                    container.append(r + hints)

                return container

            return container[0]

        if answer:
            return "desire", [actor, out_des, out_obj, answer]

        return "desire", [actor, out_des, out_obj]

    elif qType == "attribute":
        act, out_attr, scene = actor.queryAttribute(None, None, event)

        sent_act = determineVerbForm(actor, act[0], "present")

        attr = ""
        out_prop = None
        propType = None

        if type(out_attr) is str:
            try:
                attr = Entity.itemList[out_attr.lower()]
            except Exception as e:
                print("Error on assembleSentence attribute: ", e)

            propType, out_prop = assembleProp(attr, scene + "ext")

            print("scene + ext: ", scene + "ext")
            print("item appearance attributes: ", attr.appProp)
            print("item personality attributes: ", attr.perProp)
            print("item amount attributes: ", attr.amtProp)
            print("out_prop: ", out_prop)

        elif type(out_attr) is item_type.Item:
            propType, out_prop = assembleProp(out_attr, scene + "ext")

            print("scene + ext: ", scene + "ext")
            print("item appearance attributes: ", out_attr.appProp)
            print("item personality attributes: ", out_attr.perProp)
            print("item amount attributes: ", out_attr.amtProp)
            print("out_prop: ", out_prop)

            attr = out_attr.name

        if out_prop and (propType == "appearance" or propType == "personality"):
            sent_prop = formatMultipleItems(out_prop)
            sent_add = " that is "
        else:
            sent_prop = ""
            sent_add = ""

        container = []
        if genType == "sentence":
            if propType == "amount":
                container.append(actor.name + " " + sent_act + " " + sent_prop + " " + attr)
            else:
                container.append(actor.name + " " + sent_act + " " + attr + sent_add + sent_prop)

            if turnType == "prompt":
                hintTemplateA = []
                hintTemplateB = []

                if propType != "amount":
                    hintTemplateB.extend([" So, what is the " + ansType + " of someone who " + sent_act
                                          + " " + out_prop + " " + attr + "?",
                                          " Do you know anyone who also " + sent_act + " " + out_prop
                                          + " " + attr + "? What is their " + ansType + " like?"
                                          ])
                else:
                    hintTemplateB.extend([" So, what is the " + ansType + " of someone who has " + out_prop + " "
                                          + attr + "?",
                                          " Do you know anyone who also has " + out_prop + " "
                                          + attr + "? What is their " + ansType + " like?"
                                          ])

                if relType == "reason":
                    hintTemplateA.extend([container[0] + " because of " + actor.name + poss + ansType + ".",
                                          container[
                                              0] + " and I think it has something to do with " + actor.name
                                          + poss + ansType + "."])

                else:
                    hintTemplateA.extend([actor.name + " has a certain " + ansType + " because "
                                          + container[0] + ".",
                                          "because " + container[0] + ", " + actor.name + poss
                                          + ansType + " is a certain way."])

                for hints in hintTemplateB:
                    if hintTemplateA:
                        r = random.choice(hintTemplateA)
                        hintTemplateA.remove(r)
                        container.append(r + hints)
                    else:
                        container.append(container[0] + "." + hints)

                return container

            elif turnType == "pump":
                hintTemplateA = []
                hintTemplateB = []

                hintTemplateB.extend([" Can you tell me about " + actor.name + poss + ansType + "?",
                                      " Describe " + actor.name + poss + ansType + ".",
                                      " Tell me about " + actor.name + poss + ansType + "."
                                      ])

                if relType == "reason":
                    hintTemplateA.extend([actor.name + poss + ansType + " is caused by "
                                          + container[0] + ".",
                                          container[0] + " so " + actor.name + poss + ansType
                                          + " must be affected."
                                          ])
                else:
                    hintTemplateA.extend([container[0] + " is because of " + actor.name + poss
                                          + ansType + ".",
                                          container[0] + "."])

                for hints in hintTemplateB:
                    if hintTemplateA:
                        r = random.choice(hintTemplateA)
                        hintTemplateA.remove(r)
                        container.append(r + hints)
                    else:
                        container.append(container[0] + "." + hints)

                return container

            return container[0]

        if answer:
            return "attribute", [actor, act, attr, propType, out_prop, answer]

        return "attribute", [actor, act, attr, propType, out_prop]

    elif qType == "actor_appearance":
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

            container = []
            if genType == "sentence":
                container.append(actor.name + " looks " + out_prop)

                if turnType == "prompt":
                    hintTemplateA = []
                    hintTemplateB = []
                    hintTemplateA.extend(
                        [" Do you know anyone who is " + out_prop + "? What is their " + ansType + "?",
                         " What is the " + ansType + " of someone who is " + out_prop + "?",
                         " What about " + actor.name + "'s appearance affects " + pronoun_obj
                         + " " + ansType + "?"
                         ])

                    if relType == "reason":
                        hintTemplateB.extend(
                            [container[0],
                             container[0] + ". So maybe what causes " + pronoun_obj + " to be " + out_prop
                             + " has something to do with " + pronoun_obj + " " + ansType + "."
                             ])

                    else:
                        hintTemplateB.extend([
                            actor.name + poss + ansType + " is caused by " + pronoun_obj
                            + " " + out_prop + " appearance.",
                            "maybe " + actor.name + poss + ansType
                            + " has something to do with " + pronoun_obj + " " + out_prop + " appearance."
                        ])

                    for hints in hintTemplateA:
                        if hintTemplateB:
                            r = random.choice(hintTemplateB)
                            hintTemplateB.remove(r)
                            container.append(r + hints)
                        else:
                            container.append(container[0] + "." + hints)

                    return container

                elif turnType == "pump":
                    hintTemplateA = []
                    hintTemplateB = []

                    hintTemplateB.extend([" Tell me about " + actor.name + poss + ansType + ".",
                                          " Can you describe " + + actor.name + poss + ansType + "?",
                                          " Tell me about " + actor.name + poss + ansType + "."])

                    if relType == "reason":
                        hintTemplateA.extend(["What is the " + ansType + " of someone who is " + out_prop + "?",
                                              " and " + pronoun_obj.title() + " " + ansType + " is the reason."])
                    else:
                        hintTemplateA.extend(["What is the " + ansType + " of someone who is " + out_prop + "?",
                                              actor.name + poss + ansType + " causes " + pronoun_obj + " to be "
                                              + out_prop + "."])

                    for hints in hintTemplateB:
                        if hintTemplateA:
                            r = random.choice(hintTemplateA)
                            hintTemplateA.remove(r)
                            container.append(r + hints)
                        else:
                            container.append(hints)

                    return container

                return container[0]

            if answer:
                return "actor_appearance", [actor, prop, answer]

            return "actor_appearance", [actor, prop]

    elif qType == "actor_personality":
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
                container.append(actor.name + " is " + out_prop)

                if turnType == "prompt":
                    hintTemplateA = []
                    hintTemplateB = []
                    hintTemplateA.extend(
                        [" Do you know anyone who is " + out_prop + "? What is their " + ansType + "?",
                         " What is the " + ansType + " of someone who is " + out_prop + "?",
                         " What about " + actor.name + "'s personality makes " + pronoun_obj
                         + " " + ansType + "?"
                         ])

                    if relType == "reason":
                        hintTemplateB.extend(
                            [container[0],
                             container[0] + ". So maybe what causes " + pronoun_obj + " to be " + out_prop
                             + " has something to do with " + pronoun_obj + " " + ansType + "."
                             ])

                    else:
                        hintTemplateB.extend([
                            actor.name + poss + ansType + " is caused by " + pronoun_obj
                            + " " + out_prop + " personality.",
                            "maybe " + actor.name + poss + ansType
                            + " has something to do with " + pronoun_obj + " " + out_prop + " personality."
                        ])

                    for hints in hintTemplateA:
                        if hintTemplateB:
                            r = random.choice(hintTemplateB)
                            hintTemplateB.remove(r)
                            container.append(r + hints)
                        else:
                            container.append(container[0] + hints)

                    return container

                elif turnType == "pump":
                    hintTemplateA = []
                    hintTemplateB = []

                    hintTemplateB.extend([" Say something about " + actor.name + poss + ansType + ".",
                                          " Can you describe " + + actor.name + poss + ansType + "?",
                                          " Tell me about " + actor.name + poss + ansType + "."])

                    if relType == "reason":
                        hintTemplateA.extend(
                            [container[0] + ". What is the " + ansType + " of someone who is " + out_prop + "?",
                             container[0] + " and " + pronoun_obj.title() + " " + ansType + " is the reason."])
                    else:
                        hintTemplateA.extend(
                            [container[0] + ". What is the " + ansType + " of someone who is " + out_prop + "?",
                             actor.name + poss + ansType + " causes " + pronoun_obj + " to be "
                             + out_prop + "."])

                    for hints in hintTemplateB:
                        if hintTemplateA:
                            r = random.choice(hintTemplateA)
                            hintTemplateA.remove(r)
                            container.append(r + hints)
                        else:
                            container.append(hints)

                    return container

                return container[0]

            if answer:
                return "actor_personality", [actor, prop, answer]

            return "actor_personality", [actor, prop]

    # elif qType == "item_appearance":
    #
    # elif qType == "item_amount":

    elif qType == "purpose":
        out_act = ""
        out_obj = ""
        try:
            out_act, out_obj, scene = actor.queryPurpose(None, None, event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemPurpose")

        sent_act = []
        if type(out_act[0]) is list:
            for states in out_act[0]:
                sent_act.append(determineVerbForm(actor, states, "past"))
        else:
            sent_act.append(determineVerbForm(actor, out_act[0], "past"))

        act = formatMultipleItems(sent_act)

        container = []
        if genType == "sentence":
            container.append(actor.name + " " + act + " " + out_obj)

            if turnType == "prompt":
                hintTemplateA = []
                hintTemplateB = []

                if relType == "reason":
                    hintTemplateA.extend(
                        [container[0] + ". So maybe what causes " + pronoun_obj + " to " + act + " " + out_obj
                         + " has something to do with " + pronoun_obj + " " + ansType + ".",
                         container[0] + " and " + pronoun_obj + " " + ansType + " is the reason."
                         ])

                    res_prop = actor.perProp
                    out_prop = []
                    for items in res_prop:
                        out_prop.extend(items[0])

                    sent_prop = formatMultipleItems(out_prop)
                    if sent_prop and ansType == "personality":
                        hintTemplateB.append(" What is the " + ansType + " of something that " + act
                                             + " a person who is " + sent_prop + "?")

                    hintTemplateB.extend([" What about " + actor.name + poss + ansType
                                          + " makes " + pronoun_obj + " " + act + " " + out_obj + "?"])

                else:
                    hintTemplateA.extend([
                        "maybe what causes " + pronoun_obj + " to " + act + " " + out_obj
                        + " has something to do with " + pronoun_obj + " " + ansType + " since " + container[0] + ".",
                        actor.name + poss + ansType + " causes " + pronoun_obj + " to " + act + " "
                        + out_obj + "."
                    ])

                    res_prop = actor.perProp
                    out_prop = []
                    for items in res_prop:
                        out_prop.extend(items[0])

                    sent_prop = formatMultipleItems(out_prop)
                    if sent_prop and ansType == "personality":
                        hintTemplateB.append(" What is the " + ansType + " of something that " + act
                                             + " a person who is " + sent_prop + "?")

                    hintTemplateB.extend([" What about " + actor.name + poss + ansType
                                          + " makes " + pronoun_obj + " " + act + " " + out_obj + "?"])

                for hints in hintTemplateA:
                    if hintTemplateB:
                        r = random.choice(hintTemplateB)
                        hintTemplateB.remove(r)
                        container.append(hints + r)
                    else:
                        container.append(hints)

                return container

            elif turnType == "pump":
                hintTemplateA = []
                hintTemplateB = []

                if relType == "reason":
                    hintTemplateB.extend(
                        [" What is the " + ansType + " of something that " + act + " " + out_obj + "?",
                         " Can you describe " + actor.name + poss + ansType + "?",
                         " Tell me about " + actor.name + poss + ansType + "."])

                    hintTemplateA.extend([container[0] + " and " + actor.name + " " + act + " " + out_obj
                                          + " because of " + pronoun_obj + " " + ansType + ".",
                                          container[
                                              0] + " and " + pronoun_obj.title() + " " + ansType + " is the reason."])

                else:
                    hintTemplateB.extend(
                        [" What is the " + ansType + " of something that " + act + " " + out_obj + "?",
                         " Can you describe " + actor.name + poss + ansType + "?"])

                    hintTemplateA.extend([actor.name + " " + act + " " + out_obj
                                          + " because of " + pronoun_obj + " " + ansType + ".",
                                          actor.name + poss + ansType + " is the reason why " + container[
                                              0] + "."])

                for hints in hintTemplateB:
                    r = random.choice(hintTemplateA)
                    container.append(r + hints)

                return container

            return container[0]

        if answer:
            return "purpose", [actor, out_act, out_obj, answer]

        return "purpose", [actor, out_act, out_obj]

    elif qType == "location":
        out_act = ""
        loc = ""
        try:
            out_act, loc, scene = actor.queryLocation(None, None, event)
        except Exception as e:
            a = 1
            # print("Error: ", e, " on ", time, " itemPurpose")

        act = determineVerbForm(actor, out_act[0], "past")

        if type(loc) is str:
            loc = loc
        else:
            loc = loc.name

        if genType == "sentence":
            return actor.name + " " + act + " at " + loc

        if answer:
            return "location", [actor, out_act, loc, answer]

        return "location", [actor, out_act, loc]

    return "unknown", None


def producePronoun(actor, genType=None):
    pronoun = ""

    if genType == "objPro":
        pronoun = "its"

        try:
            if actor.gender == "female":
                pronoun = "her"
            elif actor.gender == "male":
                pronoun = "him"
            elif actor.gender == "collective":
                pronoun = "their"
        except Exception as e:
            print("Error in producePronoun: ", e)
    else:
        pronoun = "it"

        try:
            if actor.gender == "female":
                pronoun = "she"
            elif actor.gender == "male":
                pronoun = "he"
            elif actor.gender == "collective":
                pronoun = "they"
        except Exception as e:
            print("Error in producePronoun: ", e)

    return pronoun


def generateHintForRelName(ansList):
    actor, rel, char = ansList

    wordCount = len(char[0].name.split())
    if wordCount == 1:
        words = "word"
    else:
        words = "words"

    poss = determinePossessiveForm(actor)

    hintChoices = [
        "the first name of " + actor.name + poss + rel + " starts with " + char[0].name[:1] + ".",
        "the name of " + actor.name + poss + rel + " is composed of " + str(wordCount) + " " + words + ".",
        "the first name of " + actor.name + poss + rel + " has the letter " + char[0].name[2] + "."]

    return hintChoices


def replenishHintsB(actor, char):
    hintTemplateB = []

    hintTemplateB.extend([" What kind of relationship do you think they have?",
                          " So, what do you think is their relationship with each other?",
                          " What is their relationship to each other then?",
                          " What can their relationship be?",
                          " So, what do you think is their relationship?",
                          " What are they to each other?",
                          " So, what do you think is the relationship of " + char.name.title() + " to " + actor.name + "?"
                          ])

    return hintTemplateB


def generateHintForRelRel(ansList):
    actor, rel, char = ansList
    hintChoices = []
    hintTemplateA = []
    hintTemplateC = []

    poss = determinePossessiveForm(actor)

    hintTemplateC.extend([" Who can " + char.name.title() + " be to " + actor.name + "?",
                          " So, what do you think is the relationship of " + char.name.title() + " to " + actor.name + "?"
                          ])

    if [x for x in rel if x == "classmate"] or rel == "classmate":
        hintTemplateA.extend([
            actor.name + " and " + char.name.title() + " go to the same school.",
            actor.name + " and " + char.name.title() + " are being taught by the same teacher.",
            actor.name + " and " + char.name.title() + " attend the same classes."
        ])

        hintTemplateB = replenishHintsB(actor, char)

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintTemplateB.remove(r)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "friend"] or rel == "friend":
        hintTemplateA.extend([
            actor.name + " and " + char.name.title() + " talk to each other sometimes. Maybe they are a little more than acquaintances?",
            actor.name + " and " + char.name.title() + " can even become best friends if they spend more time together.",
            actor.name + " likes to talk to " + char.name.title() + "."
        ])

        hintTemplateB = replenishHintsB(actor, char)

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintTemplateB.remove(r)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "best friend"] or rel == "best friend":
        hintTemplateA.extend([
            actor.name + " and " + char.name.title() + " are always together. Maybe they are a little more than friends?",
            actor.name + " and " + char.name.title() + " go to school together.",
            actor.name + " and " + char.name.title() + " even share items."
        ])

        hintTemplateB = replenishHintsB(actor, char)

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintTemplateB.remove(r)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "father"] or rel == "father":
        hintTemplateA.extend([
            actor.name + " and " + char.name.title() + " live in the same house.",
            actor.name + " and " + char.name.title() + " are relatives.",
            char.name.title() + " provides for " + actor.name + poss + "needs."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "daughter"] or rel == "daughter":
        hintTemplateA.extend([
            actor.name + " and " + char.name.title() + " live in the same house.",
            actor.name + " and " + char.name.title() + " are relatives.",
            actor.name + " loves " + char.name.title() + " very much."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "brother"] or rel == "brother":
        hintTemplateA.extend([
            actor.name + " and " + char.name.title() + " live in the same house.",
            actor.name + " and " + char.name.title() + " have the same surname!",
            char.name.title() + " and " + actor.name + " are relatives."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "sister"] or rel == "sister":
        hintTemplateA.extend([
            actor.name + " and " + char.name.title() + " live in the same house.",
            actor.name + " and " + char.name.title() + " have the same surname!",
            char.name.title() + " and " + actor.name + " are relatives."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "teacher"] or rel == "teacher":
        hintTemplateA.extend([
            actor.name + " respects " + char.name.title() + " very much. Maybe they also see each other at school.",
            actor.name + " learns a lot from listening to " + char.name.title() + ".",
            "you can consider " + char.name.title() + " as " + actor.name + poss + "second mother."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "student"] or rel == "student":
        hintTemplateA.extend([
            char.name.title() + " respects " + actor.name + " very much. Maybe they also see each other at school.",
            char.name.title() + " learns a lot from listening to " + actor.name + ".",
            "you can consider " + actor.name + " as " + char.name.title() + poss + "second mother."
        ])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateC)

            hintChoices.append(hints + r)

    if [x for x in rel if x == "neighbor"] or rel == "neighbor":
        hintTemplateA.extend([
            char.name.title() + " and " + actor.name + " live in the same neighborhood.",
            actor.name + " lives near " + char.name.title() + ".",
            "there is a possibility that " + actor.name + "'s and " + char.name.title() + poss + "houses are only beside each other!"
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

    temp = Entity.locList[loc.name.lower()].appProp
    if temp:
        for properties in temp:
            hintChoices.append(
                "the place where " + actor.name + action + " is " + properties + ".")

    else:
        wordCount = len(loc.split())
        if wordCount == 1:
            words = "word"
        else:
            words = "words"

        hintChoices.extend([
            "the name of the place where " + actor.name + " " + action + " starts with " + loc[:1] + ".",
            "the name of the place where " + actor.name + " " + action + " is composed of " + str(
                wordCount) + " " + words + ".",
            "the name of the place where " + actor.name + " " + action + " has the letter " + loc[2] + "."])

    return hintChoices


def generateHintForAppProp(ansList):
    actor, prop = ansList
    hintChoices = []
    temp = []

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
                    "I think it's because " + actor.name + " is __. The word in the blank starts with " + adj[
                        0] + " and its synonym is " + synonym + ". Can you complete the sentence?")

    return hintChoices


def generatePumpForAppProp(ansList):
    actor, prop = ansList
    hintChoices = []

    poss = determinePossessiveForm(actor)

    hintChoices.extend([
        "I think it's related to " + actor.name + poss + "appearance. Can you describe " + actor.name + poss + "appearance?"])

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

    basic = act
    act = determineVerbForm(actor, act, "present")
    poss = determinePossessiveForm(actor)

    hintChoices.extend(
        [
            "I think it's related to the " + propType + " of the " + attr + " " + actor.name + " " + act + ". Say something about " + actor.name + poss + attr + ".",
            "Why do you think will a person become " + propAns + " because of the " + attr + " " + pronoun + " " + act + "? What is with their " + attr + "?",
            "Do you know anyone who is " + propAns + "? What is the " + propType + " of the " + attr + " they " + basic + "?"
        ])

    return hintChoices


def generateElabForAttr(ansList):
    actor, act, attr, propType, prop = ansList
    pronoun = producePronoun(actor)
    propDefs = []

    act = determineVerbForm(actor, act, "present")

    if type(prop) is list and propType == "appearance":
        for properties in prop:
            propDefs.append(WordNet.getDefinition(properties))

    else:
        propDefs.append(WordNet.getDefinition(prop))

    hintChoices = []

    hintChoices.extend(["I think it's related to the " + attr + " " + actor.name + " " + act + ". Since " +
                        pronoun + " " + act + " " + attr + " that is " + random.choice(propDefs) + ". "])

    return hintChoices


def replenishHintsC(actor):
    hintTemplateC = []

    poss = determinePossessiveForm(actor)

    hintTemplateC.extend(["I think the role of " + actor.name + " in the story",
                          "I think " + actor.name + poss + "role in the story"])

    return hintTemplateC


def generateHintForType(ansList):
    actor, charType = ansList
    hintTemplateA = []
    hintTemplateB = []
    hintChoices = []

    poss = determinePossessiveForm(actor)

    hintTemplateA.extend([" What do you think is the word?",
                          " So, can you guess the word?",
                          " Can you give me the correct word to describe " + actor.name + poss + "role?",
                          " What is the role of " + actor.name + " in the story?"
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
    act, attr, event = actor.queryAttribute(None, item, None)
    cause_event = ref.queryRelations(event, "cause")
    reason_event = ref.queryRelations(event, "reason")

    act = determineVerbForm(actor, act[0], "present")
    if cause_event:
        if type(cause_event) is list:
            for evs in cause_event:
                sent = assembleSentence(evs, genType="sentence")
                if type(sent) is list:
                    for entries in sent:
                        causeList.append(entries)
                else:
                    causeList.append(sent)

        else:
            sent = assembleSentence(cause_event, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    causeList.append(entries)
            else:
                causeList.append(sent)

    if reason_event:
        if type(reason_event) is list:
            for evs in reason_event:
                sent = assembleSentence(evs, genType="sentence")
                if type(sent) is list:
                    for entries in sent:
                        causeList.append(entries)
                else:
                    causeList.append(sent)

        else:
            sent = assembleSentence(reason_event, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    causeList.append(entries)
            else:
                causeList.append(sent)

    look = determineVerbForm(actor, "look", "present")

    for entries in causeList:
        hintChoices.append(
            "I think it's because " + entries + ", the " + item + " " + actor.name + " " + act + " " + look + " a certain way.")

    return hintChoices


def generatePumpForItem(ansList):
    events = []
    hintTemplateA = []
    hintTemplateB = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    act, attr, event = actor.queryAttribute(None, item, None)
    cause_event = ref.queryRelations(event, "cause")
    pronoun = producePronoun(actor, genType="objPro")

    poss = determinePossessiveForm(actor)
    look = determineVerbForm(actor, "look", "present")

    if type(attr) is not str:
        attr = attr.name

    hintTemplateA.extend(
        [" So, what do you think is the appearance of " + actor.name + poss + attr + "?",
         " What does " + actor.name + poss + attr + " " + look + " like?"])

    if cause_event:
        if type(cause_event) is list:
            for evs in cause_event:
                events.append(ref.queryLookup(evs))
        else:
            events.append(ref.queryLookup(cause_event))

    for evs in events:
        event, actor, qType = evs

        hintTemplateB.extend(
            ["I think the reason why " + actor + poss + attr + " " + look + " like that is related to "
             + pronoun + " " + qType + "."])

    for hints in hintTemplateA:
        r = random.choice(hintTemplateB)

        hintChoices.append(r + hints)

    return hintChoices


def generateElabForAppearance(ansList):
    reasonList = []
    causeList = []
    hintChoices = []
    actor, out_prop = ansList
    pronoun_obj = producePronoun(actor, genType="objPro")
    poss = determinePossessiveForm(actor)

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
            sent = assembleSentence(event, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append(
                        "you should describe " + actor.name + poss + "appearance. " + entries + " because " + pronoun_obj + " appearance is " +
                        def_prop + ".")

    if causeList:
        for causes in causeList:
            def_prop, event = causes
            sent = assembleSentence(event, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append(
                        "since " + actor.name + poss + "appearance is " + def_prop + ", " + entries + ".")

    temp = []
    actor, out_prop = ansList
    for props in out_prop:
        ans_props, event = actor.queryProperty(props, "appearance", None)
        sent = assembleSentence(event, genType="sentence")

        def_prop = WordNet.getDefinition(props)

        if type(sent) is list:
            for entries in sent:
                temp.append(entries)
        else:
            temp.append(sent)

        for entries in temp:
            if def_prop:
                hintChoices.append(
                    entries + " because " + actor.name + poss + "appearance is " + def_prop
                    + ". Describe " + actor.name + poss + "appearance.")

    return hintChoices


def generatePromptForAppearance(ansList):
    reasonList = []
    hintChoices = []
    actor, out_prop = ansList

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "appearance", None)
        reason_event = ref.queryRelations(event, "reason")

        if reason_event:
            if type(reason_event) is list:
                for reasons in reason_event:
                    temp = (props, reasons)
                    reasonList.append(temp)
            else:
                temp = (props, reason_event)
                reasonList.append(temp)

    if reasonList:
        for reason in reasonList:
            out_prop, event = reason
            results = assembleSentence(event, genType="sentence", turnType="prompt", ansType="appearance",
                                       relType="reason")
            sent = results[0]
            results.remove(sent)

            hintChoices.extend(results)

    return hintChoices


def generatePumpForAppearance(ansList):
    reasonList = []
    hintChoices = []
    actor, out_prop = ansList

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "appearance", None)
        reason_event = ref.queryRelations(event, "reason")

        if reason_event:
            if type(reason_event) is list:
                for causes in reason_event:
                    temp = (props, causes)
                    reasonList.append(temp)
            else:
                temp = (props, reason_event)
                reasonList.append(temp)

    if reasonList:
        for reason in reasonList:
            out_prop, event = reason
            results = assembleSentence(event, genType="sentence", turnType="pump", ansType="appearance",
                                       relType="reason")
            sent = results[0]
            results.remove(sent)

            hintChoices.extend(results)


def generateElabForPersonality(ansList):
    reasonList = []
    causeList = []
    hintChoices = []
    actor, out_prop = ansList
    pronoun_obj = producePronoun(actor, genType="objPro")

    # if type(out_prop) is list:
    #    for items in out_prop

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
            sent = assembleSentence(event, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append(
                        "you should describe " + actor.name + "'s personality. " + entries + " because "
                        + pronoun_obj + " personality is " + def_prop + ".")

    if causeList:
        for causes in causeList:
            temp = []
            def_prop, event = causes
            sent = assembleSentence(event, genType="sentence")

            if type(sent) is list:
                for entries in sent:
                    temp.append(entries)
            else:
                temp.append(sent)

            for entries in temp:
                if def_prop:
                    hintChoices.append([
                        "Since " + actor.name + "'s personality is " + def_prop + ", " + entries + ".",
                        "I think " + actor.name + "'s personality is " + def_prop + ", " + entries + ". Describe "
                        + actor.name + "'s personality."
                    ])

    for props in out_prop:
        def_prop = WordNet.getDefinition(props)

        if def_prop:
            hintChoices.append(
                "I think " + actor.name + "'s personality is " + def_prop + ". Describe "
                + actor.name + "'s personality.")

    return hintChoices


def generatePromptForPersonality(ansList):
    reasonList = []
    causeList = []
    hintChoices = []
    actor, out_prop = ansList

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "personality", None)
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
                for reason in cause_event:
                    temp = (props, reason)
                    causeList.append(temp)
            else:
                temp = (props, cause_event)
                causeList.append(temp)

    if reasonList:
        for reason in reasonList:
            out_prop, event = reason
            results = assembleSentence(event, genType="sentence", turnType="prompt", ansType="personality",
                                       relType="reason")
            sent = results[0]
            results.remove(sent)

            hintChoices.extend(results)

    if causeList:
        for cause in causeList:
            out_prop, event = cause
            results = assembleSentence(event, genType="sentence", turnType="prompt", ansType="personality",
                                       relType="cause")
            sent = results[0]
            results.remove(sent)

            hintChoices.extend(results)

    return hintChoices


def generatePumpForPersonality(ansList):
    causeList = []
    reasonList = []
    hintChoices = []
    actor, out_prop = ansList

    for props in out_prop:
        ans_prop, event = actor.queryProperty(props, "personality", None)
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
        for reason in reasonList:
            out_prop, event = reason
            results = assembleSentence(event, genType="sentence", turnType="pump", ansType="personality",
                                       relType="reason")
            sent = results[0]
            results.remove(sent)

            hintChoices.extend(results)

    if causeList:
        for cause in causeList:
            out_prop, event = cause
            results = assembleSentence(event, genType="sentence", turnType="prompt", ansType="personality",
                                       relType="cause")
            sent = results[0]
            results.remove(sent)

            hintChoices.extend(results)

    return hintChoices


def generatePromptForActs(ansList):
    hintChoices = []
    hintTemplateA = []
    hintTemplateB = []
    actionWord = ""

    for entries in ansList:
        ansType, answers = entries
        ans_actor = answers[0]

        actor = ""
        action = ""
        obj = ""
        propType = None
        prop = None

        if len(answers[len(answers) - 1]) == 5:
            actor, action, obj, propType, prop = answers[len(answers) - 1]
        elif len(answers[len(answers) - 1]) == 2:
            actor, action = answers[len(answers) - 1]

        if type(obj) is item_type.Item:
            obj = obj.name

        obj = formatMultipleItems(obj)
        print("obj in generatePromptForActs: ", obj)

        sent_ans_actor = ans_actor.name
        sent_actor = actor.name

        poss = determinePossessiveForm(ans_actor)
        ans_act = determineVerbForm(actor, action, "past")
        pres_ans_act = determineVerbForm(actor, action, "present")
        have = determineVerbForm(ans_actor, "have", "present")

        if ansType == "action":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "pastt")

        elif ansType == "desire":
            actionWord = "what " + sent_ans_actor + " desired to " + answers[1][0]

        elif ansType == "state" or ansType == "location":
            actionWord = sent_ans_actor + poss + ansType

        elif ansType == "actor_appearance":
            actionWord = sent_ans_actor + poss + "appearance"

        elif ansType == "actor_personality":
            actionWord = sent_ans_actor + poss + "personality"

        elif ansType == "attribute":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "present")

        elif ansType == "item_appearance":
            actionWord = "the appearance of " + sent_ans_actor + " items"

        elif ansType == "item_amount":
            actionWord = "the amount of items " + sent_ans_actor + " " + have

        elif ansType == "location":
            actionWord = sent_ans_actor + poss + "location"

        resForChar = ""
        resForItem = ""

        if obj != "":
            try:
                resForChar = Entity.charList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                resForItem = Entity.itemList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            if prop:
                prop = formatMultipleItems(prop)

            if propType == "appearance" or propType == "personality":
                obj = " that is " + prop

            elif propType == "amount":
                obj = prop + " " + obj

            else:
                obj = " " + obj

        if resForChar != "":
            resForChar = " someone"

        if resForChar == "" and obj != "":
            resForItem = " something"

        hintTemplateA.extend([" What causes a person to " + pres_ans_act + resForChar + resForItem + "? Can you tell me?",
                              " Do you know anyone who has " + pres_ans_act + resForChar + resForItem + " before? What happened?",
                              " What is something that could make you " + pres_ans_act + resForChar + resForItem + "? Maybe that also made "
                              + sent_actor + " " + pres_ans_act + obj + "."])

        hintTemplateB.extend([sent_actor + " " + ans_act + obj + " because of "
                              + actionWord + "."])

        for hints in hintTemplateB:
            r = random.choice(hintTemplateA)
            hintTemplateA.remove(r)
            hintChoices.append(hints + r)

        hintTemplateA = []
        hintTemplateB = []

    return hintChoices


def generatePumpForActs(ansList):
    hintChoices = []
    hintTemplateA = []
    hintTemplateB = []
    actionWord = ""

    for entries in ansList:
        ansType, answers = entries
        print("answers: ", answers)
        ans_actor = answers[0]
        print("answers[len]: ", answers[len(answers) - 1])

        print("length: ", len(answers[len(answers) - 1]))

        actor = ""
        action = ""
        obj = ""
        propType = None
        prop = None

        if len(answers[len(answers) - 1]) == 5:
            actor, action, obj, propType, prop = answers[len(answers) - 1]
        elif len(answers[len(answers) - 1]) == 2:
            actor, action = answers[len(answers) - 1]

        if type(obj) is item_type.Item:
            obj = obj.name

        obj = formatMultipleItems(obj)
        print("obj in generatePumpForActs: ", obj)

        if obj != "":
            if prop:
                prop = formatMultipleItems(prop)

            if propType == "appearance" or propType == "personality":
                obj = " that is " + prop

            elif propType == "amount":
                obj = prop + " " + obj

            else:
                obj = " " + obj

        sent_ans_actor = ans_actor.name
        sent_actor = actor.name

        poss = determinePossessiveForm(ans_actor)
        actor_poss = determinePossessiveForm(actor)
        ans_act = determineVerbForm(actor, action, "past")
        have = determineVerbForm(ans_actor, "have", "present")

        if ansType == "action":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "past")

        elif ansType == "desire":
            actionWord = "what " + sent_ans_actor + " desired to " + answers[1][0]

        elif ansType == "state" or ansType == "location":
            actionWord = sent_ans_actor + poss + ansType

        elif ansType == "actor_appearance":
            actionWord = sent_ans_actor + poss + "appearance"

        elif ansType == "actor_personality":
            actionWord = sent_ans_actor + poss + "personality"

        elif ansType == "attribute":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "present")

        elif ansType == "item_appearance":
            actionWord = "the appearance of " + sent_ans_actor + " items"

        elif ansType == "item_amount":
            actionWord = "the amount of items " + sent_ans_actor + " " + have

        elif ansType == "location":
            actionWord = sent_ans_actor + poss + "location"

        hintTemplateA.extend([" Can you tell me about " + actionWord + "?",
                              " How does that affect " + sent_actor + actor_poss + "actions? "])

        hintTemplateB.extend(["the reason why " + sent_actor + " " + ans_act + obj + " has something to do with " + actionWord + "."])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintChoices.append(r + hints)

        hintTemplateA = []
        hintTemplateB = []

    return hintChoices


def generateElabForActs(ansList):
    hintChoices = []

    for entries in ansList:
        ansType, answers = entries
        ans_actor = answers[0]

        actor = ""
        action = ""
        obj = ""
        propType = None
        prop = None
        ans_action = ""

        if len(answers[len(answers) - 1]) == 5:
            actor, action, obj, propType, prop = answers[len(answers) - 1]
        elif len(answers[len(answers) - 1]) == 2:
            actor, action = answers[len(answers) - 1]

        def_prop = WordNet.getDefinition(ans_action, verb="Yes")

        if type(obj) is item_type.Item:
            obj = obj.name

        obj = formatMultipleItems(obj)
        print("obj in generatePumpForActs: ", obj)

        sent_ans_actor = ans_actor.name
        sent_actor = actor.name

        poss = determinePossessiveForm(ans_actor)
        ans_act = determineVerbForm(actor, action, "past")
        pres_ans_act = determineVerbForm(actor, action, "present")
        have = determineVerbForm(ans_actor, "have", "present")

        actionWord = ""
        if ansType == "action":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "past")

        elif ansType == "desire":
            actionWord = "what " + sent_ans_actor + " desired to " + answers[1][0]

        elif ansType == "state" or ansType == "location":
            actionWord = sent_ans_actor + poss + ansType

        elif ansType == "actor_appearance":
            actionWord = sent_ans_actor + poss + "appearance"

        elif ansType == "actor_personality":
            actionWord = sent_ans_actor + poss + "personality"

        elif ansType == "attribute":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "present")

        elif ansType == "item_appearance":
            actionWord = "the appearance of " + sent_ans_actor + " items"

        elif ansType == "item_amount":
            actionWord = "the amount of items " + sent_ans_actor + " " + have

        elif ansType == "location":
            actionWord = sent_ans_actor + poss + " location"

        resForChar = ""
        resForItem = ""

        if obj != "":
            try:
                resForChar = Entity.charList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                resForItem = Entity.itemList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            if prop:
                prop = formatMultipleItems(prop)

            if propType == "appearance" or propType == "personality":
                obj = obj + " that is " + prop

            elif propType == "amount":
                obj = prop + " " + obj

            else:
                obj = " " + obj

        if resForChar != "":
            resForChar = " a person"

        if resForChar == "" and obj != "":
            resForItem = " an item"

        if def_prop:
            hintChoices.append(
                sent_actor + " " + ans_act + obj + " because of " + actionWord + ". "
                + pres_ans_act.title() + " means " + def_prop + resForChar + resForItem + ".")

    return hintChoices
