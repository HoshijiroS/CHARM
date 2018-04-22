import random

import nltk
from nltk.tag.stanford import CoreNLPParser
from nltk.tag import SennaTagger
from nltk.tree import ParentedTree
from nltk.stem import WordNetLemmatizer

import model.dialogue_manager.sentence_parser as parser
import model.dialogue_manager.content_provider as provider
import model.story_world.entities as Entity
import model.story_world.story_scenes as ref

incorrect = False
question = True
gotHints = False
first = True
followUp = False
answerList = []
hintList = []
result = []
compMessage = [""]
wrongMessage = [""]
correctAnswer = ()


def guessesExhausted():
    global incorrect
    global question
    global gotHints
    global compMessage
    global first
    global followUp

    first = True
    incorrect = False
    question = True
    gotHints = False
    followUp = True
    compMessage = [""]


def gotCorrectAnswer(preparedString, followUpSent):
    global incorrect
    global question
    global gotHints
    global result
    global wrongMessage
    global compMessage
    global first
    global followUp

    first = True
    incorrect = False
    question = False
    gotHints = False
    followUp = True
    wrongMessage = [""]
    compMessage = [""]

    result = []
    result.append(preparedString + followUpSent)


def resetWrongMessage():
    message = ["I don't think that's the answer, but you can try again. ",
               "I don't think that's the answer. Let's try getting the right answer together. ",
               "I don't think that's the answer. Let's try again! "]

    return message


def cleanList(answerList):
    for entries in answerList:
        temp = entries
        ansType, ansList = entries

        if not ansList:
            answerList.remove(temp)

        else:
            for answer in ansList:
                if not answer:
                    answerList.remove(temp)

    return answerList


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


def find_matches(list_keys, list_pos):
    list_match = [x for x in list_pos if x[0] in list_keys]
    dict_index = {}
    for x in list_match:
        dict_index[x[0]] = find_index_with_duplicates(list_pos, x)
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
    t = SennaTagger('C:/Senna')
    tags = ["NNP", "NNS", "NNPS"]
    processed_message = combine_similar(t.tag(sequence), tags)

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


