import random

import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag.stanford import CoreNLPParser
from nltk.tree import ParentedTree

import model.dialogue_manager.content_provider as provider
import model.dialogue_manager.sentence_parser as parser
import model.story_world.entities as Entity
import model.story_world.story_scenes as ref

import model.story_world.classes.Item as item_type
import model.story_world.classes.Character as char_type

incorrect = True
question = False
gotHints = False
first = True
flip = True
skip = False
lock = False
regSentence = True
guessesNotExhausted = True
answerList = []
finalHintList = []
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
    global finalHintList
    global flip
    global skip
    global guessesNotExhausted
    global regSentence
    global lock

    first = True
    incorrect = False
    question = False
    regSentence = True
    gotHints = False
    flip = True
    skip = True
    lock = False
    compMessage = [""]
    finalHintList = []
    guessesNotExhausted = False


def gotCorrectAnswer(preparedString, followUpSent):
    global incorrect
    global question
    global regSentence
    global gotHints
    global result
    global wrongMessage
    global compMessage
    global first
    global guessesNotExhausted
    global skip
    global lock

    first = True
    incorrect = True
    question = False
    regSentence = False
    gotHints = True
    skip = False
    lock = False
    guessesNotExhausted = True
    wrongMessage = [""]
    compMessage = [""]

    result = []
    result.append(preparedString + followUpSent)


def resetWrongMessage():
    message = ["I don't think that's the answer, but you can try again. ",
               "Let's try getting the right answer together. ",
               "Let's try again! "]

    return message


