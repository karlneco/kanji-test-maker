from Question import Question

class WritingQuestion(Question):
    """
    This is the class for writing type questions.
    """

    def __init__(self,question_type, question_text):
        super().__init__(question_type, question_text)

    def render(self):

        return self.question_text
