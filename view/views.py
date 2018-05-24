import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

import model.externals.logger as logger
from model.dialogue_manager import dialogue_turns as parser
from model.story_world import story_content


# Create your views here.

@ensure_csrf_cookie
def index(request):
    context = {}
    story_content.currIndex = 0
    return render(request, 'view/index.html', context)


def process_message(request):
    message = json.loads(request.body.decode('utf-8'))['message']
    print(message)

    logger.log("User", message)
    output_message = parser.parse_message(message)
    logger.log("CHARM", output_message)

    data = {'response': output_message}
    return JsonResponse(data)


def prev_page(request):
    chapName, chapFull, pageMax, pageNum, pageContents = story_content.getPrevPage()
    data = {'content': pageContents, 'pageNum': pageNum, 'pageMax': pageMax, 'chapName': chapName, 'chapFull': chapFull}
    return JsonResponse(data)


def next_page(request):
    chapName, chapFull, pageMax, pageNum, pageContents = story_content.getNextPage()
    data = {'content': pageContents, 'pageNum': pageNum, 'pageMax': pageMax, 'chapName': chapName, 'chapFull': chapFull}
    return JsonResponse(data)


def generate_log(request):
    logger.save_log()
    data = {'message': 'Log generated.'}
    return JsonResponse(data)
