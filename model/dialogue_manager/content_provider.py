import random
import re
import inflect
inflect = inflect.engine()

import distance

import model.externals.wordnet as WordNet
import model.story_world.classes.Item as item_type
import model.story_world.entities as Entity
import model.story_world.story_scenes as ref
from model.conjugator import conjugator
from nltk.corpus import wordnet as wordnet
from nltk.stem import WordNetLemmatizer


def formatMultipleItems(listAnswer):
    if type(listAnswer) is list and listAnswer:
        if len(listAnswer) > 1:
            return ", ".join(listAnswer[:-1]) + " and " + listAnswer[len(listAnswer) - 1]

        else:
            return listAnswer[0]

    if type(listAnswer) is str:
        return listAnswer

    elif type(listAnswer) is item_type.Item:
        return listAnswer.name

    else:
        return listAnswer

    return None


def determinePossessiveForm(actor):
    poss = "'s "

    try:
        if actor.gender == "collective" or actor.name.endsWith("s"):
            poss = "' "
    except Exception as e:
        print("Error on determinePossessive: ", e)

    return poss


def determineVerbForm(actor, verb, tense):
    if len(wordnet.synsets(verb)) > 0 and getCommonPartOfSpeech(verb) == 'a':
        return verb

    elif len(wordnet.synsets(verb)) > 0 and getCommonPartOfSpeech(verb) == 'v':
        if type(actor) is str:
            if actor == "plural":
                if tense == "present":
                    return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PRESENT_TENSE)
                else:
                    return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PAST_TENSE)

            else:
                if tense == "present":
                    return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PRESENT_TENSE)
                else:
                    return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PAST_TENSE)

        else:
            if inflect.singular_noun(actor.name.lower()):
                if tense == "present":
                    return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PRESENT_TENSE)
                else:
                    return conjugator.conjugate(verb, number=conjugator.PLURAL, tense=conjugator.PAST_TENSE)

            else:
                if tense == "present":
                    return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PRESENT_TENSE)
                else:
                    return conjugator.conjugate(verb, number=conjugator.SINGULAR, tense=conjugator.PAST_TENSE)

    return verb


