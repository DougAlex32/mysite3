from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId
from .models import Question

client = MongoClient(os.getenv('MONGO_URI'))
db = client['mysite3']
print(db.list_collection_names())
print(db.polls_question.find_one())

new_question_id = db.polls_question.insert_one({
    'question text' : 'What ORM do we use from MongoDB?',
    'pub_date': datetime.now()
})
print('new polls question', db.polls_question.find_one({'pub_date': datetime.now()}))

print( 'searched question', db.polls_question.find_one({ '_id': ObjectId('65bea3bf0844e3eadfbc684e')}))

def search_question_by_text(request, text):
    question = db.polls_question.find_one({'question text': text})
    if question:
        return HttpResponse(f"Found question: {question}")
    else:
        return HttpResponse(f"Question with text '{text}' not found.")

def search_all_questions_by_pub_date(request, pub_date):
    questions = db.polls_question.find({'pub_date': pub_date})
    result = [f"Question: {q}" for q in questions]
    return HttpResponse(result)

def update_question(request, question_id):
    result = db.polls_question.update_one(
        {'_id': ObjectId(question_id)},
        {'$set': {'pub_date': datetime.now()}}
    )
    if result.modified_count > 0:
        return HttpResponse(f"Question with ID {question_id} updated successfully.")
    else:
        return HttpResponse(f"Question with ID {question_id} not found.")

def delete_question(request, question_id):
    result = db.polls_question.delete_one({'_id': ObjectId(question_id)})
    if result.deleted_count > 0:
        return HttpResponse(f"Question with ID {question_id} deleted successfully.")
    else:
        return HttpResponse(f"Question with ID {question_id} not found.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# Create your views here.
