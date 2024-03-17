from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib import messages
from django.db.models import Prefetch

from .forms import AnswerForm
from .models import Tournament, Participant, Question, Answer

class TournamentView(TemplateView):
    template_name = 'tournament/index.html'

    def _get_base_context(self, tournament_id, selected_question=None):
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        participant = get_object_or_404(Participant, user=self.request.user, tournament=tournament)
        questions = Question.objects.filter(tournament=tournament).prefetch_related(
            Prefetch('answer_set', queryset=Answer.objects.filter(participant=participant), to_attr='participant_answers')
        )

        context = {
            'title': "Турнир",
            'tournament': tournament,
            'participant': participant,
            'questions': questions,
            'selected_question': selected_question,
            'answer_form': AnswerForm(),
        }

        return context

    def get(self, request, tournament_id):
        tournament = get_object_or_404(Tournament, pk=tournament_id)
        current_time = timezone.now()

        if not request.user.is_authenticated:
            return HttpResponseForbidden("Для доступа к турниру необходимо войти в систему.")

        if current_time < tournament.start_time or current_time > tournament.end_time:
            return HttpResponseForbidden("Доступ к турниру закрыт в данный момент.")

        selected_question_id = request.GET.get('selected_question')
        selected_question = None
        if selected_question_id:
            selected_question = get_object_or_404(Question, pk=selected_question_id, tournament=tournament)

        context = self._get_base_context(tournament_id, selected_question=selected_question)
        return self.render_to_response(context)

    def post(self, request, tournament_id):
        form_type = request.POST.get('form_type')

        if form_type == 'choose_question':
            question_id = request.POST.get('question_id')
            try:
                selected_question = Question.objects.get(pk=question_id, tournament_id=tournament_id)
            except Question.DoesNotExist:
                messages.error(request, "Вопрос не найден.")
                return redirect('tournament:tournament', tournament_id=tournament_id)

        elif form_type == 'submit_answer':
            form = AnswerForm(request.POST)
            if form.is_valid():
                try:
                    answer = form.save(commit=False)
                    answer.participant = Participant.objects.get(user=request.user, tournament_id=tournament_id)
                    answer.question = get_object_or_404(Question, pk=request.POST['question_id'],
                                                        tournament_id=tournament_id)
                    answer.save()
                    messages.success(request, "Ваш ответ сохранен.")
                    return HttpResponseRedirect(reverse('tournament:tournament', args=(
                    tournament_id,)) + f"?selected_question={answer.question.pk}")
                except (Participant.DoesNotExist, Question.DoesNotExist):
                    messages.error(request, "Произошла ошибка при сохранении ответа.")

            # Если форма не валидна, перенаправляем обратно на страницу турнира
            return redirect('tournament:tournament', tournament_id=tournament_id)

        else:
            messages.error(request, "Неверный запрос.")
            return redirect('tournament:tournament', tournament_id=tournament_id)

        # Если выбран вопрос, возвращаем пользователя на страницу турнира с выбранным вопросом
        if 'selected_question' in locals():
            return HttpResponseRedirect(
                reverse('tournament:tournament', args=(tournament_id,)) + f"?selected_question={selected_question.pk}")

        # Если не было действий связанных с выбором вопроса, просто вернуть пользователя на страницу турнира
        return redirect('tournament:tournament', tournament_id=tournament_id)
