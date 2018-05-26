import random

import nltk
from nltk.tag.stanford import CoreNLPParser
from nltk.tree import ParentedTree
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

import model.dialogue_manager.sentence_parser as parser
import model.dialogue_manager.content_provider as provider
import model.story_world.entities as Entity
import model.story_world.story_scenes as ref
import model.externals.logger as logger

incorrect = False
question = True
regSentence = True
gotHints = False
first = True
followUp = False
flip = True
answerList = []
finalHintList = []
result = []
compMessage = [""]
wrongMessage = [""]
correctAnswer = ()


def guessesExhausted():
    global incorrect
    global question
    global regSentence
    global gotHints
    global compMessage
    global first
    global followUp
    global finalHintList
    global flip

    first = True
    incorrect = False
    question = True
    regSentence = True
    gotHints = False
    followUp = True
    flip = True
    compMessage = [""]
    finalHintList = []


def gotCorrectAnswer(preparedString, followUpSent):
    global incorrect
    global question
    global regSentence
    global gotHints
    global result
    global wrongMessage
    global compMessage
    global first

    first = True
    incorrect = True
    question = False
    regSentence = False
    gotHints = False
    wrongMessage = [""]
    compMessage = [""]

    result = []
    result.append(preparedString + followUpSent)


def resetWrongMessage():
    message = ["I don't think that's the answer, but you can try again. ",
               "I don't think that's the answer. Let's try getting the right answer together. ",
               "I don't think that's the answer. Let's try again! "]

    return message


def cleanList():
    global answerList

    for entries in answerList:
        temp = entries
        ansType, ansList = entries

        if not ansList:
            answerList.remove(temp)

        else:
            if type(ansList) is list:
                for answer in ansList:
                    if not answer:
                        answerList.remove(temp)
            elif not ansList:
                answerList.remove(temp)

    return answerList


def findNearNot(sent, verbTags):
    curr = 0
    found = False
    while curr < len(sent):
        if not found and sent[curr][0].lower() == 'not':
            found = True
        elif found and sent[curr][1] in verbTags:
            return "not " + sent[curr][0]
        curr = curr + 1

    if found:
        return None
    else:
        return None


def findNearNot_Adj(sent, verbTags):
    curr = 0
    found = False
    while curr < len(sent):
        if not found and sent[curr][1].lower() == 'JJ':
            found = True
        elif found and sent[curr][1] in verbTags:
            return "not " + sent[curr][0]
        curr = curr + 1

    if found:
        return None
    else:
        return None


