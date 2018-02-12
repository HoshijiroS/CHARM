import nltk
from nltk.tag.stanford import CoreNLPParser
from nltk.tree import ParentedTree

import model.dialogue_manager.content_provider as cont_plan


def determineSentenceType(sequence):
    beg = sequence[0][0].lower()

    posList = [x for x, y in enumerate(sequence) if y[1] == "POS"]
    toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]

    nounTags = ["NN", "NNS", "NNP", "NNPS"]
    charList = [item[0].lower() for item in sequence if item[1] in nounTags]

    verbTags = ["VBD", "VBZ", "VB", "VBP"]
    verbList = [item[0].lower() for item in sequence if item[1] in verbTags]

    answer_list = []

    if beg == "who":
        if [item for item in sequence if "VBZ" in item] != [] or [item for item in sequence if "VBP" in item] != []:

            if posList != []:
                for index in posList:
                    answer_list.append(
                        cont_plan.confirmCharacter(sequence[index - 1][0], None, sequence[index + 1][0], None, None, 0))

            elif toList != []:
                for index in toList:
                    answer_list.append(
                        cont_plan.confirmCharacter(sequence[index + 1][0], sequence[index - 1][0], None, None, None, 0))

            else:
                for character in charList:
                    answer_list.append(cont_plan.confirmCharacter(character, None, None, None, None, 0))

    if beg == "where":
        if charList != []:
            if verbList != []:
                for character in charList:
                    for action in verbList:
                        answer_list.append(cont_plan.confirmCharacter(character, None, None, action, None, 1))

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
                output.append((" ".join([x[0] for x in curr]), tag))
                curr[:] = []
                tag = ""
            output.append(x)
        elif x[1] == tag:
            curr.append(x)
        else:
            if len(curr) > 0:
                output.append((" ".join([x[0] for x in curr]), tag))
                curr[:] = []
            tag = x[1]
            curr.append(x)
    if len(curr) > 0:
        output.append((" ".join([x[0] for x in curr]), tag))
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
