import nltk
from nltk.tag.stanford import CoreNLPParser
from nltk.tree import ParentedTree

import model.story_world.entities as Entity
import model.dialogue_manager.content_provider as cont_plan

def find_index_with_duplicates(seq, item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item, start_at+1)
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

def determineSentenceType(sequence):
    #print("sequence: ", sequence)
    beg = sequence[0][0]
    #print("beginning: ", beg)

    posList = [x for x, y in enumerate(sequence) if y[1] == "POS"]
    toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]
    ofList = [x for x, y in enumerate(sequence) if y[0] == "of"]
    andList = [x for x, y in enumerate(sequence) if y[0] == "and"]

    if toList != []:
        sequence = [i for i in sequence if i[0] != "the"]
        toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]

    nounTags = ["NN", "NNS", "NNP", "NNPS"]
    charList = [item[0] for item in sequence if item[1] in nounTags]
    print("charList: ", charList)

    verbTags = ["VBD", "VBZ", "VB", "VBP"]
    verbList = [item[0] for item in sequence if item[1] in verbTags]
    print("verbList: ", verbList)

    answer_list = []

    if beg == "who":
        if [item for item in sequence if "VBZ" in item] != [] or [item for item in sequence if "VBP" in item] != []:

            if posList != []:
                for index in posList:
                    answer_list.append(
                        cont_plan.confirmCharacter(sequence[index - 1][0], 0, relationship=sequence[index + 1][0]))

            elif ofList != []:
                for index in ofList:
                    answer_list.append(
                        cont_plan.confirmCharacter(sequence[index + 1][0], 0, relationship=sequence[index - 1][0]))

            elif toList != []:
                for index in toList:
                    answer_list.append(
                        cont_plan.confirmCharacter(sequence[index + 1][0], 0, person=sequence[index - 1][0]))

            else:
                for character in charList:
                    answer_list.append(cont_plan.confirmCharacter(character, 0))

    if beg == "where":
        if charList != []:
            if verbList != []:
                for character in charList:
                    for action in verbList:
                        answer_list.append(cont_plan.confirmCharacter(character, 1, action=action))

    if beg == "what":
        itemMatches = find_matches(Entity.itemList.keys(), sequence)
        itemMatches = list(set(itemMatches))
        print("itemMatches: ", itemMatches)
        #if nounMatches != []:
        #    print("name: ", [item for item in sequence if "name" in item])
        #    print("relationship: ", [item for item in sequence if "relationship" in item])
        if [item for item in sequence if "name" in item] != []:
            for index in posList:
                answer_list.append(
                    cont_plan.confirmCharacter(sequence[index - 1][0], 0, relationship=sequence[index + 1][0]))

            for index in ofList:
                answer_list.append(
                    cont_plan.confirmCharacter(sequence[index + 1][0], 0, relationship=sequence[index - 1][0]))

        elif [item for item in sequence if "relationship" in item] != []:
            for index in andList:
                answer_list.append(
                    cont_plan.confirmCharacter(sequence[index - 1][0], 0, person=sequence[index + 1][0]))

        elif [item for item in sequence if "appearance" in item] != []:
            if itemMatches != []:
                if posList != []:
                    for index in posList:
                        answer_list.append(
                            cont_plan.confirmCharacter(sequence[index - 1][0], 2, item=sequence[index + 1][0], propType="appearance"))

                else:
                    for index in ofList:
                        print("A: ", sequence[index + 1][0], " B:", sequence[index - 1][0])
                        answer_list.append(
                            cont_plan.confirmCharacter(sequence[index + 1][0], 2, item=sequence[index - 1][0], propType="appearance"))

            else:
                charList.remove("appearance")
                for character in charList:
                    answer_list.append(
                        cont_plan.confirmCharacter(character, 2, propType="appearance"))

        elif [item for item in sequence if "personality" in item] != []:
            charList.remove("personality")
            for character in charList:
                answer_list.append(
                    cont_plan.confirmCharacter(character, 2, propType="property"))

    if beg == "when":
        #if verbList != []:
        print("VerbList: ", verbList)
        for character in charList:
            for action in verbList:
                answer_list.append(cont_plan.confirmCharacter(character, 3, action=action))

    answer_list = [x for x in answer_list if x != "I don't know."]

    if len(answer_list) > 1:
        return "; ".join(answer_list[:-1]) + " and " + answer_list[len(answer_list) - 1] + "."

    elif len(answer_list) == 1:
        return answer_list[0] + "."

    else:
        return "I don't know."


def combine_similar(input, tags):
    output = []
    curr = []
    tag = ""
    for x in input:
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
    tags = ["NN", "NNP", "NNS", "NNPS"]
    processed_message = combine_similar(sequence.pos(), tags)

    return determineSentenceType(processed_message)


def split_compound(tree, count, messages):
    if type(tree) is nltk.tree.ParentedTree:
        if tree.label() == 'SBARQ' and count > 1:
            sentence = single_sentence(tree)
            messages.append(sentence)

    for subtree in tree:
        if type(subtree) is nltk.tree.ParentedTree:
            split_compound(subtree, count + 1, messages)
        else:
            break

    return messages


def parse_message(message):
    r = CoreNLPParser('http://localhost:9000/')
    user_input = ParentedTree.convert(list(r.raw_parse(message))[0])

    user_input.pretty_print()

    output_message = "I don't know"

    messages = []
    messages = split_compound(user_input, 0, messages)

    if messages == []:
        messages.append(single_sentence(user_input))

    if len(messages) > 1:
        output_message = " ".join(messages)
    else:
        output_message = messages[0]

    return output_message
