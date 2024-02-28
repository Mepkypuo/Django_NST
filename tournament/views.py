from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.utils import timezone

from .forms import AnswerForm
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

    # Получение списка вопросов для турнира
    questions = Question.objects.filter(tournament=tournament)

    # Обработка формы
    selected_question = None
    if request.method == 'POST':
        question_id = request.POST.get('question_id')
        selected_question = get_object_or_404(Question, pk=question_id)

    data = {
        'title': "Турнир",
        'tournament': tournament,
        'participant': participant,
        'questions': questions,
        'selected_question': selected_question,
    }

    return render(request, 'tournament/index.html', context=data)


def submit_answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            # Сохраните ответ в базе данных
            answer = form.save(commit=False)
            answer.participant = request.user.participant  # Получение участника из текущего пользователя
            answer.save()
            return redirect('tournament')  # Перенаправьте куда-то после отправки ответа
    else:
        form = AnswerForm()
    return render(request, 'index.html', {'form': form})