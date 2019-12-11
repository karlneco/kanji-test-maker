from Question import Question

class ReadingQuestion(Question):
    """
    This is the class for reading type questions.
    """

    def __init__(self,question_type, question_text):
        super().__init__(question_type, question_text)

    def __str__(self):

        return self.question_text
