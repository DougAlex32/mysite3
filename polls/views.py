from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId

client = MongoClient(os.getenv('MONGO_URI'))
db = client['mysite3']
print(db.list_collection_names())
print(db.polls_question.find_one())

new_question_id = db.polls_question.insert_one({
    'question text' : 'What ORM do we use from MongoDB?',
    'pub_date': datetime.now()
})
print('new polls question', db.polls_question.find_one({'pub_date': datetime.now()}))
def index(request):
    return HttpResponse("Hello, world. You're at the poll index")
# Create your views here.
