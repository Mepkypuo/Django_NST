from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView

from .forms import AnswerForm
from .models import Tournament, Participant, Question, Answer


class TournamentView(TemplateView):
    template_name = 'tournament/index.html'

    def get(self, request, tournament_id):
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

        context = {
            'title': "Турнир",
            'tournament': tournament,
            'participant': participant,
            'questions': questions,
            'selected_question': None,
            'answer_form': AnswerForm()
        }

        return self.render_to_response(context)

    def post(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)

        form_type = request.POST.get('form_type', None)

        # POST запрос для выбора вопроса
        if form_type == 'choose_question':
            question_id = request.POST.get('question_id')
            selected_question = get_object_or_404(Question, pk=question_id)

            context = {
                'title': "Турнир",
                'tournament': tournament,
                'participant': Participant.objects.get(user=request.user, tournament=tournament),
                'questions': Question.objects.filter(tournament=tournament),
                'selected_question': selected_question,
                'answer_form': AnswerForm(),  # Добавляем форму ответа в контекст
            }
            return self.render_to_response(context)

        # POST запрос для отправки ответа
        elif form_type == 'submit_answer':
            form = AnswerForm(request.POST)

            if form.is_valid():
                answer = form.save(commit=False)
                answer.participant = Participant.objects.get(user=request.user, tournament=tournament)
                answer.question = Question.objects.get(pk=request.POST['question_id'])
                answer.save()

                # Получаем выбранный вопрос из запроса POST
                selected_question_id = request.POST.get('question_id')
                selected_question = get_object_or_404(Question, pk=selected_question_id)

                # Получаем турнир из контекста или из базы данных
                tournament = get_object_or_404(Tournament, pk=tournament_id)

                # Получаем участника из контекста или из базы данных
                participant = Participant.objects.get(user=request.user, tournament=tournament)

                context = {
                    'title': "Турнир",
                    'tournament': tournament,
                    'participant': participant,
                    'questions': Question.objects.filter(tournament=tournament),
                    'selected_question': selected_question,
                    'answer_form': AnswerForm(),
                }

                return self.render_to_response(context)

        # Если не удалось обработать POST запрос, возвращаем 404
        return HttpResponseForbidden("Invalid POST request.")

