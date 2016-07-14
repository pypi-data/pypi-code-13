from django.db import models


class Contributor(models.Model):

    given_name = models.CharField(max_length=255,
                                  blank=True,
                                  null=True)
    family_name = models.CharField(max_length=255,
                                   blank=True,
                                   null=True,
                                   db_index=True)

    class Meta:
        ordering = ("family_name", "given_name")

    def __str__(self):
        u = ""
        if self.given_name:
            u = self.given_name
            if self.family_name:
                u += " "
        if self.family_name:
            u += self.family_name
        return u


class Credit(models.Model):

    headline = models.CharField(max_length=255)
    contributors = models.ManyToManyField(Contributor,
                                          through="Contribution",
                                          blank=True)
    ordinal = models.PositiveIntegerField(blank=True,
                                          db_index=True)

    class Meta:
        ordering = ("ordinal",)

    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if not self.ordinal:
            last_credit = Credit.objects.last()
            self.ordinal = last_credit.ordinal + 10 if last_credit else 10
        return super().save(*args, *kwargs)


class Contribution(models.Model):
    contributor = models.ForeignKey(Contributor,
                                    on_delete=models.CASCADE)
    credit = models.ForeignKey(Credit,
                               on_delete=models.CASCADE)
