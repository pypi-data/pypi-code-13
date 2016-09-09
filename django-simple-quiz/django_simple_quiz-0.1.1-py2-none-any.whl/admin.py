from django.apps import apps
from django.contrib import admin

AnswerChoice = apps.get_model('quiz', 'AnswerChoice')
Question = apps.get_model('quiz', 'Question')
Quiz = apps.get_model('quiz', 'Quiz')
QuizResult = apps.get_model('quiz', 'QuizResult')
QuizResultItem = apps.get_model('quiz', 'QuizResultItem')


class QuizAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Quiz, QuizAdmin)


class AnswerChoiceAdminInline(admin.TabularInline):
    model = AnswerChoice
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerChoiceAdminInline]
    list_display = ['question', 'question_type', 'position']
    list_editable = ['position']
    list_filter = ['quiz__name']
admin.site.register(Question, QuestionAdmin)


class QuizResultItemAdminInline(admin.TabularInline):
    model = QuizResultItem
    extra = 0


class QuizResultAdmin(admin.ModelAdmin):
    inlines = [QuizResultItemAdminInline]
    list_display = ['name', 'email', 'created']
    list_filter = ['quiz']
admin.site.register(QuizResult, QuizResultAdmin)
