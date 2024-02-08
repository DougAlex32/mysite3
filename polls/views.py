from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from .models import Question,Choice
from django.template import loader
from django.urls import reverse
from datetime import datetime
from django.views import generic
from django.utils import timezone
# from pymongo import MongoClient
import os
# from dotenv import load_dotenv
# load_dotenv()
from bson import ObjectId


# client = MongoClient(os.getenv('MONGO_URI'))
# db = client['mysite3']
# print(db.list_collection_names())
# print(db.polls_question.find_one())

# new_question_id = db.polls_question.insert_one({
#     'question text' : 'What ORM do we use from MongoDB?',
#     'pub_date': datetime.now()
# })
# print('new polls question', db.polls_question.find_one({'pub_date': datetime.now()}))

# print( 'searched question', db.polls_question.find_one({ '_id': ObjectId('65bea3bf0844e3eadfbc684e')}))

# def search_question_by_text(request, text):
#     question = db.polls_question.find_one({'question text': text})
#     if question:
#         return HttpResponse(f"Found question: {question}")
#     else:
#         return HttpResponse(f"Question with text '{text}' not found.")

# def search_all_questions_by_pub_date(request, pub_date):
#     questions = db.polls_question.find({'pub_date': pub_date})
#     result = [f"Question: {q}" for q in questions]
#     return HttpResponse(result)

# def update_question(request, question_id):
#     result = db.polls_question.update_one(
#         {'_id': ObjectId(question_id)},
#         {'$set': {'pub_date': datetime.now()}}
#     )
#     if result.modified_count > 0:
#         return HttpResponse(f"Question with ID {question_id} updated successfully.")
#     else:
#         return HttpResponse(f"Question with ID {question_id} not found.")

# def delete_question(request, question_id):
#     result = db.polls_question.delete_one({'_id': ObjectId(question_id)})
#     if result.deleted_count > 0:
#         return HttpResponse(f"Question with ID {question_id} deleted successfully.")
#     else:
#         return HttpResponse(f"Question with ID {question_id} not found.")

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

#  def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[
        :5
    ]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))




# Create your views here.
