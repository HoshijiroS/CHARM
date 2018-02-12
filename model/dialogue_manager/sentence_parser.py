import nltk
from nltk.tag.stanford import CoreNLPParser
from nltk.tree import ParentedTree

import model.dialogue_manager.content_provider as cont_plan


def determineSentenceType(sequence):
    beg = sequence[0][0].lower()

    posList = [x for x, y in enumerate(sequence) if y[1] == "POS"]
    toList = [x for x, y in enumerate(sequence) if y[1] == "TO"]

    if beg == "who":
        tags = ["NN", "NNS", "NNP", "NNPS"]
        charList = [item[0].lower() for item in sequence if item[1] in tags]
        if [item for item in sequence if "VBZ" in item] != [] or [item for item in sequence if "VBP" in item] != []:
            answer_list = []

            if posList != []:
                for index in posList:
                    answer_list.append(cont_plan.confirmCharacter(sequence[index - 1][0], None, sequence[index + 1][0]))

            elif toList != []:
                for index in toList:
                    answer_list.append(cont_plan.confirmCharacter(sequence[index + 1][0], sequence[index - 1][0], None))

                print("answer list: ", answer_list)

            else:
                for characters in charList:
                    answer_list.append(cont_plan.confirmCharacter(characters, None, None))

            if len(answer_list) > 1:
                return "; ".join(answer_list[:-1]) + ", and " + answer_list[len(answer_list) - 1]
            else:
                return answer_list[0] + "."


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

    # print("Message: ", OUTPUT_MESSAGE)
    # for x in user_input.pos():
    #    print("label: ", x[1], " entry: ", x[0])

    # r = CoreNLPPOSTagger('http://localhost:9000/')
    # user_input = r.tag(nltk.word_tokenize(message))
    # print(user_input)

    # print(traverse_tree(user_input, []))
    # user_input.pretty_print()

    # determineSentenceType(user_input)

    # answer questions
    # WRB = [item for item in user_input if 'WRB' in item]
    # WHO = [item for item in user_input if 'WP' in item]
    # NNP = [item for item in user_input if 'NNP' in item]
    # NN = [item for item in user_input if 'NN' in item]
    # VB = [item for item in user_input if 'VB' in item]
    # VBZ = [item for item in user_input if 'VBZ' in item]

    # if WRB != []:
    #     if WRB[0][0] == 'Where' or WRB[0][0] == 'where':
    #         if NNP != []:
    #             NNP = NNP[0][0]
    #             print('NNP: ' + NNP)
    #         else:
    #             NNP = None
    #
    #         if VB != []:
    #             VB = VB[0][0]
    #         else:
    #             VB = None
    #
    #         # whereQuestion(actor, verb, location)
    #         output_message = cont_plan.whereQuestion(NNP, VB, None)
    #
    # if WHO != []:
    #     if NNP != []:
    #         NNP = NNP[0][0]
    #     else:
    #         NNP = None
    #
    #     if NN != []:
    #         NN = NN[0][0]
    #         print("NN: " + NN)
    #     else:
    #         NN = None

    # whoQuestion(actor, person, relationship)
    # user_input = cont_plan.whoQuestion(NNP, None, NN)
