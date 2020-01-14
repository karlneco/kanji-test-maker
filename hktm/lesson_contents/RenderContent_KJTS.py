from hktm.lesson_contents.RenderContentBase import RenderContentBase
from yattag import Doc

class RenderContentKJTS(RenderContentBase):
    """
    This is the class for rendering kanji tests.
    """

############################################################### reading question
    def reading(self,question,mode):
        '''
        This renders a reading question

        Returns
        -------
        tuple (str,int)
            the string is the doc tree to send to the output, the int is the
            required number of pixels to rais the subsequent hiragana block
            - this should be a negative number and will be used as a partameter
            to css margin-left attribute
        '''

        doc, tag, text = Doc().tagtext()
        rise_next = 0
        #create the tags
        with tag('div',('class','kanji_reading')):
            with tag('div'):
                # extract the kanji characters and out put them in the div
                text(question[0:question.find(self.te_reading)])
            # check if the question needs more space for the hiragaana te_writing
            # this is requested by adding 'japanse spaces' to the kanji characeter
            if ('　' in question[0:question.find(self.te_reading)]):
                rise_next = -60 #if so then tell the main rendere to raise the next hiragana block

            # now eat the block nom nom nom
            with tag('div',('class','kanji_reading_brackets')):
                doc.stag('img', src='/static/top_bracket.png', width=self.render_mode[mode])
                with tag('div'):
                    text(' ')
                doc.stag('img', src='/static/btm_bracket.png', width=self.render_mode[mode])
        return (doc.getvalue(), rise_next)

############################################################### writing question
    def writing(self,question,mode):
        '''
        This renders a writing question

        Returns
        -------
        tuple (str,int)
            the string is the doc tree to send to the output, the int is the
            required number of pixels to rais the subsequent hiragana block
            - this should be a negative number and will be used as a partameter
            to css margin-left attribute
        '''

        doc, tag, text = Doc().tagtext()
        with tag('div',('class','kanji_writing')):
            with tag('div',('class','kanji_box')):
                doc.stag('img', src='/static/kanji-box.png', height=self.render_mode[mode])
        # now eat the block nom nom nom
            with tag('div',('class','furigana')):
                    # extract the kanji characters and out put them in the div
                    text(question[0:question.find(self.te_writing)])
        return (doc.getvalue(), 0)



########################################################### combination question
    def combo(self,question,mode):
        '''
        This renders a combination question

        Returns
        -------
        tuple (str,int)
            the string is the doc tree to send to the output, the int is the
            required number of pixels to rais the subsequent hiragana block
            - this should be a negative number and will be used as a partameter
            to css margin-left attribute
        '''
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
        return (doc.getvalue(), 0)



#################################################################### constructor
    def __init__(self,question_bundle):
        super().__init__(question_bundle)
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



################################################################ render question
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



############################################################### render a preview
    def render(self):
        '''
        This renders an in-line preview of a question set
        '''
        doc, tag, text = Doc().tagtext()


        with tag('div',('class','preview')):
            for question in self.question_list:

                #initialize string indexer
                si = 0
                raise_next = 0
                #render a question in its own div
                with tag('div',('class','question')):
                    while question[si:] != '':

                        #if we are dealing with a token marker, start token processing
                        if question[si] in self.tokens:
                            renderd_question = self.render_question(question[si:],'preview')
                            doc.asis(renderd_question[0])
                            raise_next = renderd_question[1]
                            #eat the token untill we find its closure
                            while question[si] not in self.close_tokens:
                                si+=1

                            si+=1 # eat the closing marker of this token
                        else: #this is just "normal" output

                            # if we got a raise parameter from the render_question call
                            # this is where we'll use it
                            div_style = ''
                            if raise_next != 0:
                                    div_style = f'margin-top: {raise_next}px'
                            with tag('div',('class','hiragana'), style=div_style):
                                with tag('div'):
                                    h = ""
                                    while (question[si-1:]!='') and (question[si:si+1] not in self.tokens) :
                                        h=h+question[si]
                                        si+=1
                                    text(h)
                                with tag('div', width='30px'):
                                    text(' ')
        return doc.getvalue()