def find_index_with_duplicates(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at + 1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs


def find_matches(list_keys, list_keys_loc, list_pos):
    match_string = " ".join([x[0].lower() for x in list_pos])
    list_match = [x for x in list_keys if x in match_string]
    list_match_loc = [x for x in list_keys_loc if x in match_string]
    dict_index = {}
    for x in list_match:
        dict_index[x[0]] = find_index_with_duplicates(list_pos, x)

    list_match.extend(list_match_loc)

    return list_match


def combine_similar(user_input, tags):
    output = []
    curr = []
    tag = ""
    for x in user_input:
        if x[1] not in tags:
            if len(curr) > 0:
                output.append((" ".join([x[0].lower() for x in curr]), tag))
                curr[:] = []
                tag = ""
            output.append(x)
        elif x[1] == tag:
            curr.append(x)
        else:
            if len(curr) > 0:
                output.append((" ".join([x[0].lower() for x in curr]), tag))
                curr[:] = []
            tag = x[1]
            curr.append(x)
    if len(curr) > 0:
        output.append((" ".join([x[0].lower() for x in curr]), tag))
    return output


def single_sentence(sequence):
    tags = ["NNP", "NNS", "NNPS"]
    processed_message = combine_similar(sequence, tags)

    return determineSentenceType(processed_message)


def split_compound(tree, count, messages):
    if type(tree) is nltk.tree.ParentedTree:
        if tree.label() == 'SBARQ' and count > 1:
            global compMessage
            compMessage = ["Let us talk about your first question for now. ",
                           "We should focus on your first question. ",
                           "Let's focus on your first question? Ok so, ",
                           "Hey, let's answer your first question first. "]

            # print("compMessage: ", compMessage)

    for subtree in tree:
        if type(subtree) is nltk.tree.ParentedTree:
            split_compound(subtree, count + 1, messages)
        else:
            break

    return messages


def populateDialogueTurns():
    global answerList
    global finalHintList
    global result

    finalHintList = []
    hintList = []

    for entries in answerList:
        ansType, ansList = entries
        hintChoices = []

        if ansType == "relationship_name":
            actor, rel, char = ansList

            if len(char) > 1:
                result = []
                nameList = [x.name.title() for x in char]
                out_char = ", ".join(nameList[:-1]) + " and " + nameList[len(nameList) - 1]

                result.append(actor.name.title() + " has many " + rel + "s. They are " + out_char + ".")
                guessesExhausted()

            else:
                hintChoices.extend(provider.generateHintForRelName(ansList))
                hintList.extend(
                    ["I think " + entries + " Which of the characters has a name like this?" for entries in
                     hintChoices])

        elif ansType == "relationship_rel":
            hintChoices.extend(provider.generateHintForRelRel(ansList))

            if len(hintChoices) > 3:
                i = 0
                temp = []
                while i < 3:
                    r = random.choice(hintChoices)
                    hintChoices.remove(r)
                    temp.append(r)
                    i = i + 1

                hintList.extend(["I think " + entries for entries in temp])

            else:
                hintList.extend(["I think " + entries for entries in hintChoices])

        elif ansType == "location":
            hintChoices.extend(provider.generateHintForLocation(ansList))

            if len(hintChoices) > 3:
                i = 0
                temp = []
                while i < 3:
                    r = random.choice(hintChoices)
                    hintChoices.remove(r)
                    temp.append(r)
                    i = i + 1

                hintList.extend(
                    ["I think " + entries + " What place in the story do you think this is?" for entries in
                     temp])

            else:
                hintList.extend(
                    ["I think " + entries + " What place in the story do you think this is?" for entries in
                     hintChoices])

        elif ansType == "appProperty":
            hintChoices.extend(provider.generateHintForAppProp(ansList))
            hintChoices.extend(provider.generatePumpForAppProp(ansList))
            hintChoices.extend(provider.generatePromptForAppProp(correctAnswer))

            if hintChoices:
                if len(hintChoices) > 5:
                    i = 0
                    temp = []
                    while i < 5:
                        r = random.choice(hintChoices)
                        hintChoices.remove(r)
                        temp.append(r)
                        i = i + 1

                    hintList.extend(temp)

                else:
                    hintList.extend(hintChoices)

        elif ansType == "attribute":
            hintChoices.extend(provider.generatePromptForAttr(ansList, correctAnswer))
            hintChoices.extend(provider.generateElabForAttr(ansList))
            # hintChoices = provider.generatePumpsForAppProp()
            # hintChoices = provider.generateElabForAppProp()

            hintList.extend(hintChoices)

        elif ansType == "cause":
            hintChoices.extend(provider.generatePumpForActs(ansList))
            hintChoices.extend(provider.generatePromptForActs(ansList))
            hintChoices.extend(provider.generateElabForActs(ansList))

            hintList.extend(["I think " + entries for entries in hintChoices])

        elif ansType == "type":
            hintChoices.extend(provider.generateHintForType(ansList))

            hintList.extend(hintChoices)

        elif ansType == "item_appearance":
            hintChoices.extend(provider.generateElabForItem(ansList))
            hintChoices.extend(provider.generatePumpForItem(ansList))

            hintList.extend(hintChoices)

        elif ansType == "item_amount":
            print("item_amount")

        elif ansType == "actor_appearance":
            hintChoices.extend(provider.generatePromptForAppearance(ansList))
            hintChoices.extend(provider.generatePumpForAppearance(ansList))
            hintChoices.extend(provider.generateElabForAppearance(ansList))

            hintList.extend(["I think " + entries for entries in hintChoices])

        elif ansType == "actor_personality":
            hintChoices.extend(provider.generatePromptForPersonality(ansList))
            hintChoices.extend(provider.generatePumpForPersonality(ansList))
            hintChoices.extend(provider.generateElabForPersonality(ansList))

            hintList.extend(["I think " + entries for entries in hintChoices])

        elif ansType == "confirmation":
            hintList.append("Do you mean " + ansList.name.title() + "?")

        print("hintList: ", hintList)

    if hintList:
        if len(hintList) > 5:
            i = 0
            while i < 5:
                r = random.choice(hintList)
                hintList.remove(r)
                finalHintList.append(r)
                i = i + 1

        else:
            finalHintList.extend(hintList)


def stop(sequence):
    tempResult = []
    global answerList
    global finalHintList
    global question
    global followUp

    response = "i do n't want to talk anymore"
    user_response = " ".join([x[0].lower() for x in sequence][:7])

    if user_response == response:
        tempResult.extend(["I see", "Okay"])
        result.append(random.choice(tempResult) + ". I'll just be here if you need me.")

        guessesExhausted()
        question = False
        followUp = False
        answerList = []
        finalHintList = []


def determineSentenceType(sequence):
    global incorrect
    global question
    global regSentence
    global gotHints
    global finalHintList
    global first
    global answerList
    global result
    global compMessage
    global wrongMessage
    global followUp
    global flip

    wnl = WordNetLemmatizer()

    sequence = [(x[0].lower(), x[1]) for x in sequence]
    print("sequence: ", sequence)
    beg = sequence[0][0]
    end = sequence[len(sequence) - 1][0]
    posList = [x for x, y in enumerate(sequence) if y[1] == "POS"]
    toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]
    ofList = [x for x, y in enumerate(sequence) if y[0] == "of"]
    andList = [x for x, y in enumerate(sequence) if y[0] == "and"]

    dummy = find_matches(Entity.itemList.keys(), Entity.locList.keys(), sequence)
    itemList = []
    if dummy:
        itemList = list(set(dummy))
        print("itemList: ", itemList)

    if toList:
        sequence = [i for i in sequence if i[0] != "the"]
        toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]

    nounTags = ["NN", "NNS", "NNP", "NNPS"]
    charList = [item[0] for item in sequence if item[1] in nounTags]

    verbTags = ["VBD", "VBZ", "VB", "VBP"]
    verbList = [item[0] for item in sequence if item[1] in verbTags]

    not_verbs = findNearNot(sequence, verbTags)
    if not_verbs:
        verbList.append(not_verbs)

    adjTags = ["JJ", "JJS", "JJR"]
    adjList = [item[0] for item in sequence if item[1] in adjTags]

    advTags = ["RB", "RBS", "RBR"]
    advList = [item[0] for item in sequence if item[1] in advTags]

    temp = []
    tempResult = []

    for items in charList:
        if wordnet.synsets(items, 'v'):
            verbList.append(items)

    stop(sequence)

    if beg == "who" and end == "?":
        temp.extend(parser.parseWhoMessage(sequence, posList, ofList, toList, charList))
        question = True
        followUp = False
        regSentence = False

    elif beg == "where" and end == "?":
        temp.extend(parser.parseWhereMessage(charList, verbList))
        question = True
        followUp = False
        regSentence = False

    elif beg == "what" and end == "?":
        temp.extend(parser.parseWhatMessage(sequence, posList, ofList, charList, andList, itemList))
        question = True
        followUp = False
        regSentence = False

    elif beg == "why" and end == "?":
        temp.extend(parser.parseWhyMessage(charList, verbList, advList, itemList, adjList))
        question = True
        followUp = False
        regSentence = False

    if len(sequence) > 3 and end == "." and regSentence and \
            not set([x[0].lower() for x in sequence]).issuperset(set("i do n't want to talk anymore".split())):
        tempResult.extend(["I see.", "Tell me more.", "Okay."])
        result.append(random.choice(tempResult))

        guessesExhausted()
        question = False
        followUp = False

    elif len(sequence) <= 3 and end == "." and regSentence:
        generateFollowUp(None, None)
        question = False
        followUp = True
        regSentence = False
        flip = False
        print("initial result: ", result)

    if question is True:
        answerList = []
        answerList.extend(temp)

    if question is True or followUp is True:
        if question is True:
            result = []
        wrongMessage = [""]
        incorrect = True

        answerList = [x for x in answerList if x[0] != "unknown"]
        tempResult = []
        print("answerList: ", answerList)

        if not answerList:
            tempResult.extend(["I don't really know the answer to that. You can rephrase your question if you want?",
                               "I'm sorry but, I don't really know the answer to your question",
                               "I don't really know the answer to that. But you can ask me other questions."])

            result.append(random.choice(tempResult))
            guessesExhausted()

        if answerList:
            question = False

            for answers in answerList:
                ansType, answer = answers

                if ansType == "meaning":
                    result.append(answer)
                    guessesExhausted()

            #populate hints
            if gotHints is False:
                wrongMessage = [""]
                incorrect = True

                cleanList()
                populateDialogueTurns()
                gotHints = True

    #check answer
    if (question is False or followUp is True) and incorrect is True:
        stop(sequence)

        wrongMessage = resetWrongMessage()
        for answers in answerList:
            ansType, ansList = answers
            print("ansType: ", ansType)

            if ansType == "relationship_name":
                actor, rel, char = ansList
                answer = provider.formatMultipleItems(rel)
                if charList:
                    for character in charList:
                        if char[0].name.lower() == character:
                            sentence_answer = char[0].name + " is " + actor.name + "'s " + answer
                            generateFollowUp(sentence_answer, "relationship_name")

            elif ansType == "relationship_rel":
                actor, rel, char = ansList
                if type(rel) is not str:
                    pluralList = [x + "s" for x in rel]
                    answer = list(set(rel) & set(charList))
                    pluralAnswer = list(set(pluralList) & set(charList))

                    if answer:
                        answer = provider.formatMultipleItems(answer)
                        sentence_answer = char[0].name + " is " + actor.name + "'s " + answer
                        generateFollowUp(sentence_answer, "relationship_rel")

                    elif pluralAnswer:
                        pluralAnswer = provider.formatMultipleItems(pluralAnswer)
                        sentence_answer = char[0].name + " is " + actor.name + "'s " + pluralAnswer
                        generateFollowUp(sentence_answer, "relationship_rel")

                elif type(rel) is str:
                    if charList:
                        for character in charList:
                            if rel == character or rel + "s" == character:
                                sentence_answer = char[0].name + " is " + actor.name + "'s " + rel
                                generateFollowUp(sentence_answer, "relationship_rel")

            elif ansType == "location":
                actor, action, loc = ansList
                if charList:
                    for character in charList:
                        if character in loc.lower():
                            sentence_answer = actor.name + " " + action + " at " + loc
                            generateFollowUp(sentence_answer, "location")

            elif ansType == "appProperty":
                actor, prop = ansList

                if adjList:
                    for adjective in adjList:
                        for entries in prop:
                            if entries == adjective:
                                sentence_answer = actor.name + " is " + entries
                                generateFollowUp(sentence_answer, "appProperty")

                if advList:
                    for adverb in advList:
                        for entries in prop:
                            if entries == adverb:
                                sentence_answer = actor.name + " is " + entries
                                generateFollowUp(sentence_answer, "appProperty")

            elif ansType == "cause":
                for entries in ansList:
                    ansType, answers = entries
                    print("ansType: ", ansType)
                    get_ans = answers[len(answers)-1]
                    get_actor = ""
                    get_act = ""
                    get_obj = ""
                    get_propType = None
                    get_prop = None

                    if len(get_ans) == 5:
                        get_actor, get_act, get_obj, get_propType, get_prop = get_ans
                    elif len(get_ans) == 2:
                        get_actor, get_act = get_ans

                    get_act = provider.determineVerbForm(get_actor, get_act, "past")

                    if get_obj != "" and get_obj:
                        if type(get_obj) is str:
                            get_obj = get_obj
                        else:
                            get_obj = get_obj.name

                    if get_prop:
                        get_prop = provider.formatMultipleItems(get_prop)

                        if get_propType == "appearance" or get_propType == "personality":
                            get_obj = get_obj + " that is " + get_prop

                        elif get_propType == "amount":
                            get_obj = get_prop + " " + get_obj

                    if type(get_actor) is str:
                        get_actor = get_actor
                    else:
                        get_actor = get_actor.name

                    sentence_answer = "I think " + get_actor + " " + get_act + " " + get_obj + " because "

                    if ansType == "action":
                        actor, act, out_obj, propType, prop, get_ans = answers
                        givenAnswers = []
                        out_objList = out_obj.split()
                        givenAnswers.extend([actor.name])
                        givenAnswers.extend(out_objList)
                        verbPresent = False

                        givenAnswers = [x.lower() for x in givenAnswers]
                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                            elif words[1] in nounTags:
                                formatted_seq.append(wnl.lemmatize(words[0]))
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]

                        for verb in act[1]:
                            if verb in sentence:
                                verbPresent = True

                        act = provider.determineVerbForm(actor, act[0], "past")

                        if prop:
                            prop = provider.formatMultipleItems(prop)
                            if propType == "appearance" or propType == "personality":
                                out_obj = out_obj + " that is " + prop
                            elif propType == "amount":
                                out_obj = prop + " " + out_obj

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actor.name + " " + act + " " + out_obj
                            generateFollowUp(sentence_answer, "action")

                    elif ansType == "desire":
                        actor, act, out_obj, get_ans = answers
                        givenAnswers = []
                        out_objList = out_obj.split()
                        givenAnswers.extend([actor.name])
                        givenAnswers.extend(out_objList)
                        givenAnswers = [x.lower() for x in givenAnswers]
                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                            elif words[1] in nounTags:
                                formatted_seq.append(wnl.lemmatize(words[0]))
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]
                        verbPresent = False

                        for verb in act[1]:
                            if verb in sentence:
                                verbPresent = True

                        act = provider.determineVerbForm(actor, act[0], "past")

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actor.name + " desired to " + act + " " + out_obj
                            generateFollowUp(sentence_answer, "desire")

                    elif ansType == "state":
                        actor, out_state, get_ans = answers
                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        givenAnswers = [x.lower() for x in givenAnswers]
                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]
                        verbPresent = False

                        for verb in out_state[1]:
                            if verb in sentence:
                                verbPresent = True

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actor.name + " is " + out_state
                            generateFollowUp(sentence_answer, "state")

                    elif ansType == "location":
                        print("answers: ", answers)
                        actor, action, loc, get_ans = answers
                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        givenAnswers.append(loc)
                        givenAnswers = [x.lower() for x in givenAnswers]
                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]
                        verbPresent = False

                        for verb in action[1]:
                            if verb in sentence:
                                verbPresent = True

                        action = provider.determineVerbForm(actor, action[0], "past")

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actor.name + " " + action + " at " + loc
                            generateFollowUp(sentence_answer, "location")

                    elif ansType == "actor_appearance":
                        actor, prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.append(actor.name)
                        if type(prop) is list:
                            givenAnswers.extend(prop)
                        else:
                            givenAnswers.append(prop)

                        out_prop = provider.formatMultipleItems(prop)

                        if set(sentence).issuperset(set(givenAnswers)):
                            sentence_answer = sentence_answer + actor.name + " looks " + out_prop
                            generateFollowUp(sentence_answer, "actor_appearance")

                    elif ansType == "actor_personality":
                        actor, prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.append(actor.name)
                        if type(prop) is list:
                            givenAnswers.extend(prop)
                        else:
                            givenAnswers.append(prop)

                        out_prop = provider.formatMultipleItems(prop)

                        if set(sentence).issuperset(set(givenAnswers)):
                            sentence_answer = sentence_answer + actor.name + " is " + out_prop
                            generateFollowUp(sentence_answer, "actor_personality")

                    elif ansType == "attribute":
                        actor, act, attr, propType, out_prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        if out_prop:
                            givenAnswers.extend([out_prop])
                        givenAnswers.extend(attr.split())
                        givenAnswers = [x.lower() for x in givenAnswers]
                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                            elif words[1] in nounTags:
                                formatted_seq.append(wnl.lemmatize(words[0]))
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]
                        verbPresent = False

                        for verb in act[1]:
                            if verb in sentence:
                                verbPresent = True

                        act = provider.determineVerbForm(actor, act[0], "past")

                        if out_prop:
                            sent_prop = provider.formatMultipleItems(out_prop)
                            sent_add = " that is "
                        else:
                            sent_prop = ""
                            sent_add = ""

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            if propType == "amount":
                                sentence_answer = sentence_answer + actor.name + " " + act + " " + sent_prop + " " + attr
                            else:
                                sentence_answer = sentence_answer + actor.name + " " + act + " " + attr + sent_add + sent_prop

                            generateFollowUp(sentence_answer, "attribute")

            elif ansType == "item_appearance":
                actor, act, item, prop = ansList

                givenAnswers = []
                givenAnswers.append(item)
                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                out_prop = provider.formatMultipleItems(prop)

                givenAnswers = [x.lower() for x in givenAnswers]
                print("sequence: ", sequence)

                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    elif words[1] in nounTags:
                        formatted_seq.append(wnl.lemmatize(words[0]))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]

                print("sentence: ", sentence)
                print("givenAnswers: ", givenAnswers)

                act = provider.determineVerbForm(actor, act[0], "past")

                if set(sentence).issuperset(set(givenAnswers)):
                    sentence_answer = actor.name + " " + act + " a " + item + " that looks " + out_prop
                    generateFollowUp(sentence_answer, "item_appearance")

            elif ansType == "item_amount":
                a = 1

            elif ansType == "action":
                actor, act, out_obj, propType, prop = ansList
                givenAnswers = []
                out_objList = out_obj.split()
                givenAnswers.extend([actor.name])
                givenAnswers.extend(out_objList)
                verbPresent = False

                givenAnswers = [x.lower() for x in givenAnswers]
                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    elif words[1] in nounTags:
                        formatted_seq.append(wnl.lemmatize(words[0]))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]

                for verb in act[1]:
                    if verb in sentence:
                        verbPresent = True

                act = provider.determineVerbForm(actor, act[0], "past")

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    sentence_answer = actor.name + " " + act + " " + out_obj
                    generateFollowUp(sentence_answer, "action")

            elif ansType == "desire":
                actor, act, out_obj = ansList
                givenAnswers = []
                out_objList = out_obj.split()
                givenAnswers.extend([actor.name])
                givenAnswers.extend(out_objList)
                givenAnswers = [x.lower() for x in givenAnswers]
                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    elif words[1] in nounTags:
                        formatted_seq.append(wnl.lemmatize(words[0]))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]
                verbPresent = False

                for verb in act[1]:
                    if verb in sentence:
                        verbPresent = True

                act = provider.determineVerbForm(actor, act[0], "past")

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    sentence_answer = actor.name + " desired to " + act + " " + out_obj
                    generateFollowUp(sentence_answer, "desire")

            elif ansType == "state":
                actor, out_state = ansList
                givenAnswers = []
                givenAnswers.extend([actor.name])
                givenAnswers = [x.lower() for x in givenAnswers]
                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]
                verbPresent = False

                for verb in out_state[1]:
                    if verb in sentence:
                        verbPresent = True

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    sentence_answer = actor.name + " is " + out_state
                    generateFollowUp(sentence_answer, "state")

            elif ansType == "actor_appearance":
                actor, prop = ansList

                givenAnswers = []
                givenAnswers.append(actor.name)
                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                out_prop = provider.formatMultipleItems(prop)

                if set(sentence).issuperset(set(givenAnswers)):
                    sentence_answer = actor.name + " looks " + out_prop
                    generateFollowUp(sentence_answer, "actor_appearance")

            elif ansType == "actor_personality":
                actor, prop = ansList

                givenAnswers = []
                givenAnswers.append(actor.name)
                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                out_prop = provider.formatMultipleItems(prop)

                if set(sentence).issuperset(set(givenAnswers)):
                    sentence_answer = actor.name + " is " + out_prop
                    generateFollowUp(sentence_answer, "actor_personality")

            elif ansType == "attribute":
                actor, act, attr, propType, out_prop = ansList

                givenAnswers = []
                givenAnswers.extend([actor.name])
                if out_prop:
                    givenAnswers.extend([out_prop])
                givenAnswers.extend(attr.split())
                givenAnswers = [x.lower() for x in givenAnswers]
                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    elif words[1] in nounTags:
                        formatted_seq.append(wnl.lemmatize(words[0]))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]
                verbPresent = False

                for verb in act[1]:
                    if verb in sentence:
                        verbPresent = True

                act = provider.determineVerbForm(actor, act[0], "past")

                if out_prop:
                    sent_prop = provider.formatMultipleItems(out_prop)
                    sent_add = " that is "
                else:
                    sent_prop = ""
                    sent_add = ""

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    if propType == "amount":
                        sentence_answer = actor.name + " " + act + " " + sent_prop + " " + attr
                    else:
                        sentence_answer = actor.name + " " + act + " " + attr + sent_add + sent_prop

                    generateFollowUp(sentence_answer, "attribute")

            elif ansType == "type":
                a = 1

    if gotHints is True and incorrect is True and regSentence is False:
        sentences = []

        #take hints to give
        if finalHintList != [[]] and finalHintList != []:
            if flip:
                r = random.choice(finalHintList)
                finalHintList.remove(r)

                if first is True:
                    result.append(random.choice(compMessage) + r)
                    first = False
                else:
                    result.append(random.choice(wrongMessage) + r)

            flip = True

        #give answer since guesses exhausted
        else:
            for answers in answerList:
                ansType, ansList = answers

                if ansType == "relationship_name":
                    actor, rel, char = ansList

                    out = provider.formatMultipleItems(rel)

                    sentences.append("I think " + actor.name.title() + "'s " + out + " is " + char[0].name.title() + ".")

                elif ansType == "relationship_rel":
                    actor, rel, char = ansList

                    out = provider.formatMultipleItems(rel)

                    sentences.append("I think " + char.name.title() + " is " + actor.name.title() + "'s " + out + ".")

                elif ansType == "state":
                    actor, action, loc = ansList

                    sentences.append("I think " + actor.name.title() + " is " + action + " in " + loc + ".")

                elif ansType == "cause":
                    temp = []

                    sent_prop = ""
                    sent_add = ""

                    for entries in ansList:
                        ansType, answers = entries

                        get_ans = answers[len(answers) - 1]
                        get_actor = ""
                        get_act = ""
                        get_obj = ""
                        get_propType = None
                        get_prop = None

                        if len(get_ans) == 5:
                            get_actor, get_act, get_obj, get_propType, get_prop = get_ans
                        elif len(get_ans) == 2:
                            get_actor, get_act = get_ans

                        get_act = provider.determineVerbForm(get_actor, get_act, "past")

                        if get_obj != "":
                            if type(get_obj) is str:
                                get_obj = get_obj
                            else:
                                get_obj = get_obj.name

                        if get_prop:
                            get_prop = provider.formatMultipleItems(get_prop)

                            if get_propType == "appearance" or get_propType == "personality":
                                get_obj = get_obj + " that looks " + get_prop
                            elif get_propType == "amount":
                                get_obj = get_prop + " " + get_obj

                        if ansType == "action":
                            actor, act, out_obj, propType, prop, get_ans = answers
                            act = provider.determineVerbForm(actor, act[0], "past")

                            temp.append(actor.name + " " + act + " " + out_obj)

                        elif ansType == "desire":
                            actor, act, out_obj, get_ans = answers

                            temp.append(actor.name + " desired to " + act[0] + " " + out_obj)

                        elif ansType == "state":
                            actor, out_state, get_ans = answers

                            out_state = provider.determineVerbForm(actor, out_state[0], "present")

                            temp.append(actor.name + " is " + out_state)

                        elif ansType == "location":
                            actor, action, loc, get_ans = answers
                            action = provider.determineVerbForm(actor, action[0], "past")

                            temp.append(actor.name + " " + action + " at " + loc)

                        elif ansType == "actor_appearance":
                            actor, prop, get_ans = answers
                            out_prop = provider.formatMultipleItems(prop)

                            temp.append(actor.name + " looks " + out_prop)

                        elif ansType == "actor_personality":
                            actor, prop, get_ans = answers
                            out_prop = provider.formatMultipleItems(prop)

                            temp.append(actor.name + " is " + out_prop)

                        elif ansType == "attribute":
                            actor, act, attr, propType, out_prop, get_ans = answers
                            act = provider.determineVerbForm(actor, act[0], "past")

                            if out_prop:
                                sent_prop = provider.formatMultipleItems(out_prop)
                                sent_add = " that is "

                            if propType == "amount":
                                temp.append(actor.name + " " + act + " " + sent_prop + " " + attr)
                            else:
                                temp.append(actor.name + " " + act + " " + attr + sent_add + sent_prop)

                        sentence = get_actor.name + " " + get_act + " " + get_obj + " because "

                    cause = provider.formatMultipleItems(temp)
                    sentences.append(sentence + cause)

                elif ansType == "item_appearance":
                    actor, act, item, prop = ansList

                    out_prop = provider.formatMultipleItems(prop)
                    act = provider.determineVerbForm(actor, act[0], "past")

                    result.append(actor.name + " " + act + " a " + item + " that is " + out_prop + ".")

                elif ansType == "item_amount":
                    print("item_amount")

                elif ansType == "action":
                    actor, act, out_obj, propType, prop = ansList

                    out_obj = provider.formatMultipleItems(out_obj)
                    if propType and prop:
                        prop = provider.formatMultipleItems(prop)

                        if propType == "appearance" or propType == "personality":
                            out_obj = out_obj + " that looks " + prop
                        elif propType == "amount":
                            out_obj = prop + " " + out_obj

                    act = provider.determineVerbForm(actor, act[0], "past")

                    sentences.append(actor.name + " " + act + " " + out_obj)

                elif ansType == "desire":
                    actor, act, out_obj = ansList

                    sentences.append(actor.name + " desired to " + act[0] + " " + out_obj)

                elif ansType == "state":
                    actor, out_state = ansList

                    out_state = provider.determineVerbForm(actor, out_state[0], "present")

                    sentences.append(actor.name + " is " + out_state)

                elif ansType == "location":
                    actor, action, loc = ansList

                    action = provider.determineVerbForm(actor, action[0], "past")

                    sentences.append(actor.name + " " + action + " at " + loc)

                elif ansType == "actor_appearance":
                    actor, prop = ansList

                    out_prop = provider.formatMultipleItems(prop)

                    sentences.append(actor.name + " looks " + out_prop)

                elif ansType == "actor_personality":
                    actor, prop = ansList

                    out_prop = provider.formatMultipleItems(prop)

                    sentences.append(actor.name + " is " + out_prop)

                elif ansType == "attribute":
                    actor, act, attr, propType, out_prop = ansList

                    act = provider.determineVerbForm(actor, act[0], "past")

                    if propType == "amount":
                        sentences.append(actor.name + " " + act + " " + sent_prop + " " + attr)
                    else:
                        sentences.append(actor.name + " " + act + " " + attr + sent_add + sent_prop)

            print("initial result 2: ", result)
            print("sentences: ", sentences)
            if sentences:
                dummy = provider.formatMultipleItems(sentences)
                generateFollowUp(dummy, None, exhausted="yes")

    if result:
        print("result: ", result)
        if len(result) > 1:
            dummy = "; ".join(result[:-1]) + " and " + result[len(result) - 1]
            result = []
            return dummy

        elif len(result) == 1:
            dummy = result[0]
            result = []
            return dummy
    else:
        return "Try asking me a question."


