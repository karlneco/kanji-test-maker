from hktm.questions.QuestionBase import QuestionBase

class ComboQuestion(QuestionBase):
    """
    This is the class for combination type questions.
    """

    def __init__(self,question_type, question_text):
        super().__init__(question_type, question_text)

    def render(self):

        return f'This is a combo question {self.question_text}'
