# # Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from datetime import datetime
from .models import Question, Choice, Message


def detail(request, question_id):
    pk = Question.objects.get(id = question_id)
    context = {'question': pk}
    return render(request, 'main/detail.html', context)


def results(request, question_id):

    field = request.GET.get('field', '' )

    response = "You're looking at the results of question %s. %s"
    return HttpResponse(response % (question_id, field))



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'main/detail.html', {'question': question,'error_message': "You didn't select a choice.",})
    else:
        selected_choice.votes += 1
        selected_choice.save()

        return HttpResponseRedirect(reverse('results', args=(question.id,)))


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'main/index.html',context)


def long_text_form(request):
    if request.method == 'POST':
        question_text = request.POST['question_text']
        long_text = request.POST['long_text']
        q = Question()
        q.long_text = long_text
        q.question_text = question_text
        q.pub_date = datetime.now()
        q.save()
        return HttpResponseRedirect(reverse('detail', args=(q.id,)))
    return render(request, 'main/form.html', {})

def blog(request):
    message_list = Message.new_message
    return render(request, 'main/blog_1.html', {})