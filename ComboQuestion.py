from Question import Question

class ComboQuestion(Question):
    """
    This is the class for combination type questions.
    """

    def __init__(self,question_type, question_text):
        super().__init__(question_type, question_text)

    def render(self):

        return self.question_text
