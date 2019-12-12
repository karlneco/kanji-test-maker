from hktm.questions.QuestionBase import QuestionBase

class WritingQuestion(QuestionBase):
    """
    This is the class for writing type questions.
    """

    def __init__(self,question_type, question_text):
        super().__init__(question_type, question_text)

    def render(self):

        return f'This is a writing question {self.question_text}'