def determineSentenceType(sequence):
    global incorrect
    global question
    global gotHints
    global first
    global answerList
    global hintList
    global finalHintList
    global result
    global compMessage
    global wrongMessage
    global followUp

    wnl = WordNetLemmatizer()

    print("sequence: ", sequence)
    beg = sequence[0][0]
    posList = [x for x, y in enumerate(sequence) if y[1] == "POS"]
    toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]
    ofList = [x for x, y in enumerate(sequence) if y[0] == "of"]
    andList = [x for x, y in enumerate(sequence) if y[0] == "and"]
    itemList = list(set(find_matches(Entity.itemList.keys(), sequence)))

    if toList:
        sequence = [i for i in sequence if i[0] != "the"]
        toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]

    nounTags = ["NN", "NNS", "NNP", "NNPS"]
    charList = [item[0] for item in sequence if item[1] in nounTags]

    verbTags = ["VBD", "VBZ", "VB", "VBP"]
    verbList = [item[0] for item in sequence if item[1] in verbTags]

    adjTags = ["JJ", "JJS", "JJR"]
    adjList = [item[0] for item in sequence if item[1] in adjTags]

    advTags = ["RB", "RBS", "RBR"]
    advList = [item[0] for item in sequence if item[1] in advTags]

    temp = []

    if beg == "who":
        temp.extend(parser.parseWhoMessage(sequence, posList, ofList, toList, charList))
        question = True
        followUp = False

    if beg == "where":
        temp.extend(parser.parseWhereMessage(charList, verbList))
        question = True
        followUp = False

    if beg == "what":
        temp.extend(parser.parseWhatMessage(sequence, posList, ofList, charList, andList, itemList))
        question = True
        followUp = False

    if beg == "why":
        temp.extend(parser.parseWhyMessage(charList, verbList))
        question = True
        followUp = False

    if question is True:
        answerList = []
        answerList.extend(temp)

    if question is True or followUp is True:
        result = []
        wrongMessage = [""]
        incorrect = True

        answerList = [x for x in answerList if x[0] != "unknown"]
        tempResult = []

        if not answerList:
            tempResult.extend(["I don't really know the answer to that. You can rephrase your question if you want?",
                               "I'm sorry but, I don't really know the answer to your question",
                               "I don't really know the answer to that. But you can ask me other questions."])

            result.append(random.choice(tempResult))
            guessesExhausted()

        if answerList:
            question = False

            if gotHints is False:
                hintList = []
                finalHintList = []
                wrongMessage = [""]
                incorrect = True

                answerList = cleanList(answerList)

                # r = [x for x in answerList if x[0] == "cause"]
                # answerList = [x for x in answerList if x[0] != "cause"]
                # for entries in r:
                #     ansType, ansList = entries
                #     answerList.extend(ansList)

                print("answerList: ", answerList)

                for entries in answerList:
                    ansType, ansList = entries
                    print("ansType: ", ansType)
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
                        print("hintChoices: ", hintChoices)

                        hintList.extend(["I think " + entries for entries in hintChoices])

                    elif ansType == "type":
                        hintChoices.extend(provider.generateHintForType(ansList))

                        hintList.extend(hintChoices)

                    elif ansType == "item_appearance":
                        hintChoices.extend(provider.generateElabForItem(ansList))
                        hintChoices.extend(provider.generatePumpForItem(ansList))

                        hintList.extend(hintChoices)

                    elif ansType == "item_amount":
                        a = 1

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

                gotHints = True

    if (question is False or followUp is True) and incorrect is True:
        wrongMessage = resetWrongMessage()
        for answers in answerList:
            ansType, ansList = answers

            if ansType == "relationship_name":
                actor, rel, char = ansList
                answer = provider.formatMultipleItems(rel)
                if charList:
                    for character in charList:
                        if char[0].name.lower() == character:
                            sentence_answer = char.name + " is " + actor.name + "'s " + answer
                            generateFollowUp(sentence_answer, "relationship_name", ansList)

            elif ansType == "relationship_rel":
                actor, rel, char = ansList
                if type(rel) is not str:
                    pluralList = [x + "s" for x in rel]
                    answer = list(set(rel) & set(charList))
                    pluralAnswer = list(set(pluralList) & set(charList))

                    if answer:
                        answer = provider.formatMultipleItems(answer)
                        sentence_answer = char.name + " is " + actor.name + "'s " + answer
                        generateFollowUp(sentence_answer, "relationship_rel", ansList)

                    elif pluralAnswer:
                        pluralAnswer = provider.formatMultipleItems(pluralAnswer)
                        sentence_answer = char.name + " is " + actor.name + "'s " + pluralAnswer
                        generateFollowUp(sentence_answer, "relationship_rel", ansList)

                elif type(rel) is str:
                    if charList:
                        for character in charList:
                            if rel == character or rel + "s" == character:
                                generateFollowUp(character, "relationship_rel", ansList)

            elif ansType == "location":
                actor, action, loc = ansList
                if charList:
                    for character in charList:
                        if character in loc.lower():
                            sentence_answer = actor.name + " " + action + " at " + loc
                            generateFollowUp(sentence_answer, "location", ansList)

            elif ansType == "appProperty":
                actor, prop = ansList

                if adjList:
                    for adjective in adjList:
                        for entries in prop:
                            if entries == adjective:
                                sentence_answer = actor.name + " is " + entries
                                generateFollowUp(sentence_answer, "appProperty", ansList)

                if advList:
                    for adverb in advList:
                        for entries in prop:
                            if entries == adverb:
                                sentence_answer = actor.name + " is " + entries
                                generateFollowUp(sentence_answer, "appProperty", ansList)

            elif ansType == "cause":
                for entries in ansList:
                    ansType, answers = entries

                    if ansType == "action":
                        actor, act, out_obj, get_ans = answers
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
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]

                        for verb in act[1]:
                            if verb in sentence:
                                verbPresent = True

                        act = provider.determineVerbForm(actor, act[0], "past")

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = actor.name + " " + act + " " + out_obj
                            generateFollowUp(sentence_answer, "action", answers)

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
                            generateFollowUp(sentence_answer, "desire", answers)

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
                            sentence_answer = actor.name + " is " + out_state
                            generateFollowUp(sentence_answer, "state", answers)

                    elif ansType == "location":
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
                            sentence_answer = actor.name + " " + action + " at " + loc
                            generateFollowUp(sentence_answer, "location", answers)

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
                            sentence_answer = actor.name + " looks " + out_prop
                            generateFollowUp(sentence_answer, "actor_appearance", answers)

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
                            sentence_answer = actor.name + " is " + out_prop
                            generateFollowUp(sentence_answer, "actor_personality", answers)

                    elif ansType == "attribute":
                        actor, act, attr, propType, out_prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        if out_prop:
                            givenAnswers.extend(out_prop)
                        givenAnswers.extend(attr.split())
                        givenAnswers = [x.lower() for x in givenAnswers]
                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
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

                            generateFollowUp(sentence_answer, "attribute", answers)

            elif ansType == "item_appearance":
                actor, act, item, prop = ansList

                givenAnswers = []
                givenAnswers.append(item)
                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                out_prop = provider.formatMultipleItems(prop)

                verbPresent = False

                givenAnswers = [x.lower() for x in givenAnswers]
                print("sequence: ", sequence)

                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]

                print("sentence: ", sentence)
                print("givenAnswers: ", givenAnswers)

                act = provider.determineVerbForm(actor, act[0], "past")

                if set(sentence).issuperset(set(givenAnswers)):
                    sentence_answer = actor.name + " " + act + " a " + item + " that looks " + out_prop
                    print("here!")
                    generateFollowUp(sentence_answer, "item_appearance", answers)

            elif ansType == "item_amount":
                a = 1

            elif ansType == "action":
                actor, act, out_obj = ansList
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
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]

                for verb in act[1]:
                    if verb in sentence:
                        verbPresent = True

                act = provider.determineVerbForm(actor, act[0], "past")

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    sentence_answer = actor.name + " " + act + " " + out_obj
                    generateFollowUp(sentence_answer, "action", ansList)

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
                    generateFollowUp(sentence_answer, "desire", ansList)

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
                    generateFollowUp(sentence_answer, "state", ansList)

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
                    generateFollowUp(sentence_answer, "actor_appearance", ansList)

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
                    generateFollowUp(sentence_answer, "actor_personality", ansList)

            elif ansType == "attribute":
                actor, act, attr, propType, out_prop = ansList

                givenAnswers = []
                givenAnswers.extend([actor.name])
                if out_prop:
                    givenAnswers.extend(out_prop)
                givenAnswers.extend(attr.split())
                givenAnswers = [x.lower() for x in givenAnswers]
                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
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

                    generateFollowUp(sentence_answer, "attribute", ansList)

            elif ansType == "type":
                a = 1

    if gotHints is True and incorrect is True:
        result = []
        if finalHintList != [[]] and finalHintList != []:
            r = random.choice(finalHintList)
            finalHintList.remove(r)

            if first is True:
                result.append(random.choice(compMessage) + r)
                first = False
            else:
                result.append(random.choice(wrongMessage) + r)

        else:
            for answers in answerList:
                ansType, ansList = answers

                if ansType == "relationship_name":
                    actor, rel, char = ansList

                    out = provider.formatMultipleItems(rel)

                    result.append("I think " + actor.name.title() + "'s " + out + " is " + char[0].name.title() + ".")
                    guessesExhausted()

                if ansType == "relationship_rel":
                    actor, rel, char = ansList

                    out = provider.formatMultipleItems(rel)

                    result.append("I think " + char.name.title() + " is " + actor.name.title() + "'s " + out + ".")
                    guessesExhausted()

                if ansType == "location":
                    actor, action, loc = ansList

                    result.append("I think " + actor.name.title() + " " + action + " in " + loc + ".")
                    guessesExhausted()

                if ansType == "state":
                    actor, action, loc = ansList

                    result.append("I think " + actor.name.title() + " is " + action + " in " + loc + ".")
                    guessesExhausted()

                elif ansType == "cause":
                    for entries in ansList:
                        ansType, answers = entries

                        if ansType == "action":
                            actor, act, out_obj, get_ans = answers
                            act = provider.determineVerbForm(actor, act[0], "past")

                            result.append(actor.name + " " + act + " " + out_obj)
                            guessesExhausted()

                        elif ansType == "desire":
                            actor, act, out_obj, get_ans = answers
                            act = provider.determineVerbForm(actor, act[0], "past")

                            result.append(actor.name + " desired to " + act + " " + out_obj)
                            guessesExhausted()

                        elif ansType == "state":
                            actor, out_state, get_ans = answers

                            result.append(actor.name + " is " + out_state)
                            guessesExhausted()

                        elif ansType == "location":
                            actor, action, loc, get_ans = answers
                            action = provider.determineVerbForm(actor, action[0], "past")

                            result.append(actor.name + " " + action + " at " + loc)
                            guessesExhausted()

                        elif ansType == "actor_appearance":
                            actor, prop, get_ans = answers
                            out_prop = provider.formatMultipleItems(prop)

                            result.append(actor.name + " looks " + out_prop)
                            guessesExhausted()

                        elif ansType == "actor_personality":
                            actor, prop, get_ans = answers
                            out_prop = provider.formatMultipleItems(prop)

                            result.append(actor.name + " is " + out_prop)
                            guessesExhausted()

                        elif ansType == "attribute":
                            actor, act, attr, propType, out_prop, get_ans = answers
                            act = provider.determineVerbForm(actor, act[0], "past")

                            if out_prop:
                                sent_prop = provider.formatMultipleItems(out_prop)
                                sent_add = " that is "
                            else:
                                sent_prop = ""
                                sent_add = ""

                            if propType == "amount":
                                result.append(actor.name + " " + act + " " + sent_prop + " " + attr)
                                guessesExhausted()
                            else:
                                result.append(actor.name + " " + act + " " + attr + sent_add + sent_prop)
                                guessesExhausted()

                elif ansType == "item_appearance":
                    actor, act, item, prop = ansList

                    out_prop = provider.formatMultipleItems(prop)
                    act = provider.determineVerbForm(actor, act[0], "past")

                    result.append(actor.name + " " + act + " a " + item + " that is " + out_prop + ".")
                    guessesExhausted()

                elif ansType == "item_amount":
                    a = 1

                elif ansType == "action":
                    actor, act, out_obj = ansList

                    act = provider.determineVerbForm(actor, act[0], "past")

                    result.append(actor.name + " " + act + " " + out_obj)
                    guessesExhausted()

                elif ansType == "desire":
                    actor, act, out_obj = ansList

                    act = provider.determineVerbForm(actor, act[0], "past")

                    result.append(actor.name + " desired to " + act + " " + out_obj)
                    guessesExhausted()

                elif ansType == "state":
                    actor, out_state = ansList

                    result.append(actor.name + " is " + out_state)
                    guessesExhausted()

                elif ansType == "location":
                    actor, action, loc = ansList

                    action = provider.determineVerbForm(actor, action[0], "past")

                    result.append(actor.name + " " + action + " at " + loc)
                    guessesExhausted()

                elif ansType == "actor_appearance":
                    actor, prop = ansList

                    out_prop = provider.formatMultipleItems(prop)

                    result.append(actor.name + " looks " + out_prop)
                    guessesExhausted()

                elif ansType == "actor_personality":
                    actor, prop = ansList

                    out_prop = provider.formatMultipleItems(prop)

                    result.append(actor.name + " is " + out_prop)
                    guessesExhausted()

                elif ansType == "attribute":
                    actor, act, attr, propType, out_prop = ansList

                    act = provider.determineVerbForm(actor, act[0], "past")

                    if propType == "amount":
                        result.append(actor.name + " " + act + " " + sent_prop + " " + attr)
                        guessesExhausted()
                    else:
                        result.append(actor.name + " " + act + " " + attr + sent_add + sent_prop)
                        guessesExhausted()

    elif gotHints is False and incorrect is True:
        result = []

    if result:
        print("result: ", result)
        if len(result) > 1:
            return "; ".join(result[:-1]) + " and " + result[len(result) - 1]

        elif len(result) == 1:
            return result[0]
    else:
        return "Try asking me a question."