def getRandomActor():
    name, actor = random.choice(list(Entity.charList.items()))

    return actor


def generateFollowUpSentence():
    global answerList
    global finalHintList

    finalHintList = []
    answerList = []
    output_choices = []
    action = None
    state = None

    while not output_choices:
        output_choices = []

        actor = getRandomActor()
        try:
            action = Entity.charList[actor.name.lower()].act
        except Exception as e:
            print("Error in action generateFollowUp: ", e)

        try:
            state = Entity.charList[actor.name.lower()].state
        except Exception as e:
            print("Error in state generateFollowUp: ", e)

        # try:
        #     appProp = Entity.charList[actor.name.lower()].appProp
        # except Exception as e:
        #     print("Error in appProp generateFollowUp: ", e)
        #
        # try:
        #     perProp = Entity.charList[actor.name.lower()].perProp
        # except Exception as e:
        #     print("Error in perProp generateFollowUp: ", e)

        # try:
        #   location = Entity.charList[actor.name.lower()].loc
        # except Exception as e:
        #     print("Error in loc generateFollowUp: ", e)

        try:
            desire = Entity.charList[actor.name.lower()].des
        except Exception as e:
            print("Error in desire generateFollowUp: ", e)


        # if appProp:
        #     current = random.choice(appProp)
        #     prop, event = current
        #
        #     followUpResult = ref.queryRelations(event, "cause")
        #
        #     if followUpResult:
        #         temp = (event, provider.whatQuestion(actor, None, "appearance", None))
        #         output_choices.append(temp)
        #
        # if perProp:
        #     current = random.choice(perProp)
        #     prop, event = current
        #
        #     followUpResult = ref.queryRelations(event, "cause")
        #
        #     if followUpResult:
        #         temp = (event, provider.whatQuestion(actor, None, "personality", None))
        #         output_choices.append(temp)
        #
        # if location:
        #     current = random.choice(location)
        #     act, loc, event = current
        #
        #     if type(loc) is str:
        #         loc = loc.lower()
        #
        #     else:
        #         loc = loc.name.lower()
        #
        #     followUpResult = ref.queryRelations(event, "cause")
        #
        #     if followUpResult:
        #         temp = (event, provider.whereQuestion(actor, act[0], loc))
        #         output_choices.append(temp)

        if desire:
            current = random.choice(desire)
            des, obj, event = current

            if type(obj) is str:
                obj = obj.lower()

            else:
                obj = obj.name.lower()

            followUpResult = ref.queryRelations(event, "cause")

            if followUpResult:
                temp = (event, provider.whyQuestion(actor, des[0], obj))
                output_choices.append(temp)

        if action:
            current = random.choice(action)
            act, obj, event = current

            if type(obj) is str:
                obj = obj.lower()

            else:
                obj = obj.name.lower()

            followUpResult = ref.queryRelations(event, "cause")

            if followUpResult:
                temp = (event, provider.whyQuestion(actor, act[0], obj))
                output_choices.append(temp)

        if state:
            current = random.choice(state)
            state, event = current
            print("state[0]: ", state[0])

            followUpResult = ref.queryRelations(event, "cause")

            if followUpResult:
                temp = (event, provider.whyQuestion(actor, state[0], None))
                output_choices.append(temp)

    print("output_choices: ", output_choices)
    event, output = random.choice(output_choices)
    answerList.append(output)
    sentence = provider.assembleSentence(event, genType="sentence")
    populateDialogueTurns()

    return " How come " + sentence + "? What do you think is the reason?"


