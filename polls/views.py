from django.shortcuts import render, get_object_or_404

# from django.template import loader

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.db.models import F

from django.views import generic
from django.utils import timezone


"""
# Create your views here.
def index(request):
  latest_question_list = Question.objects.order_by("-pub_date")[:5]
  #template = loader.get_template("polls/index.html")
  context = {
    "latest_question_list":latest_question_list
  }
  #output = "\n".join([q.question_text for q in latest_question_list ])
  #return HttpResponse(template.render(context,request))
  return render(request,"polls/index.html",context)
  


def detail(request,question_id):
  '''try:
    question = Question.objects.get(pk=question_id)
  except Question.DoesNotExist:
    raise Http404("Question Doesn't exist")'''
  #return HttpResponse("You're looking at question %s." % question_id)
  question = get_object_or_404(Question,pk=question_id)
  return render(request,"polls/detail.html",{"question":question})
  

def results(request,question_id):
  question = get_object_or_404(Question,pk=question_id)
  '''
  response = "You're looking at the results of question %s."
  return HttpResponse(response % question_id) '''
  return render(request,"polls/results.html",{"question":question})
"""


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """ Return the last five published questions (not including those set to be
        published in the future)."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """Excludes any questions that aren't published yet.."""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(requset, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=requset.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        """modifiying data base value like this could cause rase condition so
        selected_choice.votes += 1
        selected_choice.save()"""
        choice = Choice.objects.filter(pk=requset.POST["choice"])
        choice.update(votes=F("votes") + 1)
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    ##return HttpResponse("You're voting on question %s." % question_id)

    # changing the above view to generic view
