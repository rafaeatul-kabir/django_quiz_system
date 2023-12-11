from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import models

class Topic(models.Model):
    name = models.CharField(max_length=100,)
    def __str__(self):
        return self.name
class Question(models.Model):
    question_body = models.TextField()
    answer = models.CharField(max_length=255)
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    
    def clean(self):
        super().clean()
        # Ensure that at least one of the options is the correct answer
        if self.answer not in [self.option1, self.option2, self.option3, self.option4]:
            raise ValidationError("The correct answer must be one of the provided options.")

    def __str__(self):
        return self.question_body

class UserQuestionAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    chosen_option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Compare the chosen option with the correct answer of the question
        self.is_correct = self.chosen_option == self.question.answer
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"Question: {self.question.question_body[:50]} - Chosen Option: {self.chosen_option} - Correct: {self.is_correct}"


class UserRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempts = models.ManyToManyField(UserQuestionAttempt)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)    
    def __str__(self):
        return f"{self.user.username} - Record on {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']

