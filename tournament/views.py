from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.utils import timezone

from .models import Tournament, Participant, Question


def index(request,tournament_id):
    tournament = get_object_or_404(Tournament, pk=tournament_id)
    current_time = timezone.now()

    # Проверка доступа к турниру для зарегистрированных пользователей
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Для доступа к турниру необходимо войти в систему.")

    # Проверка доступа к турниру для участников с учетом времени начала и окончания
    if current_time < tournament.start_time or current_time > tournament.end_time:
        return HttpResponseForbidden("Доступ к турниру закрыт в данный момент.")

    # Проверка доступа к турниру для пользователей, участвующих в нем
    participant = Participant.objects.filter(user=request.user, tournament=tournament).first()
    if not participant:
        return HttpResponseForbidden("Вы не участвуете в данном турнире.")

    tournament_name = tournament.name
    questions = Question.objects.filter(tournament__name=tournament_name).order_by('id')
    selected_question = "Выберите любой вопрос"

    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        if question_id:
            selected_question = Question.objects.get(id=question_id)


    data = {
        'title': "Турнир",
        'tournament': tournament,
        'tournament_name': tournament_name,
        'selected_question': selected_question,
        'participant': participant
    }

    return render(request, 'tournament/index.html', context=data)



    # tournament_name = "тестовый турнир"
    # questions = Question.objects.filter(tournament__name=tournament_name).order_by('id')
    # selected_question = "Выберите любой вопрос"
    #
    # if request.method == 'POST':
    #     question_id = request.POST.get('question_id')
    #     if question_id:
    #         selected_question = Question.objects.get(id=question_id)
    #
    # data = {
    #     'title': "Турнир",
    #     'questions': questions,
    #     'selected_question': selected_question,
    #     'tournament': tournament_name
    # }