from datetime import date
from django.db import models

from .utils import get_full_date

class Goal(models.Model):
    """Goal model class"""

    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]

    title = models.CharField(max_length=65)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField()
    progress = models.FloatField(default=0.0)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    completed = models.DateField(null=True, blank=True)

    def get_progress_str(self):
        if self.progress % 1 == 0:
            return f'{int(self.progress)}%'
        
        return f'{self.progress:.2f}%'
    
    def get_deadline_str(self):
        return get_full_date(self.deadline)
    
    def get_completed_str(self):
        if self.completed:
            return get_full_date(self.completed)
    
    def complete_goal(self):
        self.completed = date.today()
        self.progress = 100.0

    def __str__(self):
        return self.title