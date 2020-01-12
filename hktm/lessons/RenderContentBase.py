class RenderContentBase():
    """
    This defines the data common for all content type renderers
    """

    def __init__(self, question_bundle):
        self.question_bundle = question_bundle.splitlines()
