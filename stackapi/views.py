from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from stackapi.models import Question
from stackapi.serializer import QuestionSerializer
from bs4 import BeautifulSoup

import requests
import json

# Create your views here.

def index(request):
    return HttpResponse("All Good")

class questionapi(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

def latest(request):
    try:
        res = requests.get("https://stackoverflow.com/questions")
        soup = BeautifulSoup(res.text, "html.parser")
        questions = soup.select(".s-post-summary")

        for q in questions:
            x = q.select_one('.s-link').getText()
            vote_count = q.select_one('.s-post-summary--stats-item-number').getText()
            views = q.select_one('.s-post-summary--stats-item:last-child').attrs['title']

            question = Question()
            question.question = x
            question.vote_count = vote_count
            question.views = views

            question.save()
        return HttpResponse("Latest Entry Inserted from StackOverFlow. ")
    except Exception as m:
        return HttpResponse(f" Failed{m}")