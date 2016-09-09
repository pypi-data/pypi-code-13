from quiz import abstract_models
from quiz.utils import is_model_registered

__all__ = []


if not is_model_registered('quiz', 'Quiz'):
    class Quiz(abstract_models.AbstractQuiz):
        pass

    __all__.append('Quiz')


if not is_model_registered('quiz', 'Question'):
    class Question(abstract_models.AbstractQuestion):
        pass

    __all__.append('Question')


if not is_model_registered('quiz', 'AnswerChoice'):
    class AnswerChoice(abstract_models.AbstractAnswerChoice):
        pass

    __all__.append('AnswerChoice')


if not is_model_registered('quiz', 'QuizResult'):
    class QuizResult(abstract_models.AbstractQuizResult):
        pass

    __all__.append('QuizResult')


if not is_model_registered('quiz', 'QuizResultItem'):
    class QuizResultItem(abstract_models.AbstractQuizResultItem):
        pass

    __all__.append('QuizResultItem')