def cleanList(inputList):
    # global answerList

    for entries in inputList:
        temp = entries
        ansType, ansList = entries

        if not ansList:
            inputList.remove(temp)

        else:
            if type(ansList) is list:
                for answer in ansList:
                    if not answer:
                        try:
                            inputList.remove(temp)
                        except Exception as e:
                            print("Error in cleanList: ", e)
            elif not ansList:
                inputList.remove(temp)

    return inputList


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
            compMessage = ["Let us talk about your first statement for now.",
                           "We should focus on what you said first.",
                           "Let's focus on your first statement? Ok so,",
                           "Hey, let's focus on what you said first."]

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

        # elif ansType == "appProperty":
        #     hintChoices.extend(provider.generateHintForAppProp(ansList))
        #     hintChoices.extend(provider.generatePumpForAppProp(ansList))
        #     hintChoices.extend(provider.generatePromptForAppProp(correctAnswer))
        #
        #     if hintChoices:
        #         if len(hintChoices) > 5:
        #             i = 0
        #             temp = []
        #             while i < 5:
        #                 r = random.choice(hintChoices)
        #                 hintChoices.remove(r)
        #                 temp.append(r)
        #                 i = i + 1
        #
        #             hintList.extend(temp)
        #
        #         else:
        #             hintList.extend(hintChoices)

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
            hintChoices.extend(provider.generatePumpForItem(ansList))
            hintChoices.extend(provider.generatePromptForItem(ansList))
            hintChoices.extend(provider.generateHintForItem(ansList))
            hintChoices.extend(provider.generateElabForItem(ansList))

            hintList.extend(hintChoices)

        elif ansType == "item_amount":
            hintChoices.extend(provider.generatePumpForAmtItem(ansList))
            hintChoices.extend(provider.generatePromptForAmtItem(ansList))

            hintList.extend(hintChoices)

        elif ansType == "actor_appearance":
            hintChoices.extend(provider.generatePumpForAppearance(ansList))
            hintChoices.extend(provider.generateElabForAppearance(ansList))

            hintList.extend(["I think " + entries for entries in hintChoices])

        elif ansType == "actor_personality":
            hintChoices.extend(provider.generatePumpForPersonality(ansList))
            hintChoices.extend(provider.generateElabForPersonality(ansList))

            hintList.extend(["I think " + entries for entries in hintChoices])

        elif ansType == "confirmation":
            hintList.append("Do you mean " + ansList.name.title() + "?")
            guessesNotExhausted = False

    if hintList:
        if len(hintList) > 3:
            i = 0
            while i < 3:
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

    response = "i do n't want to talk anymore"
    user_response = " ".join([x[0].lower() for x in sequence][:7])

    if user_response == response:
        tempResult.extend(["I see", "Okay"])
        result.append(random.choice(tempResult) + ". I'll just be here if you need me.")

        guessesExhausted()
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
    global flip
    global skip
    global guessesNotExhausted
    global lock

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
        if len(wordnet.synsets(items)) > 0 and provider.getCommonPartOfSpeech(items) == 'v':
            verbList.append(items)

    stop(sequence)

    # print("question: ", question, "incorrect: ", incorrect, "guessesNotExhausted: ", guessesNotExhausted, "gotHints: ", gotHints)

    if beg == "who" and end == "?" and lock is False:
        dummyAnswer = parser.parseWhoMessage(sequence, posList, ofList, toList, charList)

        dummyAnswer = cleanList(dummyAnswer)

        if dummyAnswer:
            lock = True
            for entries in dummyAnswer:
                if entries[1]:
                    ansType, ansList = entries

                    if ansType == "relationship_name":
                        actor, rel, char = ansList
                        answer = provider.formatMultipleItems(rel)
                        verb = " is "

                        if char:
                            if type(char) is list and len(char) > 1:
                                char = [x.name for x in char]
                                char_answer = ", ".join(char[:-1]) + " and " + char[len(char) - 1]
                                verb = " are "
                                answer = answer + "s"
                            elif type(char) is list and len(char) == 1:
                                char_answer = char[0].name
                            else:
                                char_answer = char.name

                            sentence_answer = char_answer + verb + actor.name + "'s " + answer

                            generateFollowUp(sentence_answer, "rel", specialAnswer=actor)

                    if ansType == "relationship_rel":
                        actor, rel, char = ansList
                        answer = provider.formatMultipleItems(rel)
                        verb = " is "

                        if char:
                            if type(char) is list and len(char) > 1:
                                char = [x.name for x in char]
                                char_answer = ", ".join(char[:-1]) + " and " + char[len(char) - 1]
                                verb = " are "
                                answer = answer + "s"
                            elif type(char) is list and len(char) == 1:
                                char_answer = char[0].name
                            else:
                                char_answer = char.name

                            sentence_answer = char_answer + verb + actor.name + "'s " + answer

                            generateFollowUp(sentence_answer, "rel", specialAnswer=actor)

                    if ansType == "type":
                        actor, charType = ansList
                        answer = provider.formatMultipleItems(charType)
                        verb = " is a "

                        sentence_answer = actor.name.title() + verb + answer

                        generateFollowUp(sentence_answer, "type", specialAnswer=None)

                    if ansType == "confirmation":
                        sentence_answer = "Did you mean " + ansList.name + "?"

                        generateFollowUp(sentence_answer, "confirmation", specialAnswer=None)

        else:
            getRandomEvent("who", sequence=sequence, posList=posList, ofList=ofList, toList=toList)

    elif beg == "where" and end == "?" and lock is False:
        dummyAnswer = parser.parseWhereMessage(charList, verbList)

        dummyAnswer = cleanList(dummyAnswer)

        if dummyAnswer:
            lock = True
            for entries in dummyAnswer:
                if entries[1]:
                    ansType, ansList = entries

                    actor, act, location = ansList

                    if type(location) is str:
                        location = location
                    else:
                        location = location.name

                    act = wnl.lemmatize(act, 'v')
                    event = actor.queryLocation(act, location, None)[2]
                    sent_act = provider.determineVerbForm(actor, act, "past")
                    sentence = "I think " + actor.name + " " + sent_act + " at " + location
                    specAns = (actor, act, location, None, None)

                    generateFollowUp(sentence, ansType, exhausted="yes", event=event, specialAnswer=specAns)

        else:
            getRandomEvent("where", verbList=verbList)

    elif beg == "what" and end == "?" and lock is False:
        dummyAnswer = parser.parseWhatMessage(sequence, posList, ofList, charList, andList, itemList)

        dummyAnswer = cleanList(dummyAnswer)

        if dummyAnswer:
            lock = True
            temp.extend(dummyAnswer)
            question = True
            regSentence = False
            gotHints = False
            guessesNotExhausted = True
            skip = True

        else:
            getRandomEvent("what", sequence=sequence, posList=posList, ofList=ofList, andList=andList, itemList=itemList)

    elif beg == "why" and end == "?" and lock is False:
        dummyAnswer = parser.parseWhyMessage(charList, charList, verbList, advList, itemList, adjList)

        dummyAnswer = cleanList(dummyAnswer)

        if dummyAnswer:
            lock = True
            temp.extend(dummyAnswer)
            question = True
            gotHints = False
            regSentence = False
            guessesNotExhausted = True
            skip = True

        else:
            print("random event")
            getRandomEvent("why", verbList=verbList, advList=advList, itemList=itemList, adjList=adjList, objList=charList)

    if len(sequence) > 3 and end == "." and regSentence is True and \
            not set([x[0].lower() for x in sequence]).issuperset(set("i do n't want to talk anymore".split(" "))):
        tempResult.extend(["I see.", "Tell me more.", "Okay."])
        result.append(random.choice(tempResult))

        guessesExhausted()
        skip = False

    elif len(sequence) <= 3 and end == "." and regSentence is True:
        generateFollowUp(None, None)
        regSentence = False

    if question is True and gotHints is False and guessesNotExhausted is True:
        answerList = []
        answerList.extend(temp)
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

            # populate hints
            wrongMessage = [""]
            incorrect = True

            answerList = cleanList(answerList)
            populateDialogueTurns()
            gotHints = True

    # check answer
    if question is False and incorrect is True and guessesNotExhausted is True:
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

            # elif ansType == "appProperty":
            #     actor, prop = ansList
            #
            #     if adjList:
            #         for adjective in adjList:
            #             for entries in prop:
            #                 if entries == adjective:
            #                     sentence_answer = actor.name + " is " + entries
            #                     generateFollowUp(sentence_answer, "appProperty")
            #
            #     if advList:
            #         for adverb in advList:
            #             for entries in prop:
            #                 if entries == adverb:
            #                     sentence_answer = actor.name + " is " + entries
            #                     generateFollowUp(sentence_answer, "appProperty")a

            elif ansType == "cause":
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
                        getActorName = get_actor
                    else:
                        getActorName = get_actor.name
                        if type(get_actor) is char_type.Character:
                            if get_actor.gender == "collective":
                                getActorName = "the " + getActorName
                        elif type(get_actor) is item_type.Item:
                            if getActorName.endswith("s"):
                                getActorName = "the " + getActorName
                        else:
                            getActorName = get_actor

                    sentence_answer = getActorName + " " + get_act + " " + get_obj + " because "

                    if ansType == "action":
                        actor, act, out_obj, propType, prop, get_ans = answers
                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        givenAnswers.extend([wnl.lemmatize(x) for x in out_obj.split(" ")])
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

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            elif type(actor) is item_type.Item:
                                if getActorName.endswith("s"):
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actorName + " " + act + " " + out_obj
                            generateFollowUp(sentence_answer, "action")

                    elif ansType == "desire":
                        actor, act, out_obj, get_ans = answers
                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        givenAnswers.extend([wnl.lemmatize(x) for x in out_obj.split(" ")])
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

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actorName + " desired to " + act + " " + out_obj
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

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            elif type(actor) is item_type.Item:
                                if getActorName.endswith("s"):
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        state = " " + provider.determineVerbForm(actor, out_state[0], "past")
                        if len(wordnet.synsets(out_state[0])) > 0 and provider.getCommonPartOfSpeech(out_state[0]) == 'a':
                            state = " " + provider.determineVerbForm(actor, "be", "past") + out_state[0]

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actorName + state
                            generateFollowUp(sentence_answer, "state")

                    elif ansType == "location":
                        actor, action, loc, get_ans = answers
                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        givenAnswers.extend(loc.split(" "))
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

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            sentence_answer = sentence_answer + actorName + " " + action + " at " + loc
                            generateFollowUp(sentence_answer, "location")

                    elif ansType == "actor_appearance":
                        actor, prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.append(actor.name)
                        if type(prop) is list:
                            givenAnswers.extend(prop)
                        else:
                            givenAnswers.append(prop)

                        givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                        givenAnswers = [item for sublist in givenAnswers for item in sublist]
                        out_prop = provider.formatMultipleItems(prop)

                        formatted_seq = []
                        for words in sequence:
                            if words[1] not in verbTags:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq][:-1]

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        appearance = provider.determineVerbForm(actor, "look", "present")

                        if set(sentence).issubset(set(givenAnswers)):
                            sentence_answer = sentence_answer + actorName + " " + appearance + " " + out_prop
                            generateFollowUp(sentence_answer, "actor_appearance")

                    elif ansType == "actor_personality":
                        actor, prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.append(actor.name)
                        if type(prop) is list:
                            givenAnswers.extend(prop)
                        else:
                            givenAnswers.append(prop)

                        givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                        givenAnswers = [item for sublist in givenAnswers for item in sublist]

                        out_prop = provider.formatMultipleItems(prop)

                        formatted_seq = []
                        for words in sequence:
                            if words[1] not in verbTags:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq][:-1]

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        personality = provider.determineVerbForm(actor, "be", "present")

                        if set(sentence).issubset(set(givenAnswers)):
                            sentence_answer = sentence_answer + actorName + " " + personality + " " + out_prop
                            generateFollowUp(sentence_answer, "actor_personality")

                    elif ansType == "attribute":
                        actor, act, attr, propType, out_prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.extend([actor.name])
                        if out_prop:
                            givenAnswers.extend([out_prop])
                        givenAnswers.extend([wnl.lemmatize(x) for x in attr.split(" ")])

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

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            elif type(actor) is item_type.Item:
                                if getActorName.endswith("s"):
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                            if propType == "amount":
                                sentence_answer = sentence_answer + actorName + " " + act + " " + sent_prop + " " + attr
                            else:
                                sentence_answer = sentence_answer + actorName + " " + act + " " + attr + sent_add + sent_prop

                            generateFollowUp(sentence_answer, "attribute")

                    elif ansType == "item_appearance":
                        actor, act, item, prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.append(wnl.lemmatize(item.name))

                        if type(prop) is list:
                            givenAnswers.extend(prop)
                        else:
                            givenAnswers.append(prop)

                        out_prop = provider.formatMultipleItems(prop)

                        givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                        givenAnswers = [item for sublist in givenAnswers for item in sublist]

                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                            elif words[1] in nounTags:
                                formatted_seq.append(wnl.lemmatize(words[0]))
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]

                        act = provider.determineVerbForm(actor, act[0], "past")

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            elif type(actor) is item_type.Item:
                                if getActorName.endswith("s"):
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        if set(sentence).issuperset(set(givenAnswers)):
                            sentence_answer = actorName + " " + act + " a " + item.name + " that looks " + out_prop
                            generateFollowUp(sentence_answer, "item_appearance")

                    elif ansType == "item_amount":
                        actor, act, item, prop, get_ans = answers

                        givenAnswers = []
                        givenAnswers.append(wnl.lemmatize(item.name))

                        if type(prop) is list:
                            givenAnswers.extend(prop)
                        else:
                            givenAnswers.append(prop)

                        out_prop = provider.formatMultipleItems(prop)

                        givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                        givenAnswers = [item for sublist in givenAnswers for item in sublist]

                        formatted_seq = []
                        for words in sequence:
                            if words[1] in verbTags:
                                formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                            elif words[1] in nounTags:
                                formatted_seq.append(wnl.lemmatize(words[0]))
                            else:
                                formatted_seq.append(words[0])

                        sentence = [x.lower() for x in formatted_seq]

                        act = provider.determineVerbForm(actor, act[0], "past")

                        if type(actor) is str:
                            actorName = actor
                        else:
                            actorName = actor.name
                            if type(actor) is char_type.Character:
                                if actor.gender == "collective":
                                    actorName = "the " + actorName
                            elif type(actor) is item_type.Item:
                                if getActorName.endswith("s"):
                                    actorName = "the " + actorName
                            else:
                                actorName = actor

                        if set(sentence).issuperset(set(givenAnswers)):
                            sentence_answer = actorName + " " + act + " " + out_prop + " " + item.name
                            generateFollowUp(sentence_answer, "item_amount")

            elif ansType == "item_appearance":
                actor, act, item, prop = ansList

                givenAnswers = []
                givenAnswers.append(wnl.lemmatize(item.name))

                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                out_prop = provider.formatMultipleItems(prop)
                givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                givenAnswers = [item for sublist in givenAnswers for item in sublist]

                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    elif words[1] in nounTags:
                        formatted_seq.append(wnl.lemmatize(words[0]))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]

                act = provider.determineVerbForm(actor, act[0], "past")

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    elif type(actor) is item_type.Item:
                        if getActorName.endswith("s"):
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                if set(sentence).issuperset(set(givenAnswers)):
                    sentence_answer = actorName + " " + act + " a " + item.name + " that looks " + out_prop
                    generateFollowUp(sentence_answer, "item_appearance")

            elif ansType == "item_amount":
                actor, act, item, prop = ansList

                givenAnswers = []
                givenAnswers.append(wnl.lemmatize(item.name))

                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                out_prop = provider.formatMultipleItems(prop)
                givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                givenAnswers = [item for sublist in givenAnswers for item in sublist]

                formatted_seq = []
                for words in sequence:
                    if words[1] in verbTags:
                        formatted_seq.append(wnl.lemmatize(words[0], 'v'))
                    elif words[1] in nounTags:
                        formatted_seq.append(wnl.lemmatize(words[0]))
                    else:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq]

                act = provider.determineVerbForm(actor, act[0], "past")

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    elif type(actor) is item_type.Item:
                        if getActorName.endswith("s"):
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                if set(sentence).issuperset(set(givenAnswers)):
                    sentence_answer = actorName + " " + act + " " + out_prop + " " + item.name
                    generateFollowUp(sentence_answer, "item_amount")

            elif ansType == "action":
                actor, act, out_obj, propType, prop = ansList
                givenAnswers = []
                givenAnswers.extend([actor.name])
                givenAnswers.extend([wnl.lemmatize(x) for x in out_obj.split(" ")])
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

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    elif type(actor) is item_type.Item:
                        if getActorName.endswith("s"):
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    sentence_answer = actorName + " " + act + " " + out_obj
                    generateFollowUp(sentence_answer, "action")

            elif ansType == "desire":
                actor, act, out_obj = ansList
                givenAnswers = []
                givenAnswers.extend([actor.name])
                givenAnswers.extend([wnl.lemmatize(x) for x in out_obj.split(" ")])
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

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    sentence_answer = actorName + " desired to " + act + " " + out_obj
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

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    elif type(actor) is item_type.Item:
                        if getActorName.endswith("s"):
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                state = " " + provider.determineVerbForm(actor, out_state[0], "past")
                if len(wordnet.synsets(out_state[0])) > 0 and provider.getCommonPartOfSpeech(out_state[0]) == 'a':
                    state = " " + provider.determineVerbForm(actor, "be", "past") + out_state[0]

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    sentence_answer = actorName + " is " + state
                    generateFollowUp(sentence_answer, "state")

            elif ansType == "actor_appearance":
                actor, prop = ansList

                givenAnswers = []
                givenAnswers.append(actor.name)
                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                givenAnswers = [item for sublist in givenAnswers for item in sublist]
                out_prop = provider.formatMultipleItems(prop)

                formatted_seq = []
                for words in sequence:
                    if words[1] not in verbTags:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq][:-1]

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    elif type(actor) is item_type.Item:
                        if getActorName.endswith("s"):
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                appearance = provider.determineVerbForm(actor, "look", "present")

                if set(sentence).issubset(set(givenAnswers)):
                    sentence_answer = actorName + " " + appearance +  " " + out_prop
                    generateFollowUp(sentence_answer, "actor_appearance")

            elif ansType == "actor_personality":
                actor, prop = ansList

                givenAnswers = []
                givenAnswers.append(actor.name)
                if type(prop) is list:
                    givenAnswers.extend(prop)
                else:
                    givenAnswers.append(prop)

                givenAnswers = [x.lower().split(" ") for x in givenAnswers]
                givenAnswers = [item for sublist in givenAnswers for item in sublist]
                out_prop = provider.formatMultipleItems(prop)

                formatted_seq = []
                for words in sequence:
                    if words[1] not in verbTags:
                        formatted_seq.append(words[0])

                sentence = [x.lower() for x in formatted_seq][:-1]

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    elif type(actor) is item_type.Item:
                        if getActorName.endswith("s"):
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                personality = provider.determineVerbForm(actor, "be", "present")

                print("sentence: ", sentence)
                print("givenAnsers: ", givenAnswers)
                print(set(sentence).issubset(set(givenAnswers)))
                if set(sentence).issubset(set(givenAnswers)):
                    sentence_answer = actorName + " " + personality + " " + out_prop
                    generateFollowUp(sentence_answer, "actor_personality")

            elif ansType == "attribute":
                actor, act, attr, propType, out_prop = ansList

                givenAnswers = []
                givenAnswers.extend([actor.name])
                if out_prop:
                    givenAnswers.extend([out_prop])
                    givenAnswers.extend([wnl.lemmatize(x) for x in attr.split(" ")])
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

                if type(actor) is str:
                    actorName = actor
                else:
                    actorName = actor.name
                    if type(actor) is char_type.Character:
                        if actor.gender == "collective":
                            actorName = "the " + actorName
                    elif type(actor) is item_type.Item:
                        if getActorName.endswith("s"):
                            actorName = "the " + actorName
                    else:
                        actorName = actor

                if set(sentence).issuperset(set(givenAnswers)) and verbPresent:
                    if propType == "amount":
                        sentence_answer = actorName + " " + act + " " + sent_prop + " " + attr
                    else:
                        sentence_answer = actorName + " " + act + " " + attr + sent_add + sent_prop

                    generateFollowUp(sentence_answer, "attribute")

            elif ansType == "type":
                a = 1

    if gotHints is True and incorrect is True and guessesNotExhausted is True:
        sentences = []

        if skip:
            # take hints to give
            if finalHintList != [[]] and finalHintList != []:
                r = random.choice(finalHintList)
                finalHintList.remove(r)
                
                if first is True:
                    result.append(random.choice(compMessage) + r)
                    first = False
                else:
                    if beg == "where":
                        sentence_answer = "Where do you think so? "

                    elif beg == "who":
                        sentence_answer = "Who do you think is that person? "

                    elif beg == "why":
                        sentence_answer = "Why do you think so? "

                    elif beg == "what":
                        sentence_answer = "What do you think? "

                    else:
                        sentence_answer = random.choice(wrongMessage)
                        
                    result.append(sentence_answer + r)

            # give answer since guesses exhausted
            else:
                for answers in answerList:
                    ansType, ansList = answers

                    if ansType == "relationship_name":
                        actor, rel, char = ansList

                        out = provider.formatMultipleItems(rel)

                        sentences.append(
                            actor.name.title() + "'s " + out + " is " + char[0].name.title() + ".")

                    elif ansType == "relationship_rel":
                        actor, rel, char = ansList

                        out = provider.formatMultipleItems(rel)

                        sentences.append(
                            char.name.title() + " is " + actor.name.title() + "'s " + out + ".")

                    elif ansType == "state":
                        actor, out_state, get_ans = answers
                        out_state = out_state[0].replace("_", " ")

                        actorName = actor.name
                        if type(actor) is char_type.Character:
                            if actor.gender == "collective":
                                actorName = "the " + actorName
                        elif type(actor) is item_type.Item:
                            if actorName.endswith("s"):
                                actorName = "the " + actorName

                        verb = " " + provider.determineVerbForm(actor, out_state, "past")
                        if len(wordnet.synsets(out_state)) > 0 and provider.getCommonPartOfSpeech(out_state) == 'a':
                            verb = " " + provider.determineVerbForm(actor, "be", "past") + verb

                        sentences.append(actorName + verb + ".")

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

                            get_act = get_act.replace("_", " ")
                            get_act = provider.determineVerbForm(get_actor, get_act, "past")

                            if type(get_obj) is str:
                                if len(wordnet.synsets(get_obj)) > 0 and provider.getCommonPartOfSpeech(get_obj) == 'a':
                                    get_act = provider.determineVerbForm(actor, "be", "present")

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
                                act = act[0].replace("_", " ")
                                act = provider.determineVerbForm(actor, act, "past")

                                actorName = actor.name
                                if type(actor) is char_type.Character:
                                    if actor.gender == "collective":
                                        actorName = "the " + actorName
                                elif type(actor) is item_type.Item:
                                    if actorName.endswith("s"):
                                        actorName = "the " + actorName

                                temp.append(actorName + " " + act + " " + out_obj)

                            elif ansType == "desire":
                                actor, act, out_obj, get_ans = answers
                                act = act[0].replace("_", " ")

                                actorName = actor.name

                                if type(actor) is char_type.Character:
                                    if actor.gender == "collective":
                                        actorName = "the " + actorName

                                temp.append(actorName + " desired to " + act + " " + out_obj)

                            elif ansType == "state":
                                actor, out_state, get_ans = answers
                                out_state = out_state[0].replace("_", " ")

                                actorName = actor.name
                                if type(actor) is char_type.Character:
                                    if actor.gender == "collective":
                                        actorName = "the " + actorName
                                elif type(actor) is item_type.Item:
                                    if actorName.endswith("s"):
                                        actorName = "the " + actorName

                                verb = " " + provider.determineVerbForm(actor, out_state, "past")
                                if len(wordnet.synsets(out_state)) > 0 and provider.getCommonPartOfSpeech(out_state) == 'a':
                                    verb = " " + provider.determineVerbForm(actor, "be", "past") + verb

                                temp.append(actorName + verb)

                            elif ansType == "location":
                                actor, act, loc, get_ans = answers
                                act = act[0].replace("_", " ")
                                print("act: ", act)
                                sent_act = provider.determineVerbForm(actor, act, "past")
                                print("sent_act: ", sent_act)

                                temp.append(actor.name + " " + sent_act + " at " + loc)

                            elif ansType == "actor_appearance":
                                actor, prop, get_ans = answers
                                out_prop = provider.formatMultipleItems(prop)

                                actorName = actor.name
                                if type(actor) is char_type.Character:
                                    if actor.gender == "collective":
                                        actorName = "the " + actorName

                                verb = provider.determineVerbForm(actor, "look", "present")

                                temp.append(actorName + " " + verb + " " + out_prop)

                            elif ansType == "actor_personality":
                                actor, prop, get_ans = answers
                                out_prop = provider.formatMultipleItems(prop)

                                actorName = actor.name
                                if type(actor) is char_type.Character:
                                    if actor.gender == "collective":
                                        actorName = "the " + actorName

                                verb = provider.determineVerbForm(actor, "be", "present")

                                temp.append(actorName + " " + verb + " " + out_prop)

                            elif ansType == "attribute":
                                actor, act, attr, propType, out_prop, get_ans = answers
                                act = act[0].replace("_", " ")
                                act = provider.determineVerbForm(actor, act, "past")

                                actorName = actor.name
                                if type(actor) is char_type.Character:
                                    if actor.gender == "collective":
                                        actorName = "the " + actorName
                                elif type(actor) is item_type.Item:
                                    if actorName.endswith("s"):
                                        actorName = "the " + actorName

                                if out_prop:
                                    sent_prop = provider.formatMultipleItems(out_prop)
                                    sent_add = " that is "

                                if propType == "amount":
                                    temp.append(actorName + " " + act + " " + sent_prop + " " + attr)
                                else:
                                    temp.append(actorName + " " + act + " " + attr + sent_add + sent_prop)

                            elif ansType == "item_appearance":
                                actor, act, item, prop, get_ans = answers

                                out_prop = provider.formatMultipleItems(prop)
                                act = act[0].replace("_", " ")
                                act = provider.determineVerbForm(actor, act, "past")

                                temp.append(actor.name + " " + act + " a " + item.name + " that is " + out_prop)

                            elif ansType == "item_amount":
                                actor, act, item, prop, get_ans = answers

                                out_prop = provider.formatMultipleItems(prop)
                                act = act[0].replace("_", " ")
                                act = provider.determineVerbForm(actor, act, "past")

                                temp.append(actor.name + " " + act + " " + out_prop + " " + item.name)

                            getActorName = get_actor.name
                            if type(get_actor) is char_type.Character:
                                if get_actor.gender == "collective":
                                    getActorName = "the " + getActorName
                            elif type(get_actor) is item_type.Item:
                                if getActorName.endswith("s"):
                                    getActorName = "the " + getActorName

                            sentence = getActorName + " " + get_act + " " + get_obj + " because "

                        cause = provider.formatMultipleItems(temp)
                        sentences.append(sentence + cause)

                    elif ansType == "item_appearance":
                        actor, act, item, prop = ansList

                        out_prop = provider.formatMultipleItems(prop)
                        act = act[0].replace("_", " ")
                        act = provider.determineVerbForm(actor, act, "past")

                        sentences.append(actor.name + " " + act + " a " + item.name + " that is " + out_prop)

                    elif ansType == "item_amount":
                        actor, act, item, prop = ansList

                        out_prop = provider.formatMultipleItems(prop)
                        act = act[0].replace("_", " ")
                        act = provider.determineVerbForm(actor, act, "past")

                        sentences.append(actor.name + " " + act + " " + out_prop + " " + item.name)

                    elif ansType == "action":
                        actor, act, out_obj, propType, prop = ansList

                        out_obj = provider.formatMultipleItems(out_obj)
                        if propType and prop:
                            prop = provider.formatMultipleItems(prop)

                            if propType == "appearance" or propType == "personality":
                                out_obj = out_obj + " that looks " + prop
                            elif propType == "amount":
                                out_obj = prop + " " + out_obj

                        act = act[0].replace("_", " ")
                        act = provider.determineVerbForm(actor, act, "past")

                        actorName = actor.name
                        if type(actor) is char_type.Character:
                            if actor.gender == "collective":
                                actorName = "the " + actorName
                        elif type(actor) is item_type.Item:
                            if actorName.endswith("s"):
                                actorName = "the " + actorName

                        sentences.append(actorName + " " + act + " " + out_obj)

                    elif ansType == "desire":
                        actor, act, out_obj = ansList
                        act = act[0].replace("_", " ")

                        actorName = actor.name
                        if type(actor) is char_type.Character:
                            if actor.gender == "collective":
                                actorName = "the " + actorName

                        sentences.append(actorName + " desired to " + act + " " + out_obj)

                    elif ansType == "location":
                        actor, act, loc = ansList
                        act = act[0].replace("_", " ")
                        act = provider.determineVerbForm(actor, act, "past")

                        sentences.append(actor.name + " " + act + " at " + loc)

                    elif ansType == "actor_appearance":
                        actor, prop = ansList

                        out_prop = provider.formatMultipleItems(prop)

                        actorName = actor.name
                        if type(actor) is char_type.Character:
                            if actor.gender == "collective":
                                actorName = "the " + actorName

                        verb = provider.determineVerbForm(actor, "look", "present")

                        sentences.append(actorName + " " + verb + " " + out_prop)

                    elif ansType == "actor_personality":
                        actor, prop = ansList

                        out_prop = provider.formatMultipleItems(prop)

                        actorName = actor.name
                        if type(actor) is char_type.Character:
                            if actor.gender == "collective":
                                actorName = "the " + actorName

                        verb = provider.determineVerbForm(actor, "be", "present")

                        sentences.append(actorName + " " + verb + " " + out_prop)

                    elif ansType == "attribute":
                        actor, act, attr, propType, out_prop = ansList

                        act = act[0].replace("_", " ")
                        act = provider.determineVerbForm(actor, act, "past")

                        if out_prop:
                            sent_prop = provider.formatMultipleItems(out_prop)
                            sent_add = " that is "
                        else:
                            sent_prop = ""
                            sent_add = ""

                        actorName = actor.name
                        if type(actor) is char_type.Character:
                            if actor.gender == "collective":
                                actorName = "the " + actorName
                        elif type(actor) is item_type.Item:
                            if actorName.endswith("s"):
                                actorName = "the " + actorName

                        if propType == "amount":
                            sentences.append(actorName + " " + act + " " + sent_prop + " " + attr)
                        else:
                            sentences.append(actorName + " " + act + " " + attr + sent_add + sent_prop)

        skip = True

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