def confirmCharacter(actor, questType, person=None, relationship=None, action=None, location=None, item=None,
                     propType=None, prop=None):
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
            return whyQuestion(Entity.charList[names[val[0]]], action, item, queriedProp=prop)

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
        act, attr, scene = actor.queryAttribute(action, item, None)
    except Exception as e:
        print("error in whatQuestion: ", e)

    if action is None and attr and actor and propType:
        if propType == "appearance":
            #print("attr: ", attr.appProp)
            for properties in attr.appProp:
                if type(properties[0]) is list:
                    if len(properties[0]) > 1:
                        prop.extend(properties[0])
                    else:
                        prop.extend(properties[0])
                else:
                    prop.append(properties[0])

        elif propType == "amount":
            for properties in attr.amtProp:
                if type(properties[0]) is list:
                    if len(properties[0]) > 1:
                        prop.extend(properties[0])
                    else:
                        prop.extend(properties[0])
                else:
                    prop.append(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

        if propType == "appearance":
            # output = actor.name + poss + item.name + " is " + out_prop

            return "item_appearance", [actor, act, attr, prop]
        else:
            # output = actor.name + " has " + out_prop + " " + item.name

            return "item_amount", [actor, act, attr, prop]

    elif actor and propType and not item:
        prop = []
        if propType == "appearance":
            for properties in actor.appProp:
                if type(properties[0]) is list:
                    if len(properties[0]) > 1:
                        prop.extend(properties[0])
                    else:
                        prop.extend(properties[0])
                else:
                    prop.append(properties[0])

                # if prop is not None:
                #    out_prop = formatMultipleItems(prop)

                # output = actor.name + "'s appearance is " + out_prop

            return "actor_appearance", [actor, prop]

        elif propType == "personality":
            for properties in actor.perProp:
                if type(properties[0]) is list:
                    if len(properties[0]) > 1:
                        prop.extend(properties[0])
                    else:
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
        if type(location) is str:
            # output = actor.name + " " + action[0] + " in " + loc

            return "location", [actor, action[0], loc]
        else:
            # output = actor.name + " " + action[0] + " in " + loc.name

            return "location", [actor, action[0], loc.name]

    else:  # output = "I don't know"
        return "unknown", None


def whyQuestion(actor, action, item, queriedProp=None):
    #print("actor: ", actor, "action: ", action, "item: ", item, "queriedProp: ", queriedProp)
    act, obj, act_event = actor.queryAction(action, item, None)
    des, des_obj, des_event = actor.queryDesire(action, item, None)
    act_obj, attr, attr_event = actor.queryAttribute(action, item, None)
    state, state_event = actor.queryState(action, None)
    per_prop, per_prop_event = actor.queryProperty(queriedProp, "personality", None)
    app_prop, app_prop_event = actor.queryProperty(queriedProp, "appearance", None)

    #print("act: ", act, "state: ", state, "des: ", des, "act_obj: ", act_obj)

    answer = ""

    causeList = []

    cause_event = None

    if per_prop:
        ans_event, actor, qType = ref.queryLookup(per_prop_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = "be"
        cause_event = ref.queryRelations(ans_event, "cause")

    if app_prop:
        ans_event, actor, qType = ref.queryLookup(app_prop_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = "look"
        cause_event = ref.queryRelations(ans_event, "cause")

    if act:
        ans_event, actor, qType = ref.queryLookup(act_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = act[0]
        cause_event = ref.queryRelations(ans_event, "cause")

    if des:
        ans_event, actor, qType = ref.queryLookup(des_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = des[0]
        cause_event = ref.queryRelations(ans_event, "cause")

    elif state:
        ans_event, actor, qType = ref.queryLookup(state_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = state[0]
        cause_event = ref.queryRelations(ans_event, "cause")

    elif act_obj:
        ans_event, actor, qType = ref.queryLookup(attr_event)

        try:
            actor = Entity.charList[actor.lower()]
        except Exception as e:
            print("Error on assembleSentence on actor assignment: ", e)

        answer = act_obj[0]
        cause_event = ref.queryRelations(ans_event, "cause")

    propType = None
    prop = None

    temp = None
    if cause_event:
        if type(cause_event) is list:
            for evs in cause_event:
                if act:
                    temp = (actor, answer, obj, propType, prop)

                if des:
                    temp = (actor, answer, des_obj, propType, prop)

                if app_prop:
                    sent_app_prop = formatMultipleItems(app_prop)
                    temp = (actor, answer, sent_app_prop, None, None)

                if per_prop:
                    sent_per_prop = formatMultipleItems(per_prop)
                    temp = (actor, answer, sent_per_prop, None, None)

                if act_obj:
                    out_app_prop = attr.queryProperty(queriedProp, "appearance", None)[0]
                    out_per_prop = attr.queryProperty(queriedProp, "personality", None)[0]
                    out_amt_prop = attr.queryProperty(queriedProp, "amount", None)[0]

                    if out_app_prop:
                        temp = (actor, answer, attr, "appearance", out_app_prop)

                    if out_per_prop:
                        temp = (actor, answer, attr, "personality", out_per_prop)

                    if out_amt_prop:
                        temp = (actor, answer, attr, "amount", out_amt_prop)

                if state:
                    temp = (actor, answer)

                container = assembleSentence(evs, answer=temp)
                print("container: ", container)
                if type(container) is list:
                    for entries in container:
                        if entries[1]:
                            causeList.append(entries)
                else:
                    if container[1]:
                        causeList.append(container)

        else:
            if act:
                temp = (actor, answer, obj, propType, prop)

            if des:
                temp = (actor, answer, des_obj, propType, prop)

            if app_prop:
                sent_app_prop = formatMultipleItems(app_prop)
                temp = (actor, answer, sent_app_prop, None, None)

            if per_prop:
                sent_per_prop = formatMultipleItems(per_prop)
                temp = (actor, answer, sent_per_prop, None, None)

            if act_obj:
                out_app_prop = attr.queryProperty(queriedProp, "appearance", None)[0]
                out_per_prop = attr.queryProperty(queriedProp, "personality", None)[0]
                out_amt_prop = attr.queryProperty(queriedProp, "amount", None)[0]

                if out_app_prop:
                    temp = (actor, answer, attr, "appearance", out_app_prop)

                if out_per_prop:
                    temp = (actor, answer, attr, "personality", out_per_prop)

                if out_amt_prop:
                    temp = (actor, answer, attr, "amount", out_amt_prop)

            if state:
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

        print("causeList: ", causeList)
        return "cause", causeList

    return "unknown", None


def assembleProp(attr, in_event):
    #print("attribute in assembleProp: ", attr)
    #print("event in assemble: ", in_event)
    appProp, event = attr.queryProperty(None, "appearance", in_event)
    amtProp, event = attr.queryProperty(None, "amount", in_event)
    perProp, event = attr.queryProperty(None, "personality", in_event)

    #print("appProp, perProp, amtProp: ", appProp, amtProp, perProp)

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
    pronoun_obj = pronoun_obj.lower()
    poss = determinePossessiveForm(actor)

    if ansType == "location":
        address = actor.queryLocation(None, None, event)[2]

        if " room" in address or " row" in address or "behind " in address:
            ansType = "seat"
        else:
            ansType = "address"

    if ansType == "personality":
        ansType = "personality, financial status or description"

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
            if type(actor) is item_type.Item:
                actorName = actor.name

            else:
                if actor.gender == "collective":
                    actorName = "the " + actor.name
                else:
                    actorName = actor.name

            if len(wordnet.synsets(state[0])) > 0 and getCommonPartOfSpeech(state[0]) == 'a':
                addVerb = determineVerbForm(actor, "be", "past")
                container.append(actorName + " " + addVerb + " " + state[0])
            elif len(wordnet.synsets(state[0])) > 0 and getCommonPartOfSpeech(state[0]) == 'v':
                stateVerb = determineVerbForm(actor, state[0], "past")
                container.append(actorName + " " + stateVerb)
            else:
                addVerb = determineVerbForm(actor, "be", "past")
                container.append(actorName + " " + addVerb + " " + state[0])

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
            verb = determineVerbForm("singular", "be", "present")

            if inflect.singular_noun(out_obj.lower()):
                verb = determineVerbForm("plural", "be", "present")

            sentence_prop = out_obj + " that " + verb + " " + output_prop

        if propType == "amount":
            sentence_prop = output_prop + " " + out_obj

        container = []
        if genType == "sentence":
            if actor.gender == "collective":
                actorName = "the " + actor.name
            else:
                actorName = actor.name

            verb = determineVerbForm(actor, out_act[0], "past")

            if "not " in verb:
                verb = "did " + out_act[0]

            container.append(actorName + " " + verb + " " + sentence_prop)

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
            if actor.gender == "collective":
                actorName = "the " + actor.name
            else:
                actorName = actor.name

            container.append(actorName + " desired to " + des + " " + out_obj)

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

            #print("scene + ext: ", scene + "ext")
            #print("item appearance attributes: ", attr.appProp)
            #print("item personality attributes: ", attr.perProp)
            #print("item amount attributes: ", attr.amtProp)
            #print("out_prop: ", out_prop)

        elif type(out_attr) is item_type.Item:
            propType, out_prop = assembleProp(out_attr, scene + "ext")

            #print("scene + ext: ", scene + "ext")
            #print("item appearance attributes: ", out_attr.appProp)
            #print("item personality attributes: ", out_attr.perProp)
            #print("item amount attributes: ", out_attr.amtProp)
            #print("out_prop: ", out_prop)

            attr = out_attr.name

        if out_prop and (propType == "appearance" or propType == "personality"):
            sent_prop = formatMultipleItems(out_prop)
            verb = determineVerbForm("singular", "be", "present")

            if inflect.singular_noun(attr.lower()):
                verb = determineVerbForm("plural", "be", "present")

            sent_add = " that " + verb + " "
        else:
            sent_prop = ""
            sent_add = ""

        container = []
        if genType == "sentence":
            if actor.gender == "collective":
                actorName = "the " + actor.name
            else:
                actorName = actor.name

            if "not" in sent_act:
                sent_act = "does " + act[0]

            if propType == "amount":
                container.append(actorName + " " + sent_act + " " + sent_prop + " " + attr)
            else:
                container.append(actorName + " " + sent_act + " " + attr + sent_add + sent_prop)

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
                if actor.gender == "collective":
                    actorName = "the " + actor.name
                else:
                    actorName = actor.name

                verb = determineVerbForm(actor, "look", "present")

                container.append(actorName + " " + verb + " " + out_prop)

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

        print("genType: ", genType, "turnType: ", turnType)
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
                if actor.gender == "collective":
                    actorName = "the " + actor.name
                else:
                    actorName = actor.name

                verb = determineVerbForm(actor, "be", "present")

                container.append(actorName + " " + verb + " " + out_prop)

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

    elif qType == "item_appearance":
        prop = []

        try:
            act, attr, scene = actor.queryAttribute(None, None, event)
        except Exception as e:
            print("Error in assembleSentence item_appearance: ", e)

        if attr:
            if type(attr) is str:
                attr = Entity.itemList[attr.lower()]

            try:
                prop = attr.queryProperty(None, "appearance", scene + "ext")
            except Exception as e:
                print("Error in assembleSentence item_appearance: ", e)

        if prop:
            out_prop = formatMultipleItems(prop)

            container = []
            if genType == "sentence":
                if actor.gender == "collective":
                    actorName = "the " + actor.name
                else:
                    actorName = actor.name

                verb = determineVerbForm(actor, act, "past")
                sent_attr = attr.name

                container.append(actorName + " " + verb + " " + sent_attr + " that looks " + out_prop)

                if turnType == "prompt":
                    hintTemplateA = []
                    hintTemplateB = []
                    hintTemplateA.extend(
                        [" Do you know anyone who " + verb + " " + sent_attr + " that looks " + out_prop + "? What is their " + ansType + "?",
                         " What is the " + ansType + " of someone who " + verb + " " + sent_attr + " that looks " + out_prop + "?",
                         " What about " + actor.name + "'s " + sent_attr + " makes " + pronoun_obj
                         + " " + ansType + "?"
                         ])

                    poss = determinePossessiveForm(attr)

                    if relType == "reason":
                        hintTemplateB.extend(
                            [container[0],
                             container[0] + ". So maybe what causes " + pronoun_obj + " to "
                             + verb + " " + out_prop + " " + sent_attr + " has something to do with " + pronoun_obj + " " + ansType + "."
                             ])

                    else:
                        hintTemplateB.extend([
                            actor.name + poss + ansType + " is caused by " + pronoun_obj
                            + " " + sent_attr + poss + " appearance.",
                            "maybe " + actor.name + poss + ansType
                            + " has something to do with " + pronoun_obj + " " + sent_attr + poss + " appearance."
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

                    hintTemplateB.extend([" Say something about " + actor.name + poss + sent_attr + ".",
                                          " Can you describe " + + actor.name + poss + sent_attr + "?",
                                          " Tell me about " + actor.name + poss + sent_attr + "."])

                    if relType == "reason":
                        hintTemplateA.extend(
                            [container[0] + ". What is the " + ansType + " of someone who " + verb + " " + out_prop + " " + sent_attr + "?",
                             container[0] + " and " + pronoun_obj.title() + " " + sent_attr + " is the reason."])
                    else:
                        hintTemplateA.extend(
                            [container[0] + ". What is the " + ansType + " of someone who " + verb + " " + out_prop + " " + sent_attr + "?",
                             actor.name + poss + ansType + " causes " + pronoun_obj + " to " + verb + " " + out_prop + " " + sent_attr + "."])

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
                return "item_appearance", [actor, act, attr, prop, answer]

            return "item_appearance", [actor, act, attr, prop]

    elif qType == "item_amount":
        prop = []

        try:
            act, attr, scene = actor.queryAttribute(None, None, event)
        except Exception as e:
            print("Error in assembleSentence item_amount: ", e)

        if attr:
            if type(attr) is str:
                attr = Entity.itemList[attr.lower()]

            try:
                prop = attr.queryProperty(None, "amount", scene + "ext")
            except Exception as e:
                print("Error in assembleSentence item_amount: ", e)

        if prop:
            out_prop = formatMultipleItems(prop)

            container = []
            if genType == "sentence":
                if actor.gender == "collective":
                    actorName = "the " + actor.name
                else:
                    actorName = actor.name

                verb = determineVerbForm(actor, act, "past")
                sent_attr = attr.name

                container.append(actorName + " " + verb + " " + sent_attr + " " + out_prop)

                if turnType == "prompt":
                    hintTemplateA = []
                    hintTemplateB = []
                    hintTemplateA.extend(
                        [
                            " Do you know anyone who " + verb + " " + sent_attr + " " + out_prop + " " + sent_attr + "? What is their " + ansType + "?",
                            " What is the " + ansType + " of someone who " + verb + " " + sent_attr + " " + out_prop + " " + sent_attr + "?",
                            " What about " + actor.name + "'s " + sent_attr + " affects " + pronoun_obj
                            + " " + ansType + "?"
                            ])

                    poss = determinePossessiveForm(attr)

                    if relType == "reason":
                        hintTemplateB.extend(
                            [container[0],
                             container[0] + ". So maybe what causes " + pronoun_obj + " to "
                             + verb + " " + out_prop + " " + sent_attr + " has something to do with " + pronoun_obj + " " + ansType + "."
                             ])

                    else:
                        hintTemplateB.extend([
                            actor.name + poss + ansType + " is caused by the number of " + sent_attr + " " + pronoun_obj + " has.",
                            "maybe " + actor.name + poss + ansType
                            + " has something to do with the number of " + sent_attr + " " + pronoun_obj + " has."
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

                    hintTemplateB.extend([" Say something about " + actor.name + poss + sent_attr + ".",
                                          " Can you describe " + + actor.name + poss + sent_attr + "?",
                                          " Tell me about " + actor.name + poss + sent_attr + "."])

                    if relType == "reason":
                        hintTemplateA.extend(
                            [container[
                                 0] + ". What is the " + ansType + " of someone who " + verb + " " + out_prop + " " + sent_attr + "?",
                             container[0] + " and " + pronoun_obj.title() + " " + sent_attr + " is the reason."])
                    else:
                        hintTemplateA.extend(
                            [container[
                                 0] + ". What is the " + ansType + " of someone who " + verb + " " + out_prop + " " + sent_attr + "?",
                             actor.name + poss + ansType + " causes " + pronoun_obj + " to " + verb + " " + out_prop + " " + sent_attr + "."])

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
                return "item_amount", [actor, act, attr, prop, answer]

            return "item_amount", [actor, act, attr, prop]

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
            if inflect.singular_noun(actor.name):
                verb = determineVerbForm("plural", act, "past")
            else:
                verb = determineVerbForm("singular", act, "past")

            if "not " in verb:
                verb = "did " + out_act[0]

            container.append(actor.name + " " + verb + " " + out_obj)

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

        if type(loc) is str:
            loc = loc
        else:
            loc = loc.name

        if genType == "sentence":
            if actor.gender == "collective":
                actorName = "the " + actor.name
            else:
                actorName = actor.name

            verb = determineVerbForm(actor, out_act[0], "past")

            if "not " in verb:
                verb = "did " + out_act[0]

            return [actorName + " " + verb + " at " + loc]

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
    actor, act, loc = ansList
    wnl = WordNetLemmatizer()
    act = wnl.lemmatize(act.split("_"), 'v')
    act = determineVerbForm(actor, act[0], "present")
    hintChoices = []

    if type(loc) is str:
        temp = Entity.locList[loc.lower()].appProp
    else:
        temp = Entity.locList[loc.name.lower()].appProp

    if temp:
        for properties in temp:
            hintChoices.append(
                "the place where " + actor.name + act + " is " + properties + ".")

    else:
        wordCount = len(loc.split())
        if wordCount == 1:
            words = "word"
        else:
            words = "words"

        hintChoices.extend([
            "the name of the place where " + actor.name + " " + act + " starts with " + loc[:1] + ".",
            "the name of the place where " + actor.name + " " + act + " is composed of " + str(
                wordCount) + " " + words + ".",
            "the name of the place where " + actor.name + " " + act + " has the letter " + loc[2] + "."])

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

    wnl = WordNetLemmatizer()
    act = wnl.lemmatize(act[0].replace("_", " "), 'v')
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
    poss = determinePossessiveForm(actor)
    pronoun = producePronoun(actor)
    propDefs = []

    wnl = WordNetLemmatizer()
    act = wnl.lemmatize(act[0].replace("_", " "), 'v')
    act = determineVerbForm(actor, act, "present")

    if type(prop) is list and propType == "appearance":
        for properties in prop:
            propDefs.append(WordNet.getDefinition(properties))

    else:
        propDefs.append(WordNet.getDefinition(prop))

    verb = determineVerbForm("singular", "be", "present")

    if type(attr) is item_type.Item:
        attr = attr.name

    if inflect.singular_noun(attr.lower()):
        verb = determineVerbForm("plural", "be", "present")

    hintChoices = []

    hintChoices.extend(["I think it's related to the " + attr + " " + actor.name + " " + act + ". Since " +
                        pronoun + " " + act + " " + attr + " that " + verb + " " + random.choice(propDefs) + ". "
                        "Can you tell me more about " + actor.name + poss + attr + "?"])

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


def generateHintForItem(ansList):
    causeList = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    item = item.name
    poss = determinePossessiveForm(actor)
    act, attr, event = actor.queryAttribute(None, item, None)
    cause_event = ref.queryRelations(event, "cause")
    reason_event = ref.queryRelations(event, "reason")

    wnl = WordNetLemmatizer()
    act = wnl.lemmatize(act[0].replace("_", " "), 'v')
    act = determineVerbForm(actor, act, "present")
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

    temp = []
    for items in out_prop:
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
                    "I think since " + entries + ", the " + item + " " + actor.name + " " + act + " " + look
                    + " like a word that has the synonym " + synonym + ".")

    return hintChoices


def generateElabForItem(ansList):
    causeList = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    item = item.name
    poss = determinePossessiveForm(actor)
    act, attr, event = actor.queryAttribute(None, item, None)
    cause_event = ref.queryRelations(event, "cause")
    reason_event = ref.queryRelations(event, "reason")

    wnl = WordNetLemmatizer()
    act = wnl.lemmatize(act[0].replace("_", " "), 'v')
    act = determineVerbForm(actor, act, "present")
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

    def_prop = WordNet.getDefinition(out_prop)

    if def_prop:
        hintChoices.append(
            "I think since " + entries + ", the " + item + " " + actor.name + " " + act + " " + look +
            " " + def_prop + ". What does the " + item + " " + actor.name + " " + act + " " + look + " like?")

    return hintChoices


def generatePumpForItem(ansList):
    causeList = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    item = item.name
    poss = determinePossessiveForm(actor)
    act, attr, event = actor.queryAttribute(None, item, None)
    cause_event = ref.queryRelations(event, "cause")
    reason_event = ref.queryRelations(event, "reason")

    wnl = WordNetLemmatizer()
    act = wnl.lemmatize(act[0].replace("_", " "), 'v')
    act = determineVerbForm(actor, act, "present")
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
            "I think since " + entries + ", the " + item + " " + actor.name + " " + act + " " + look + " a certain way. "
            "Can you tell me more about " + actor.name + poss + item + "?")

    return hintChoices


def generatePromptForItem(ansList):
    events = []
    hintTemplateA = []
    hintTemplateB = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    item = item.name
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


def generatePumpForAmtItem(ansList):
    causeList = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    item = item.name
    poss = determinePossessiveForm(actor)
    act, attr, event = actor.queryAttribute(None, item, None)
    cause_event = ref.queryRelations(event, "cause")
    reason_event = ref.queryRelations(event, "reason")

    wnl = WordNetLemmatizer()
    act = wnl.lemmatize(act[0].replace("_", " "), 'v')
    act = determineVerbForm(actor, act, "present")
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

    look = determineVerbForm(actor, "be", "present")

    for entries in causeList:
        hintChoices.append(
            "I think since " + entries + ", the " + item + " " + actor.name + " " + act + " " + look + " a certain way. "
            "Can you tell me more about " + actor.name + poss + item + "?")

    return hintChoices


def generatePromptForAmtItem(ansList):
    events = []
    hintTemplateA = []
    hintTemplateB = []
    hintChoices = []
    actor, act, item, out_prop = ansList
    item = item.name
    act, attr, event = actor.queryAttribute(None, item, None)
    cause_event = ref.queryRelations(event, "cause")
    pronoun = producePronoun(actor, genType="objPro")

    poss = determinePossessiveForm(actor)
    look = determineVerbForm(actor, "be", "present")

    if type(attr) is not str:
        attr = attr.name

    hintTemplateA.extend(
        [" So, what do you think is the appearance of " + actor.name + poss + attr + "?",
         " What does " + actor.name + poss + attr + " like?"])

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
                    hintChoices.append(entries + " because " + pronoun_obj + " appearance is " +
                        def_prop + ". How can you describe " + actor.name + poss + "appearance?")

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
                        "since " + actor.name + poss + "appearance is " + def_prop + ", " + entries + ". "
                        "How can you describe " + actor.name + poss + "appearance?")

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
                    + ". How can you describe " + actor.name + poss + "appearance?")

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
    poss = determinePossessiveForm(actor)

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
                    hintChoices.append(entries + " because "
                        + pronoun_obj + " personality, financial status or description is " + def_prop + ". How can you describe " + actor.name + "?")

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
                        "Since " + actor.name + "'s personality, financial status or description is " + def_prop + ", " + entries + ". How can you describe "
                        + actor.name + "?"
                    ])

    for props in out_prop:
        def_prop = WordNet.getDefinition(props)

        if def_prop:
            hintChoices.append(actor.name + "'s personality, financial status or description means " + def_prop + ". How can you describe "
                + actor.name + "?")

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
    wnl = WordNetLemmatizer()

    for entries in ansList:
        ansType, answers = entries

        ans_obj = ""
        try:
            ans_obj = answers[2]
        except Exception as e:
            print("error in ans_actor: ", e)
        ans_actor = answers[0]

        actor = ""
        action = ""
        obj = ""
        propType = None
        prop = None
        stateVerb = ""
        stateWasVerb = ""
        verb = ""

        if len(answers[len(answers) - 1]) == 5:
            actor, action, obj, propType, prop = answers[len(answers) - 1]
        elif len(answers[len(answers) - 1]) == 2:
            actor, action = answers[len(answers) - 1]
            stateVerb = action

            if len(wordnet.synsets(action)) > 0 and getCommonPartOfSpeech(action) == 'a':
                if actor.gender == "collective":
                    verb = determineVerbForm(actor, "be", "past") + " "
                else:
                    verb = determineVerbForm(actor, "be", "past") + " "

        ans_act = determineVerbForm(actor, action, "past")

        if type(obj) is str:
            if len(wordnet.synsets(obj)) > 0 and getCommonPartOfSpeech(obj) == 'a':
                ans_act = determineVerbForm(actor, action, "present")

        if type(obj) is item_type.Item:
            obj = obj.name

        if len(wordnet.synsets(action)) > 0 and getCommonPartOfSpeech(action) == 'a':
            specialVerb = "become " + action
        elif len(wordnet.synsets(action)) > 0 and getCommonPartOfSpeech(action) == 'v':
            if len(wordnet.synsets(obj)) > 0 and getCommonPartOfSpeech(obj) == 'a':
                specialVerb = obj
            else:
                specialVerb = action + " " + obj
                if prop:
                    specialVerb = action + " " + prop + " " + obj
        else:
            specialVerb = action

        if stateVerb != "":
            stateVerb = stateVerb
            wasVerb = determineVerbForm(actor, "be", "past")
            stateWasVerb = wasVerb + " " + stateVerb

        elif stateVerb == "":
            if len(wordnet.synsets(obj)) > 0 and getCommonPartOfSpeech(obj) == 'a':
                wasVerb = determineVerbForm(actor, "be", "present")
                stateWasVerb = wasVerb + " " + obj
                stateVerb = obj

        obj = formatMultipleItems(obj)

        sent_ans_actor = ans_actor.name

        if type(actor) is str:
            sent_actor = actor
        else:
            sent_actor = actor.name

        action = action.replace("_", " ")
        poss = determinePossessiveForm(ans_actor)
        pres_ans_act = determineVerbForm(actor, action, "present")
        have = determineVerbForm(ans_actor, "have", "present")

        if "not" in ans_act:
            ans_act = "did " + ans_act
            pres_ans_act = "did " + pres_ans_act

        resForChar = ""
        resForItem = ""
        resForLoc = ""
        ans_resForChar = ""
        ans_resForItem = ""
        ans_resForLoc = ""
        alt_resForChar = ""
        alt_resForItem = ""
        alt_resForLoc = ""
        whAdd = "what "

        if obj != "":
            try:
                resForChar = Entity.charList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                resForItem = Entity.itemList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                resForLoc = Entity.locList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            if prop:
                prop = formatMultipleItems(prop)

            if propType == "appearance" or propType == "personality":
                specVerb = determineVerbForm("singular", "be", "present")

                if inflect.singular_noun(obj.lower()):
                    specVerb = determineVerbForm("plural", "be", "present")

                obj = " " + obj + " that " + specVerb + " " + prop

            elif propType == "amount":
                obj = prop + " " + obj

            else:
                obj = " " + obj

        if ans_obj != "":
            try:
                ans_resForChar = Entity.charList[ans_obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                ans_resForItem = Entity.itemList[ans_obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                ans_resForLoc = Entity.locList[ans_obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

        if ans_resForChar != "":
            whAdd = "who "

        elif ans_resForItem != "":
            whAdd = "what "

        elif ans_resForLoc != "":
            whAdd = "where "

        if ansType == "action":
            actionWord = whAdd + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "pastt")

        elif ansType == "desire":
            actionWord = whAdd + sent_ans_actor + " desired to " + answers[1][0]

        elif ansType == "state":
            actionWord = sent_ans_actor + poss + ansType

        elif ansType == "actor_appearance":
            actionWord = sent_ans_actor + poss + "appearance"

        elif ansType == "actor_personality":
            actionWord = sent_ans_actor + poss + "personality, financial status or description"

        elif ansType == "attribute":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "present")

        elif ansType == "item_appearance":
            actionWord = "the appearance of " + sent_ans_actor + " items"

        elif ansType == "item_amount":
            actionWord = "the amount of items " + sent_ans_actor + " " + have

        elif ansType == "location":
            address = answers[2]

            if " room" in address or " row" in address or "behind " in address:
                addWord = "seat"
            else:
                addWord = "address"

            actionWord = sent_ans_actor + poss + addWord

        if resForChar != "":
            resForChar = action + " someone"

            verbHas = "has " + ans_act

            dummy = " ".split(ans_act)
            if "not " in ans_act and "did " in ans_act and len(dummy) > 1:
                verbHas = "has " + "not " + dummy[len(dummy)-1]

            elif "did " in ans_act and "not " not in ans_act and len(dummy) > 1:
                verbHas = "has " + dummy[len(dummy)-1]

            print("verbHas: ", verbHas)
            alt_resForChar = verbHas + " someone"

        elif resForLoc != "":
            resForLoc = action + " at " + obj

            verbHas = "has " + ans_act

            dummy = " ".split(ans_act)
            if "not " in ans_act and "did " in ans_act and len(dummy) > 1:
                verbHas = "has " + "not " + dummy[len(dummy)-1]

            elif "did " in ans_act and "not " not in ans_act and len(dummy) > 1:
                verbHas = "has " + dummy[len(dummy)-1]

            alt_resForLoc = verbHas + " at " + obj

        elif resForItem != "":
            resForItem = action + " " + obj

            verbHas = "has " + ans_act

            dummy = " ".split(ans_act)
            if "not " in ans_act and "did " in ans_act and len(dummy) > 1:
                verbHas = "has " + "not " + dummy[len(dummy)-1]

            elif "did " in ans_act and "not " not in ans_act and len(dummy) > 1:
                verbHas = "has " + dummy[len(dummy)-1]

            alt_resForItem = verbHas + " " + obj

        hintTemplateA.extend([" What causes a person to " + specialVerb + "? Can you tell me?",
                              " Do you know anyone who " + stateWasVerb + alt_resForChar + alt_resForItem + alt_resForLoc + "? What happened?",
                              " What is something that could make you " + stateVerb + resForChar + resForItem + resForLoc + "? Maybe that also made "
                              + sent_actor + " " + action + obj + "."])

        hintTemplateB.extend([sent_actor + " " + verb + ans_act + obj + " because of "
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
    wnl = WordNetLemmatizer()

    for entries in ansList:
        ansType, answers = entries
        ans_obj = None

        try:
            ans_obj = answers[2]
        except Exception as e:
            print("error in ans_actor: ", e)

        ans_actor = answers[0]

        actor = ""
        action = ""
        obj = ""
        verb = ""
        propType = None
        prop = None

        if len(answers[len(answers) - 1]) == 5:
            actor, action, obj, propType, prop = answers[len(answers) - 1]
        elif len(answers[len(answers) - 1]) == 2:
            actor, action = answers[len(answers) - 1]

            if actor.gender == "collective":
                verb = determineVerbForm(actor, "be", "past") + " "
            else:
                verb = determineVerbForm(actor, "be", "past") + " "

        ans_act = determineVerbForm(actor, action, "past")

        if type(obj) is str:
            if len(wordnet.synsets(obj)) > 0 and getCommonPartOfSpeech(obj) == 'a':
                ans_act = determineVerbForm(actor, action, "present")

        if type(obj) is item_type.Item:
            obj = obj.name

        obj = formatMultipleItems(obj)

        if obj != "":
            if prop:
                prop = formatMultipleItems(prop)

            if propType == "appearance" or propType == "personality":
                specVerb = determineVerbForm("singular", "be", "present")

                if inflect.singular_noun(obj.lower()):
                    specVerb = determineVerbForm("plural", "be", "present")

                obj = " " + obj + " that " + specVerb + " " + prop

            elif propType == "amount":
                obj = prop + " " + obj

            else:
                obj = " " + obj

        sent_ans_actor = ans_actor.name

        if type(actor) is str:
            sent_actor = actor
        else:
            sent_actor = actor.name

        poss = determinePossessiveForm(ans_actor)
        actor_poss = determinePossessiveForm(actor)
        action = action.replace("_", " ")

        if "not " in ans_act:
            ans_act = "did " + action

        have = determineVerbForm(ans_actor, "have", "present")

        whAdd = "what "
        resForChar = ""
        resForItem = ""
        resForLoc = ""

        if ans_obj:
            try:
                resForChar = Entity.charList[ans_obj.lower()]
            except Exception as e:
                print("Error in promptActs char: ", e)

            try:
                resForItem = Entity.itemList[ans_obj.lower()]
            except Exception as e:
                print("Error in promptActs item: ", e)

            try:
                resForLoc = Entity.locList[ans_obj.lower()]
            except Exception as e:
                print("Error in promptActs loc: ", e)

        if resForChar != "":
            whAdd = "who "

        elif resForItem != "" and ans_obj:
            whAdd = "what "

        elif resForLoc != "" and ans_obj:
            whAdd = "where "

        if ansType == "action":
            actionWord = whAdd + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "past")

        elif ansType == "desire":
            actionWord = whAdd + sent_ans_actor + " desired to " + answers[1][0]
            ans_act = "desired to " + action

        elif ansType == "state":
            actionWord = sent_ans_actor + poss + ansType

        elif ansType == "actor_appearance":
            actionWord = sent_ans_actor + poss + "appearance"

        elif ansType == "actor_personality":
            actionWord = sent_ans_actor + poss + "personality, financial status or description"

        elif ansType == "attribute":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "present")

        elif ansType == "item_appearance":
            actionWord = "the appearance of " + sent_ans_actor + " items"

        elif ansType == "item_amount":
            actionWord = "the amount of items " + sent_ans_actor + " " + have

        elif ansType == "location":
            address = answers[2]

            if " room" in address or " row" in address or "behind " in address:
                addWord = "seat"
            else:
                addWord = "address"

            actionWord = sent_ans_actor + poss + addWord

        hintTemplateA.extend([" Can you tell me about " + actionWord + "?",
                              " How does that affect " + sent_actor + actor_poss + "actions? "])

        hintTemplateB.extend(["the reason why " + sent_actor + " " + verb + ans_act + obj + " has something to do with " + actionWord + "."])

        for hints in hintTemplateA:
            r = random.choice(hintTemplateB)
            hintChoices.append(r + hints)

        hintTemplateA = []
        hintTemplateB = []

    return hintChoices


def generateElabForActs(ansList):
    hintChoices = []
    wnl = WordNetLemmatizer()

    for entries in ansList:
        ansType, answers = entries
        ans_obj = None

        try:
            ans_obj = answers[2]
        except Exception as e:
            print("error in ans_actor: ", e)

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

        ans_act = determineVerbForm(actor, action, "past")

        if type(obj) is str:
            if len(wordnet.synsets(obj)) > 0 and getCommonPartOfSpeech(obj) == 'a':
                ans_act = determineVerbForm(actor, action, "present")

        def_prop = WordNet.getDefinition(ans_action, verb="Yes")

        if type(obj) is item_type.Item:
            obj = obj.name

        obj = formatMultipleItems(obj)

        sent_ans_actor = ans_actor.name

        if type(actor) is str:
            sent_actor = actor
        else:
            sent_actor = actor.name

        poss = determinePossessiveForm(ans_actor)
        action = action.replace("_", " ")
        have = determineVerbForm(ans_actor, "have", "present")

        if "not" in ans_act:
            ans_act = "did " + ans_act

        resForChar = ""
        resForItem = ""
        resForLoc = ""

        whAdd = " "

        if obj != "":
            try:
                resForChar = Entity.charList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                resForItem = Entity.itemList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            try:
                resForLoc = Entity.locList[obj.lower()]
            except Exception as e:
                print("Error in promptActs: ", e)

            if prop:
                prop = formatMultipleItems(prop)

            if propType == "appearance" or propType == "personality":
                verb = determineVerbForm("singular", "be", "present")

                if inflect.singular_noun(obj.lower()):
                    verb = determineVerbForm("plural", "be", "present")

                obj = " " + obj + " that " + verb + " " + prop

            elif propType == "amount":
                obj = prop + " " + obj

            else:
                obj = " " + obj

        if resForChar != "":
            resForChar = " a person"
            whAdd = "who "

        elif resForItem != "" and ans_obj:
            resForItem = " an item"
            whAdd = "what "

        elif resForLoc != "" and ans_obj:
            resForLoc = " somewhere"
            whAdd = "where "

        actionWord = ""
        if ansType == "action":
            actionWord = whAdd + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "past")

        elif ansType == "desire":
            actionWord = whAdd + sent_ans_actor + " desired to " + answers[1][0]
            ans_act = "desired to " + action

        elif ansType == "state":
            actionWord = sent_ans_actor + poss + ansType

        elif ansType == "actor_appearance":
            actionWord = sent_ans_actor + poss + "appearance"

        elif ansType == "actor_personality":
            actionWord = sent_ans_actor + poss + "personality, financial status or description"

        elif ansType == "attribute":
            actionWord = "what " + sent_ans_actor + " " + determineVerbForm(ans_actor, answers[1][0], "present")

        elif ansType == "item_appearance":
            actionWord = "the appearance of " + sent_ans_actor + " items"

        elif ansType == "item_amount":
            actionWord = "the amount of items " + sent_ans_actor + " " + have

        elif ansType == "location":
            address = answers[2]

            if " room" in address or " row" in address or "behind " in address:
                addWord = "seat"
            else:
                addWord = "address"

            actionWord = sent_ans_actor + poss + addWord

        if def_prop:
            hintChoices.append(
                sent_actor + " " + ans_act + obj + " because of " + actionWord + ". "
                + action.title() + " means " + def_prop + resForChar + resForItem + resForLoc + ". "
                "How does that explain " + ans_actor + poss + " actions?")

    return hintChoices


def generateMeaningForWord(sequence, word=None):
    queryWord = None

    if word == "end":
        queryWord = "_".join([x[0].lower() for x in sequence[5:-1]])

    elif word == "mid":
        queryWord = "_".join([x[0].lower() for x in sequence[2:-2]])

    if queryWord:
        def_word = WordNet.getDefinition(queryWord)

        return "meaning", queryWord.title() + " means " + def_word + "."

    return "meaning", "I did not see the meaning of that word in my dictionary. Maybe you should ask other people or" \
                      " check other dictionaries?"

def getCommonPartOfSpeech(word):
    L = [x.pos() for x in wordnet.synsets(word)]
    return max(set(L), key = L.count)
