from datetime import date

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from .utils import get_full_date, days_before

class Profile(models.Model):
    """User profile model class that extends built-in User model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

class Goal(models.Model):
    """Goal model class"""

    PRIORITY_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ]

    PROGRESS_VALIDATORS = [MinValueValidator(0.0), MaxValueValidator(100.0)]

    title = models.CharField(max_length=65)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateField()
    progress = models.FloatField(default=0.0, validators=PROGRESS_VALIDATORS)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
    completed = models.DateField(null=True, blank=True)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

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

    def undo_complete(self):
        self.completed = None

    def calculate_points(self):
        points = 0
        
        if self.completed:
            base = 10000
            days_before_deadline = days_before(self.completed, self.deadline)
            mult = 1000

            if days_before_deadline > 0:
                days_bonus = min(mult * days_before_deadline, 10000)
            else: 
                days_bonus = 0
            
            points = (base + days_bonus) * self.priority

        return points

    def __str__(self):
        return self.title