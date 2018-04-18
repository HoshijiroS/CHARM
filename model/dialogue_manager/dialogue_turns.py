import random

import nltk
from nltk.tag.stanford import CoreNLPParser
from nltk.tag import SennaTagger
from nltk.tree import ParentedTree

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


def formatMultipleItems(listAnswer):
    print("type: ", type(listAnswer), "length: ", len(listAnswer))
    if len(listAnswer) > 1 and type(listAnswer) is not str:
        out = ", ".join(listAnswer[:-1]) + " and " + listAnswer[len(listAnswer) - 1]
    elif type(listAnswer) is str:
        out = listAnswer
    else:
        out = listAnswer[0]

    return out


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
    global result
    global compMessage
    global wrongMessage
    global followUp

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
                    temp = hintList
                    hintList = []

                    i = 0
                    while i < 5:
                        r = random.choice(temp)
                        temp.remove(r)
                        hintList.append(r)
                        i = i + 1

                gotHints = True

    if (question is False or followUp is True) and incorrect is True:
        wrongMessage = resetWrongMessage()
        for answers in answerList:
            ansType, ansList = answers

            if ansType == "relationship_name":
                actor, rel, char = ansList
                if charList:
                    for character in charList:
                        if char[0].name.lower() == character:
                            generateFollowUp(character.title(), "relationship_name", ansList)

            elif ansType == "relationship_rel":
                actor, rel, char = ansList
                if type(rel) is not str:
                    pluralList = [x + "s" for x in rel]
                    answer = list(set(rel) & set(charList))
                    pluralAnswer = list(set(pluralList) & set(charList))

                    if answer:
                        answer = formatMultipleItems(answer)
                        generateFollowUp(answer, "relationship_rel", ansList)

                    elif pluralAnswer:
                        pluralAnswer = formatMultipleItems(pluralAnswer)
                        generateFollowUp(pluralAnswer, "relationship_rel", ansList)

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
                            generateFollowUp(loc, "location", ansList)

            elif ansType == "appProperty":
                actor, prop = ansList

                if adjList:
                    for adjective in adjList:
                        for entries in prop:
                            if entries == adjective:
                                generateFollowUp(entries, "appProperty", ansList)

                if advList:
                    for adverb in advList:
                        for entries in prop:
                            if entries == adverb:
                                generateFollowUp(entries, "appProperty", ansList)

            #elif ansType == "attribute":
            #    print("a")

    if gotHints is True and incorrect is True:
        result = []
        if hintList != [[]] and hintList != []:
            r = random.choice(hintList)
            hintList.remove(r)

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

                    out = formatMultipleItems(rel)

                    result.append("I think " + actor.name.title() + "'s " + out + " is " + char[0].name.title() + ".")
                    guessesExhausted()

                if ansType == "relationship_rel":
                    actor, rel, char = ansList

                    out = formatMultipleItems(rel)

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
            personality = ref.formatMultipleItems(personality)

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

                    preparedString = "Hooray! I think " + answer + " is the answer too!"
                    followUpSent = " Why do you think is " + actor.name.title() + " " + personality + "?"

                    correctAnswer = (actor, personality)
                    gotCorrectAnswer(preparedString, followUpSent)

    elif questType == "location" or questType == "relationship_rel":
        preparedString = "Hooray! I think " + answer + " is the answer too!"
        gotCorrectAnswer(preparedString, " Blah")

    elif questType == "appProperty":
        if correctAnswer:
            actor, personality = correctAnswer

            pronoun = provider.producePronoun(actor)

            preparedString = "Hooray! I also think " + actor.name.title() + " is " + personality + " because " + pronoun + " is " + answer + "."
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