def generateFollowUp(answer, questType, ansList):
    global answerList
    global result
    global correctAnswer
    praiseChoices = []

    praiseChoices.extend(["Hooray! I also think ",
                          "You got it! "])

    if questType == "relationship_name":
        actor, rel, char = ansList

        try:
            perProp = Entity.charList[actor.name.lower()].perProp
            appProp = Entity.charList[actor.name.lower()].appProp
        except Exception as e:
            # print("Error: ", e)
            a = 1

        if perProp:
            current = random.choice(perProp)
            personality, event = current
            personality = ref.provider.formatMultipleItems(personality)

            if event is not None:
                followUpResult = ref.queryRelations("Wednesday3inf10", "cause")
                answerList = []

                if not followUpResult:
                    perProp.remove(current)

                else:
                    if type(followUpResult) is list:
                        for entries in followUpResult:
                            answerList.append(provider.assembleSentence(entries))

                    else:
                        answerList.append(provider.assembleSentence(followUpResult))

                    r = random.choice(praiseChoices)
                    preparedString = r + answer + "."
                    followUpSent = " Why do you think is " + actor.name.title() + " " + personality + "?"

                    correctAnswer = (actor, personality)
                    gotCorrectAnswer(preparedString, followUpSent)

    elif questType == "location" or questType == "relationship_rel":
        r = random.choice(praiseChoices)
        preparedString = r + answer + "."
        gotCorrectAnswer(preparedString, " Blah")

    elif questType == "actor_appearance":
        if correctAnswer:
            actor, personality = correctAnswer

            r = random.choice(praiseChoices)
            preparedString = r + actor.name.title() + " is " + personality + " because " + answer + "."
            gotCorrectAnswer(preparedString, " Blah")

    elif questType == "item_appearance":
        r = random.choice(praiseChoices)
        preparedString = r + answer + "."
        gotCorrectAnswer(preparedString, " Blah")


def parse_message(message):
    r = CoreNLPParser('http://localhost:9000/')
    t = nltk.word_tokenize(message)
    user_input = ParentedTree.convert(list(r.raw_parse(message))[0])

    user_input.pretty_print()

    messages = []
    messages = [split_compound(user_input, 0, messages)][0]

    if not messages:
        messages.append(single_sentence(t))

    if len(messages) > 1:
        output_message = " ".join(messages)
    else:
        output_message = messages[0]

    return output_message
