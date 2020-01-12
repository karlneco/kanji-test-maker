class RenderContentBase():
    '''
    This defines the data common for all content type renderers
    '''

    def __init__(self, question_bundle):
        self.question_list = question_bundle.splitlines()
