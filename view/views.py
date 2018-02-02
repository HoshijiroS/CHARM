from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
import conceptnet as concept_net
from nltk.corpus import wordnet
from nltk.tag.stanford import CoreNLPPOSTagger
import nltk
import Dialogue_Manager.content_provider as cont_plan

# Create your views here.

@ensure_csrf_cookie
def index(request):
    context = {}
    return render(request, 'view/index.html', context)

def process_message(request):
    message = json.loads(request.body.decode('utf-8'))['message']
    print(message)

    print(list(set([x.name().split(".")[0] for x in wordnet.synsets('absent')])))
    print(wordnet.synsets('joyous'))

    #print([x.name().split(".")[0] for x in wordnet.synset('be.v.01').lemmas()])

    #for lemma in wordnet.synsets('has'):
    #print(lemma.name())
    #print(lemma, lemma.frame_ids())

    #wn.synset('mass.n.03').name().split(".")[0]

    #[x.name().split(".")[0] for x in wordnet.synset('think.v.01')]
    #print

    #for ss in wordnet.synsets("stand"):
    #print(ss.name(), ss.lemma_names())
    #output_message = wordnet.synsets("sit")

    r = CoreNLPPOSTagger('http://localhost:9000/')
    user_input = (r.tag(nltk.word_tokenize(message)))

    print(user_input)
    output_message = "I don't know."

    #answer questions
    WHERE = [item for item in user_input if 'WRB' in item]
    WHO = [item for item in user_input if 'WP' in item]
    NNP = [item for item in user_input if 'NNP' in item]
    NN = [item for item in user_input if 'NN' in item]
    VB = [item for item in user_input if 'VB' in item]

    print("NN: ")
    print(NN)

    if WHERE != []:
        if NNP != []:
            NNP = NNP[0][0]
        else:
            NNP = None

        if VB != []:
            VB = VB[0][0]
        else:
            VB = None

        #whereQuestion(actor, verb, location)
        output_message = cont_plan.whereQuestion(NNP, VB, None)

    if WHO != []:
        if NNP != []:
            NNP = NNP[0][0]
        else: NNP = None

        if NN != []:
            NN = NN[0][0]
            print("NN: " + NN)
        else: NN = None

        #whoQuestion(actor, person, relationship)
        output_message = cont_plan.whoQuestion(NNP, None, NN)


    #output_message = output_message[:20]
    #output_message = cont_plan.whoQuestion("wanda", "father")
    #output_message = cont_plan.whatQuestion("wanda", "mother", "has")
    #output_message = cont_plan.whereQuestion("wanda", "live")
    #output_message = cont_plan.whatQuestion("wanda")
    data = {'response': output_message}
    return JsonResponse(data)