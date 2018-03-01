import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie

from model.dialogue_manager import dialogue_turns as parser

# Create your views here.

@ensure_csrf_cookie
def index(request):
    context = {}
    return render(request, 'view/index.html', context)

def process_message(request):
    message = json.loads(request.body.decode('utf-8'))['message']
    print(message)

    output_message = parser.parse_message(message)

    data = {'response': output_message}
    return JsonResponse(data)