from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display=['name']
@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=['topic', 'question_body', 'option1','option2','option3','option4']
@admin.register(models.UserRecord)
class UserRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_attempts', 'score', 'timestamp']

    def display_attempts(self, obj):
        return ', '.join([str(attempt) for attempt in obj.attempts.all()])

    display_attempts.short_description = 'Attempts'
