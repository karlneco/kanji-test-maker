class QuestionBase():
    """
    This defines the data common for all questions
    """

    def __init__(self, question_type, question_text):
        self.question_type = question_type
        self.question_text = question_text
