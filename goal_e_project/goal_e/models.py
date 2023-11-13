from django.db import models

class Goal(models.Model):
    """Goal model class"""

    PRIORITY_CHOICES = [
        (1, 'low'),
        (2, 'medium'),
        (3, 'high')
    ]

    title = models.CharField(max_length=65)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField()
    progress = models.FloatField(default=0.0)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    completed = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title