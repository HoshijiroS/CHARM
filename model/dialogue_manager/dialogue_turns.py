import random

import nltk
from nltk.tag.stanford import CoreNLPParser
from nltk.tree import ParentedTree

import model.dialogue_manager.sentence_parser as parser
import model.story_world.entities as Entity
import model.externals.wordnet as WordNet

incorrect = False
question = True
gotHints = True
first = True
answerList = []
hintList = []
result = []
compMessage = [""]
wrongMessage = [""]


def guessesExhausted():
    global incorrect
    global question
    global gotHints
    global compMessage
    global first

    first = True
    question = True
    gotHints = False
    incorrect = False
    compMessage = [""]


def gotCorrectAnswer(answer):
    global incorrect
    global question
    global gotHints
    global result
    global wrongMessage
    global compMessage
    global first

    first = True
    incorrect = False
    question = True
    gotHints = True
    wrongMessage = [""]
    compMessage = [""]

    result = []
    result.append("Hooray! I think " + answer + " is the answer too!")


def formatMultipleItems(listAnswer):
    if len(listAnswer) > 1 and type(listAnswer) is not str:
        out = ", ".join(listAnswer[:-1]) + " and " + listAnswer[len(listAnswer) - 1]
    elif type(listAnswer) is str:
        out = listAnswer
    else:
        out = listAnswer[0]

    return out


