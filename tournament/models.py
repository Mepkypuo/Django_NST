from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Question(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    question_text = models.TextField()
    image_one = models.ImageField(upload_to='question_photos/')
    correct_answer = models.CharField(max_length=100)


class Participant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class Answer(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.answer_text == self.question.correct_answer:
            self.is_correct = True
        else:
            self.is_correct = False
        super().save(*args, **kwargs)

