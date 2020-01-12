from yattag import Doc

class ContentKJTS():
    """
    This is the class for rednering kanji tests.
    """

    def reading(self,question,mode):
        doc, tag, text = Doc().tagtext()
        #create the tags
        with tag('div',('class','kanji_reading')):
            with tag('div'):
                # extract the kanji characters and out put them in the div
                text(question[0:question.find(self.te_reading)])
            # now eat the block nom nom nom
            with tag('div',('class','kanji_reading_brackets')):
                doc.stag('img', src='/static/top_bracket.png', width=self.render_mode[mode])
                with tag('div'):
                    text(' ')
                doc.stag('img', src='/static/btm_bracket.png', width=self.render_mode[mode])
        return doc.getvalue()

    def writing(self,question,mode):
        doc, tag, text = Doc().tagtext()
        with tag('div',('class','kanji_writing')):
            with tag('div'):
                doc.stag('img', src='/static/kanji-box.png', height=self.render_mode[mode])
        # now eat the block nom nom nom
            with tag('div',('class','furigana')):
                    # extract the kanji characters and out put them in the div
                    text(question[0:question.find(self.te_writing)])
        return doc.getvalue()

    def combo(self,question,mode):
        doc, tag, text = Doc().tagtext()
        token = question[0:question.find(self.te_combo)]
        with tag('div',('class','combo_question')):
            with tag('div'):
                doc.stag('img', src='/static/top_brace.png', height='20px')
                for c in token:
                    doc.stag('img', src='/static/empty.png', height=self.render_mode[mode])
                doc.stag('img', src='/static/btm_brace.png', height='20px')
            # now eat the block nom nom nom
            with tag('div',('class','furigana-combo')):
                # extract the kanji characters and out put them in the div
                for c in token:
                    with tag('div',('class','furigana-combo-row')):
                        text(c)
        return doc.getvalue()

    def __init__(self,question_bundle):
        self.question_list = question_bundle.splitlines()
        self.close_tokens = '）」｝'
        self.tokens = '（「｛'
        self.render_mode = {
            'pdf':'90px',
            'preview':'60px'
            }
        self.ts_reading ='（'
        self.te_reading ='）'
        self.ts_writing ='「'
        self.te_writing ='」'
        self.ts_combo ='｛'
        self.te_combo ='｝'




    def render_question(self, question, mode):
        '''
        The renders the question token in whatever mode is passed in
        '''
        tokens = {
           '（': self.reading(question[1:], mode),
           '「': self.writing(question[1:], mode),
           '｛': self.combo(question[1:], mode)
           }
        return tokens.get(question[0],'nothing')

    def render(self):
        pass

    def preview(self):
        doc, tag, text = Doc().tagtext()


        with tag('div',('class','preview')):
            for question in self.question_list:

                #initialize string indexer
                si = 0;
                #render a question in its own div
                with tag('div',('class','question')):
                    while question[si:] != '':

                        #if we are dealing with a token marker, start token processing
                        if question[si] in self.tokens:
                            doc.asis(self.render_question(question[si:],'preview'))

                            #eat the token untill we find its closure
                            while question[si] not in self.close_tokens:
                                si+=1

                            si+=1 # eat the closing marker of this token
                        else: #this is just "normal" output
                            with tag('div',('class','hiragana')):
                                with tag('div'):
                                    h = ""
                                    while (question[si-1:]!='') and (question[si:si+1] not in self.tokens) :
                                        h=h+question[si]
                                        si+=1
                                    text(h)
                                with tag('div', width='30px'):
                                    text(' ')
        return doc.getvalue()