def resetWrongMessage():
    message = ["I don't think that's the answer, but ",
               "Let's try getting the right answer together. ",
               "Let's try again! "]

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
    tags = ["NNP", "NNS", "NNPS"]
    processed_message = combine_similar(sequence.pos(), tags)

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

    beg = sequence[0][0]
    posList = [x for x, y in enumerate(sequence) if y[1] == "POS"]
    toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]
    ofList = [x for x, y in enumerate(sequence) if y[0] == "of"]
    andList = [x for x, y in enumerate(sequence) if y[0] == "and"]
    itemList = list(set(find_matches(Entity.itemList.keys(), sequence)))

    if toList:
        sequence = [i for i in sequence if i[0] != "the"]
        toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]

    nounTags = ["NNS", "NNP", "NNPS"]
    charList = [item[0] for item in sequence if item[1] in nounTags]

    verbTags = ["VBD", "VBZ", "VB", "VBP"]
    verbList = [item[0] for item in sequence if item[1] in verbTags]

    if question is True:
        answerList = []
        wrongMessage = [""]
        incorrect = True

        if beg == "who":
            answerList.extend(parser.parseWhoMessage(sequence, posList, ofList, toList, charList))

        if beg == "where":
            answerList.extend(parser.parseWhereMessage(charList, verbList))

        if beg == "what":
            answerList.extend(parser.parseWhatMessage(sequence, posList, ofList, charList, andList, itemList))

        if beg == "why":
            answerList.extend(parser.parseWhyMessage(charList, verbList))

        answerList = [x for x in answerList if x[0] != "unknown"]
        tempResult = []

        if not answerList:
            tempResult.extend(["I don't really know the answer to that. You can rephrase your question if you want?",
                               "I'm sorry but, I don't really know the answer to your question",
                               "I don't really know the answer to that. But you can ask me other questions."])

            result.append(random.choice(tempResult))
            guessesExhausted()

        if len(answerList) != 0:
            question = False
            gotHints = False

        if gotHints is False:
            hintList = []
            hintChoices = []
            wrongMessage = [""]

            answerList = cleanList(answerList)

            for answers in answerList:
                ansType, ansList = answers
                print("answers: ", answers)

                if ansType == "relationship_name":
                    actor, rel, char = ansList

                    if len(char) > 1:
                        result = []
                        nameList = [x.name.title() for x in char]
                        out_char = ", ".join(nameList[:-1]) + " and " + nameList[len(nameList) - 1]

                        result.append(actor.name.title() + " has many " + rel + "s. They are " + out_char + ".")
                        guessesExhausted()

                    else:
                        wordCount = len(char[0].name.split())
                        if wordCount == 1:
                            words = "word"
                        else:
                            words = "words"

                        hintChoices = [
                            "I think the first name of " + actor.name.title() + "'s " + rel + " starts with " + char[
                                                                                                                    0].name[
                                                                                                                :1] + ".",
                            "I think the name of " + actor.name.title() + "'s " + rel + " is composed of " + str(
                                wordCount) + " " + words + ".",
                            "I think the first name of " + actor.name.title() + "'s " + rel + " has the letter " +
                            char[0].name[2] + "."]

                        hintList.append(hintChoices)
                        gotHints = True

                elif ansType == "relationship_rel":
                    actor, rel, char = ansList

                    if [x for x in rel if x == "classmate"] or rel == "classmate":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " and " + char.name.title() + " go to the same school. What kind of relationship do you think they have?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " are being taught by the same teacher. So, what do you think is their relationship with each other?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " attend the same classes. What is their relationship to each other then?"
                        ])

                    if [x for x in rel if x == "friend"] or rel == "friend":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " and " + char.name.title() + " talk to each other sometimes. Maybe they are a little more than acquaintances? What can their relationship be?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " can even become best friends if they spend more time together. So, what do you think is their relationship?",
                            "I think " + actor.name.title() + " likes to talk to " + char.name.title() + ". What are they to each other?"
                        ])

                    if [x for x in rel if x == "best friend"] or rel == "best friend":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " and " + char.name.title() + " are always together. Maybe they are a little more than friends? What are they to each other?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " go to school together. So, what do you think is their relationship?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " even share items. What can their relationship be?"
                        ])

                    if [x for x in rel if x == "father"] or rel == "father":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " are relatives. So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
                            "I think " + char.name.title() + " provides for " + actor.name.title() + "'s needs. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
                        ])

                    if [x for x in rel if x == "daughter"] or rel == "daughter":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " are relatives. So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
                            "I think " + actor.name.title() + " loves " + char.name.title() + " very much. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
                        ])

                    if [x for x in rel if x == "brother"] or rel == "brother":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " have the same surname! So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
                            "I think " + char.name.title() + " and " + actor.name.title() + " are relatives. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
                        ])

                    if [x for x in rel if x == "sister"] or rel == "sister":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " and " + char.name.title() + " live in the same house. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
                            "I think " + actor.name.title() + " and " + char.name.title() + " have the same surname! So, what do you think is the relationship of " + char.name.title() + " to " + actor.name.title() + "?",
                            "I think " + char.name.title() + " and " + actor.name.title() + " are relatives. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
                        ])

                    if [x for x in rel if x == "teacher"] or rel == "teacher":
                        hintChoices.extend([
                            "I think " + actor.name.title() + " respects " + char.name.title() + " very much. Maybe they also see each other at school. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
                            "I think " + actor.name.title() + " learns a lot from listening to " + char.name.title() + ". So, who do you think is " + char.name.title() + " to " + actor.name.title() + "?",
                            "I think you can consider " + char.name.title() + " as " + actor.name.title() + "'s second mother. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
                        ])

                    if [x for x in rel if x == "student"] or rel == "student":
                        hintChoices.extend([
                            "I think " + char.name.title() + " respects " + actor.name.title() + " very much. Maybe they also see each other at school. Who can " + char.name.title() + " be to " + actor.name.title() + "?",
                            "I think " + char.name.title() + " learns a lot from listening to " + actor.name.title() + ". So, who do you think is " + char.name.title() + " to " + actor.name.title() + "?",
                            "I think you can consider " + actor.name.title() + " as " + char.name.title() + "'s second mother. Who can " + char.name.title() + " be to " + actor.name.title() + "?"
                        ])

                    if [x for x in rel if x == "neighbor"] or rel == "neighbor":
                        hintChoices.extend([
                            "I think " + char.name.title() + " and " + actor.name.title() + " live in the same neighborhood. What do you think is their relationship with each other?",
                            "I think " + actor.name.title() + " lives near " + char.name.title() + ". So, who do you think is " + actor.name.title() + " to " + char.name.title() + "?",
                            "I think there is a possibility that " + actor.name.title() + "'s and " + char.name.title() + "'s houses are only beside each other! So, what do you think is their relationship?"
                        ])

                    if len(hintChoices) > 3:
                        i = 0
                        temp = []
                        while i < 3:
                            r = random.choice(hintChoices)
                            hintChoices.remove(r)
                            temp.append(r)
                            i = i + 1

                        hintList.append(temp)
                        gotHints = True

                    else:
                        hintList.append(hintChoices)
                        gotHints = True

                elif ansType == "location":
                    actor, action, loc = ansList

                    temp = Entity.locList[loc.lower()].appProp
                    print("Temp: ", temp)

                    if temp:
                        for properties in temp:
                            hintChoices.append(
                                "I think the place where " + actor.name.title() + action + " is " + properties)

                    else:
                        wordCount = len(loc.split())
                        if wordCount == 1:
                            words = "word"
                        else:
                            words = "words"

                        hintChoices.extend(["I think the name of the place where " + actor.name.title() + " " + action + " starts with " + loc[                                                                                            :1] + ".",
                                            "I think the name of the place where " + actor.name.title() + " " + action + " is composed of " + str(
                                            wordCount) + " " + words + ".",
                                            "I think the name of the place where " + actor.name.title() + " " + action + " has the letter " +
                                            loc[2] + "."])

                    if len(hintChoices) > 3:
                        i = 0
                        temp = []
                        while i < 3:
                            r = random.choice(hintChoices)
                            hintChoices.remove(r)
                            temp.append(r)
                            i = i + 1

                        hintList.append(temp)
                        gotHints = True

                    else:
                        hintList.append(hintChoices)
                        gotHints = True

                elif ansType == "item_appearance":
                    actor, item, prop = ansList

                    #for prop
                    #synonymList = WordNet.getAdjList(prop)

                elif ansType == "confirmation":
                    hintList.append(["Do you mean " + ansList.name.title() + "?"])
                    gotHints = True

    elif question is False and incorrect is True:
        wrongMessage = resetWrongMessage()
        for answers in answerList:
            ansType, ansList = answers

            if ansType == "relationship_name":
                actor, rel, char = ansList
                if charList:
                    for character in charList:
                        if char[0].name.lower() == character:
                            gotCorrectAnswer(character.title())

            elif ansType == "relationship_rel":
                actor, rel, char = ansList
                if type(rel) is not str:
                    pluralList = [x + "s" for x in rel]
                    answer = list(set(rel) & set(charList))
                    pluralAnswer = list(set(pluralList) & set(charList))

                    if answer:
                        answer = formatMultipleItems(answer)
                        gotCorrectAnswer(answer)

                    elif pluralAnswer:
                        pluralAnswer = formatMultipleItems(pluralAnswer)
                        gotCorrectAnswer(pluralAnswer)

                elif type(rel) is str:
                    if charList:
                        for character in charList:
                            if rel == character or rel + "s" == character:
                                gotCorrectAnswer(character)

            elif ansType == "location":
                actor, action, loc = ansList
                if charList:
                    for character in charList:
                        if character in loc.lower():
                            gotCorrectAnswer(loc)

    if gotHints is True and incorrect is True:
        result = []
        if hintList != [[]]:
            for hints in hintList:
                r = random.choice(hints)
                hints.remove(r)

                if first is True:
                    # print("compMessage2: ", compMessage)
                    result.append(random.choice(compMessage) + r)
                    first = False
                else:
                    result.append(random.choice(wrongMessage) + r)

        elif hintList == [[]]:
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

    elif gotHints is False and incorrect is True:
        result = []

    if result:
        print("result: ", result)
        if len(result) > 1:
            return "; ".join(result[:-1]) + " and " + result[len(result) - 1]

        elif len(result) == 1:
            return result[0]
    else:
        return "Try asking me a question!"


def parse_message(message):
    r = CoreNLPParser('http://localhost:9000/')
    user_input = ParentedTree.convert(list(r.raw_parse(message))[0])

    user_input.pretty_print()

    messages = []
    messages = [split_compound(user_input, 0, messages)][0]

    if not messages:
        messages.append(single_sentence(user_input))

    if len(messages) > 1:
        output_message = " ".join(messages)
    else:
        output_message = messages[0]

    return output_message