from django.db import models


class User(models.Model):
    local_id = models.IntegerField()


class History(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='phrases'
    )
    phrase = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
