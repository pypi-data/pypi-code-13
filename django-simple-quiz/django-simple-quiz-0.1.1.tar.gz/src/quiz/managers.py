from django.db import models


class QuizQuerySet(models.QuerySet):

    def get_current(self):
        return self.order_by('created').first()