def generateFollowUp(answer, questType, exhausted=None):
    global correctAnswer
    global followUp
    global gotHints
    global flip
    global regSentence

    followUp = True
    praiseChoices = []

    followUpSent = generateFollowUpSentence()

    if answer is None and questType is None:
        gotCorrectAnswer("", followUpSent)

    elif exhausted == "yes" and not questType and answer is not None:
        preparedString = "I think " + answer + "."
        gotCorrectAnswer(preparedString, followUpSent)

    else:
        praiseChoices.extend(["Hooray! I also think ",
                              "You got it! "])

        if questType == "relationship_name" or questType == "location" or questType == "relationship_rel" \
                or questType == "action" or questType == "state" or questType == "desire"\
                or questType == "type" or questType == "item_appearance" or "item_amount":

            r = random.choice(praiseChoices)
            preparedString = r + answer + "."
            gotCorrectAnswer(preparedString, followUpSent)

        elif questType == "actor_appearance" or "actor_personality":
            if correctAnswer:
                actor, appearance = correctAnswer

                r = random.choice(praiseChoices)
                preparedString = r + actor.name + " is " + appearance + " because " + answer + "."
                gotCorrectAnswer(preparedString, followUpSent)

    gotHints = True
    flip = False
    regSentence = False


def parse_message(message):
    r = CoreNLPParser('http://localhost:9000/')
    user_input = ParentedTree.convert(list(r.raw_parse(message))[0])

    user_input.pretty_print()

    messages = []
    messages = [split_compound(user_input, 0, messages)][0]

    if not messages:
        messages.append(single_sentence(user_input.pos()))

    if len(messages) > 1:
        output_message = " ".join(messages)
    else:
        output_message = messages[0]

    return output_message
