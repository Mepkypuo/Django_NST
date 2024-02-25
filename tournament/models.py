from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
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


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, verbose_name='Имя турнира')
    score = models.IntegerField(default=0, verbose_name="сумма баллов")

# @receiver(post_save, sender=Answer)
# def update_participant_score(sender, instance, created, **kwargs):
#     if created:
#         participant = instance.participant
#         if instance.is_correct:
#             participant.score += 1
#             participant.save()
#
#     participants = Participant.objects.filter(user=instance.participant.user)
#     total_score = sum([p.answers.filter(is_correct=True).count() for p in participants])
#     for participant in participants:
#         participant.score = total_score
#         participant.save()

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


class Answer(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, verbose_name='Имя участника')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100, verbose_name='ответ участника')
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.answer_text == self.question.correct_answer:
            self.is_correct = True
        else:
            self.is_correct = False
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