def generateFollowUpSentence(followUpType=None, givenEvent=None, answer=None):
    global answerList

    answerList = []
    output_choices = []

    causeList = []
    followUpResult = None

    print("givenEvent: ", givenEvent)
    if followUpType:
        followUpResult = ref.queryRelations(givenEvent, "cause")

        if not followUpResult:
            return None

        else:
            if type(followUpResult) is list:
                for entries in followUpResult:
                    container = provider.assembleSentence(entries, answer=answer)

                    if type(container) is list:
                        for values in container:
                            if values[1]:
                                causeList.append(values)
                    else:
                        if container[1]:
                            causeList.append(container)

            else:
                container = provider.assembleSentence(followUpResult, answer=answer)

                if type(container) is list:
                    for values in container:
                        if values[1]:
                            causeList.append(values)
                else:
                    if container[1]:
                        causeList.append(container)

            temp = (givenEvent, ("cause", causeList))
            output_choices.append(temp)

    else:
        action = None
        state = None
        desire = None
        per_prop = None

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

            try:
                per_prop = Entity.charList[actor.name.lower()].perProp
            except Exception as e:
                print("Error in perProp generateFollowUp: ", e)

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

            if desire:
                current = random.choice(desire)
                des, obj, event = current
                des = des[0].replace("_", " ")

                if type(obj) is str:
                    obj = obj.lower()

                else:
                    obj = obj.name.lower()

                followUpResult = ref.queryRelations(event, "cause")

                if followUpResult:
                    temp = (event, provider.whyQuestion(actor, des, obj))
                    output_choices.append(temp)

            if action:
                current = random.choice(action)
                act, obj, event = current
                act = act[0].replace("_", " ")

                if type(obj) is str:
                    obj = obj.lower()

                else:
                    obj = obj.name.lower()

                followUpResult = ref.queryRelations(event, "cause")

                if followUpResult:
                    temp = (event, provider.whyQuestion(actor, act, obj))
                    output_choices.append(temp)

            if state:
                current = random.choice(state)
                state, event = current
                state = state[0].replace("_", " ")

                followUpResult = ref.queryRelations(event, "cause")

                if followUpResult:
                    temp = (event, provider.whyQuestion(actor, state, None))
                    output_choices.append(temp)

            if per_prop:
                current = random.choice(per_prop)
                per_prop, event = current

                followUpResult = ref.queryRelations(event, "cause")

                if followUpResult:
                    temp = (event, provider.whyQuestion(actor, None, None, queriedProp=per_prop[0]))
                    output_choices.append(temp)

    print("output_choices: ", output_choices)

    output = None
    while not output:
        event, output = random.choice(output_choices)
        print("output: ", output)

    answerList.append(output)
    sentence = provider.assembleSentence(event, genType="sentence")
    populateDialogueTurns()
    print("finalHintList: ", finalHintList)
    print("answerList: ", answerList)

    return " How come " + sentence + "? What do you think is the reason?"


