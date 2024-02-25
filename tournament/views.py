from django.shortcuts import render, get_object_or_404

from .models import Question


def index(request):
    questions = Question.objects.all()
    data = {
        'title': "Турнир",
        'questions': questions,
    }
    return render(request,'tournament/index.html', context=data)

