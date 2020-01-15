class RenderContentBase():
    '''
    This defines the data common for all content type renderers
    '''

    def __init__(self, question_bundle):
        self.question_list = question_bundle.splitlines()
        self.ts_reading ='（'
        self.te_reading ='）'
        self.ts_writing ='「'
        self.te_writing ='」'
        self.ts_combo ='｛'
        self.te_combo ='｝'
