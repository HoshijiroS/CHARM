from nltk.tag.stanford import CoreNLPPOSTagger
import nltk
import Dialogue_Manager.content_provider as cont_plan

def parse_message(message):
    r = CoreNLPPOSTagger('http://localhost:9000/')
    user_input = (r.tag(nltk.word_tokenize(message)))

    print(user_input)
    output_message = "I don't know."

    # answer questions
    WRB = [item for item in user_input if 'WRB' in item]
    WHO = [item for item in user_input if 'WP' in item]
    NNP = [item for item in user_input if 'NNP' in item]
    NN = [item for item in user_input if 'NN' in item]
    VB = [item for item in user_input if 'VB' in item]
    VBZ = [item for item in user_input if 'VBZ' in item]

    if WRB != []:
        if WRB[0][0] == 'Where' or WRB[0][0] == 'where':
            if NNP != []:
                NNP = NNP[0][0]
                print('NNP: ' + NNP)
            else:
                NNP = None

            if VB != []:
                VB = VB[0][0]
            else:
                VB = None

            # whereQuestion(actor, verb, location)
            output_message = cont_plan.whereQuestion(NNP, VB, None)

    if WHO != []:
        if NNP != []:
            NNP = NNP[0][0]
        else:
            NNP = None

        if NN != []:
            NN = NN[0][0]
            print("NN: " + NN)
        else:
            NN = None

        # whoQuestion(actor, person, relationship)
        output_message = cont_plan.whoQuestion(NNP, None, NN)

    return output_message