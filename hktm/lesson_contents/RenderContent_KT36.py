from hktm.lesson_contents.KanjiTestBase import KanjiTestBase
from yattag import Doc

class RenderContentKT36(KanjiTestBase):
    """
    This is the class for rendering kanji tests.
    """





#################################################################### constructor
    def __init__(self,question_bundle):
        super().__init__(question_bundle)

        self.render_mode = {
            'pdf':'90px',
            'preview':'80'
            }


############################################################### render a preview
    def render(self):
        '''
        This renders an in-line preview of a question set
        '''
        doc, tag, text = Doc().tagtext()


        with tag('div',('class','preview'),style="--colwidth:55px;"):
            for question in self.question_list:

                #initialize string indexer
                si = 0
                raise_next = 0
                #render a question in its own div
                with tag('div',('class','question')):
                    while question[si:] != '':

                        #if we are dealing with a token marker, start token processing
                        if question[si] in self.tokens:
                            if question[si] == self.ts_reading:
                                renderd_question = self.reading(question[si+1:],'preview')
                            elif question[si] == self.ts_writing:
                                renderd_question = self.writing(question[si+1:],'preview')
                            elif question[si] == self.ts_furi:
                                renderd_question = self.furigana(question[si+1:],'preview')
                            elif question[si] == self.ts_combo:
                                renderd_question = self.combo(question[si+1:],'preview')
                            elif question[si] == self.ts_bonus:
                                renderd_question = self.bonus(question[si+1:],'preview')

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
