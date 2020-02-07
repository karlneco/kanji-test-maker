class RenderContentBase():
    '''
    This defines the data common for all content type renderers
    '''

    def __init__(self, question_bundle):
        self.question_list = question_bundle.splitlines()

        self.close_tokens = '）」｝＞』'
        self.tokens = '（「｛＜『'

        self.ts_reading ='（'
        self.te_reading ='）'
        self.ts_writing ='「'
        self.te_writing ='」'
        self.ts_furi = '『'
        self.te_furi = '』'
        self.ts_combo ='｛'
        self.te_combo ='｝'
        self.ts_bonus ='＜'
        self.te_bonus ='＞'
        self.split = '｜'
