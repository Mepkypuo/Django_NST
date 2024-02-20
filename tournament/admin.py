from django.contrib import admin
from .models import Tournament, Question, Participant, Answer

admin.site.register(Tournament)
admin.site.register(Question)
admin.site.register(Participant)
admin.site.register(Answer)
