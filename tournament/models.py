from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

User = get_user_model()


class Tournament(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя турнира')
    start_time = models.DateTimeField(verbose_name='Время начала турнира')
    end_time = models.DateTimeField(verbose_name='Время окончания турнира')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Турнир"
        verbose_name_plural = "Турниры"


class Question(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Имя турнира')
    question_text = models.TextField(verbose_name='текст вопроса')
    image_one = models.ImageField(upload_to='question_photos/', null=True, blank=True)
    correct_answer = models.CharField(max_length=100, verbose_name='Правильный ответ')

    def __str__(self):
        return self.question_text

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"


class Answer(models.Model):
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, verbose_name='Имя участника')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100, verbose_name='ответ участника')
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.answer_text = self.answer_text.strip().lower()
        self.question.correct_answer = self.question.correct_answer.strip().lower()

        if self.answer_text == self.question.correct_answer:
            self.is_correct = True
        else:
            self.is_correct = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Имя турнира')
    score = models.IntegerField(default=0, verbose_name="сумма баллов")

    def get_user_scores(self):
        total_score = Answer.objects.filter(participant__user=self.user, is_correct=True).count()
        self.score = total_score
        self.save()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


@receiver(post_save, sender=Answer)
def update_participant_score(sender, instance, created, **kwargs):
    if created:  # Проверяем, был ли создан объект
        participant = instance.participant
        if instance.is_correct:  # Проверяем, является ли ответ правильным
            participant.score += 1  # Увеличиваем счетчик баллов
        participant.save()  # Сохраняем изменения
    else:  # Объект переписывается
        if instance.is_correct != instance.previous_is_correct:  # Проверяем, изменилось ли значение is_correct
            participant = instance.participant
            if instance.is_correct:  # Проверяем, является ли новый ответ правильным
                participant.score += 1  # Увеличиваем счетчик баллов
            else:
                participant.score -= 1  # Уменьшаем счетчик
            participant.save()  # Сохраняем изменения


@receiver(pre_save, sender=Answer)
def store_previous_is_correct(sender, instance, **kwargs):
    if instance.pk:
        prev_instance = sender.objects.get(pk=instance.pk)
        instance.previous_is_correct = prev_instance.is_correct
    else:
        instance.previous_is_correct = instance.is_correct


