import json
import pymongo
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'analytics/index.html')

def send_event(request):
    db = _get_db()
    event = json.loads(request.POST['data'])
    db.ev.insert(event)
    return HttpResponse('true')

def _get_db():
    connection = pymongo.Connection('localhost', 27017)
    db = connection['todo-analytics']
    return db