def generateFollowUp(answer, questType, exhausted=None, event=None, specialAnswer=None):
    global correctAnswer
    global gotHints
    global question
    global skip
    global regSentence
    global guessesNotExhausted

    praiseChoices = []
    followUpChoices = []

    followUpSent = generateFollowUpSentence()

    if answer is None and questType is None:
        gotCorrectAnswer("", followUpSent)

        guessesNotExhausted = True
        gotHints = True
        question = False
        skip = False

    elif exhausted == "yes" and not questType and answer:
        preparedString = "I think " + answer + "."
        gotCorrectAnswer(preparedString, followUpSent)

        gotHints = True
        question = False
        skip = True

    elif exhausted == "yes" and questType and answer:
        preparedString = answer + "."
        followUpSent = generateFollowUpSentence(followUpType=questType, givenEvent=event, answer=specialAnswer)
        gotCorrectAnswer(preparedString, followUpSent)

        skip = False

    elif questType == "rel" and answer and specialAnswer:
        preparedString = answer + "."
        followUpChoices.extend([" Do you think they're close to each other?",
                                " Describe " + specialAnswer.name + ".",
                                " Can you tell me something about " + specialAnswer.name + "?"
                                ])

        gotCorrectAnswer(preparedString, random.choice(followUpChoices))
        regSentence = True
        skip = False

    elif questType == "type" and answer and not specialAnswer:
        preparedString = answer + "."

        gotCorrectAnswer(preparedString, "")
        regSentence = True
        skip = False

    elif questType == "confirmation" and answer and not specialAnswer:
        preparedString = answer

        gotCorrectAnswer(preparedString, "")
        regSentence = True
        skip = False

    else:
        praiseChoices.extend(["Maybe you're right. I also think ",
                              "I agree with you! I also think "])

        if questType == "relationship_name" or questType == "location" or questType == "relationship_rel" \
                or questType == "action" or questType == "state" or questType == "desire" \
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
        question = False
        skip = False

    # print("gotHints: ", gotHints, "question: ", question, "skip: ", skip)


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


def getRandomEvent(genType, sequence=None, posList=None, ofList=None, toList=None, verbList=None, advList=None,
                   itemList=None, adjList=None, andList=None, objList=None):

    wnl = WordNetLemmatizer()

    dummyAnswer = []
    temp = None
    answer = False

    charList = [x.name for x in list(Entity.charList.values())]

    if genType == "where":
        dummyAnswer.extend(parser.parseWhereMessage(charList, verbList))

    elif genType == "who":
        dummyAnswer.extend(parser.parseWhoMessage(sequence, posList, ofList, toList, charList))

    elif genType == "why":
        dummyAnswer.extend(parser.parseWhyMessage(charList, objList, verbList, advList, itemList, adjList))

    elif genType == "what":
        dummyAnswer.extend(parser.parseWhatMessage(sequence, posList, ofList, charList, andList, itemList,
                                              special="true"))

    dummyAnswer = cleanList(dummyAnswer)

    if dummyAnswer:
        ansList = None

        while len(dummyAnswer) > 0:
            entries = random.choice(dummyAnswer)
            dummyAnswer.remove(entries)

            temp = entries
            ansType, ansList = entries

            if ansList:
                break

        answer = False

        if ansList:
            ansType, ansList = temp

            sentence = "I don't know the answer to that, but I do know that "

            if ansType == "location":
                actor, act, location = ansList

                if type(location) is str:
                    location = location
                else:
                    location = location.name

                act = wnl.lemmatize(act, 'v')

                event = actor.queryLocation(act, location, None)[2]
                followUpResult = ref.queryRelations(event, "cause")

                if followUpResult:
                    sent_act = provider.determineVerbForm(actor, act, "past")
                    sentence = sentence + actor.name + " " + sent_act + " at " + location
                    specAns = (actor, act, location, None, None)

                    generateFollowUp(sentence, ansType, exhausted="yes", event=event, specialAnswer=specAns)
                    answer = True

            elif ansType == "relationship_name":
                actor, rel, char = ansList
                answer = provider.formatMultipleItems(rel)
                verb = " is "

                if char:
                    if type(char) is list and len(char) > 1:
                        char = [x.name for x in char]
                        char_answer = ", ".join(char[:-1]) + " and " + char[len(char) - 1]
                        verb = " are "
                        answer = answer + "s"
                    elif type(char) is list and len(char) == 1:
                        char_answer = char[0].name
                    else:
                        char_answer = char.name

                    sentence = sentence + char_answer + verb + actor.name + "'s " + answer

                    generateFollowUp(sentence, "rel", specialAnswer=actor)
                    answer = True

            elif ansType == "relationship_rel":
                actor, rel, char = ansList
                answer = provider.formatMultipleItems(rel)
                verb = " is "

                if char:
                    if type(char) is list and len(char) > 1:
                        char = [x.name for x in char]
                        char_answer = ", ".join(char[:-1]) + " and " + char[len(char) - 1]
                        verb = " are "
                        answer = answer + "s"
                    elif type(char) is list and len(char) == 1:
                        char_answer = char[0].name
                    else:
                        char_answer = char.name

                    sentence = char_answer + verb + actor.name + "'s " + answer

                    generateFollowUp(sentence, "rel", specialAnswer=actor)
                    answer = True

            elif ansType == "item_appearance":
                actor, act, item, prop = ansList
                act = provider.determineVerbForm(actor, act[0], "present")

                event = item.queryProperty(prop[0], "appearance", None)[1][:-3]
                followUpResult = ref.queryRelations(event, "cause")

                if followUpResult:
                    sentence = "I don't know the answer to that, but I do know the appearance of the " + \
                           item.name + " " + actor.name + " " + act

                    specAns = (actor, act, item, "appearance", prop)

                    generateFollowUp(sentence, ansType, exhausted="yes", event=event, specialAnswer=specAns)
                    answer = True

            elif ansType == "item_amount":
                actor, act, item, prop = ansList
                act = provider.determineVerbForm(actor, act[0], "present")

                event = item.queryProperty(prop[0], "amount", None)[1][:-3]
                followUpResult = ref.queryRelations(event, "cause")

                if followUpResult:
                    sentence = "I don't know the answer to that, but I do know the number of the " + \
                               item.name + " " + actor.name + " " + act

                    specAns = (actor, act, item, "amount", prop)

                    generateFollowUp(sentence, ansType, exhausted="yes", event=event, specialAnswer=specAns)
                    answer = True

            elif ansType == "actor_personality":
                actor, prop = ansList
                act = provider.determineVerbForm(actor, "be", "present")

                event = actor.queryProperty(prop, "personality", None)

                sentence = "I don't know the answer to that, but I do know how " + actor.name + " " + act

                specAns = (actor, act, prop, None, None)

                generateFollowUp(sentence, ansType, exhausted="yes", event=event, specialAnswer=specAns)
                answer = True

            elif ansType == "actor_appearance":
                actor, prop = ansList
                act = provider.determineVerbForm(actor, "look", "present")

                event = actor.queryProperty(prop, "appearance", None)

                sentence = "I don't know the answer to that, but I do know how " + actor.name + " " + act + " like"

                specAns = (actor, act, prop, None, None)

                generateFollowUp(sentence, ansType, exhausted="yes", event=event, specialAnswer=specAns)
                answer = True

            elif ansType == "cause":
                for entries in ansList:
                    ansType, answers = entries

                    sentence = "I don't know the answer to that, but I do know that "

                    get_ans = answers[len(answers) - 1]
                    get_actor = ""
                    get_act = ""
                    get_obj = ""
                    get_propType = None
                    get_prop = None

                    event_act = None
                    event_des = None
                    event_state = None

                    if len(get_ans) == 5:
                        get_actor, get_act, get_obj, get_propType, get_prop = get_ans

                        try:
                            event_act = get_actor.queryAction(get_act, get_obj, None)[2]
                        except Exception as e:
                            print("Error in getRandomEvent: ", e)

                        try:
                            event_des = get_actor.queryDesire(get_act, get_obj, None)[2]
                        except Exception as e:
                            print("Error in getRandomEvent: ", e)

                    elif len(get_ans) == 2:
                        get_actor, get_act = get_ans

                        try:
                            event_state = get_actor.queryState(get_act, None)[1]
                        except Exception as e:
                            print("Error in getRandomEvent: ", e)

                    verb = " " + provider.determineVerbForm(get_actor, get_act, "past")
                    if len(wordnet.synsets(get_act)) > 0 and provider.getCommonPartOfSpeech(get_act) == 'a':
                        verb = " " + provider.determineVerbForm(get_actor, "be", "past") + verb

                    if get_obj != "":
                        if type(get_obj) is str:
                            get_obj = " " + get_obj
                        else:
                            get_obj = " " + get_obj.name

                    if get_prop:
                        get_prop = provider.formatMultipleItems(get_prop)

                        get_obj = get_prop + get_obj

                    sentence = sentence + get_actor.name + " " + verb + get_obj

                    event = None
                    if event_act:
                        event = event_act
                    elif event_des:
                        event = event_des
                    elif event_state:
                        event = event_state

                    followUpResult = ref.queryRelations(event, "cause")

                    if followUpResult:
                        generateFollowUp(sentence, ansType, exhausted="yes", event=event, specialAnswer=get_ans)

                        answer = True

    if answer is False and lock is False:
        if genType == "where":
            sentence_answer = "Where do you think so?"

            generateFollowUp(sentence_answer, "confirmation", specialAnswer=None)

        elif genType == "who":
            sentence_answer = "Who do you think is that person?"

            generateFollowUp(sentence_answer, "confirmation", specialAnswer=None)

        elif genType == "why":
            sentence_answer = "Why do you think so?"

            generateFollowUp(sentence_answer, "confirmation", specialAnswer=None)

        elif genType == "what":
            sentence_answer = "What do you think?"

            generateFollowUp(sentence_answer, "confirmation", specialAnswer=None)
