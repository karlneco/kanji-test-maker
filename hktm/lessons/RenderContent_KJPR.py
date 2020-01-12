from hktm.lessons.RenderContentBase import RenderContentBase
from yattag import Doc

class RenderContentKJPR(RenderContentBase):
    """
    This is the class for rednering kanji practice sheet.
    """

#################################################################### constructor
    def __init__(self,question_bundle):
        super().__init__(question_bundle)
        self.render_mode = {
            'pdf':'90px',
            'preview':'60px'
            }

####################################################### render a single question
    def render_question(self, question, mode):
        '''
        The renders a single question given the question content (or kanji
        in this case)
        '''
        return tokens.get(question[0],'nothing')


################################################################ render the page
    def render(self):
        '''
        This renders an in-line preview of a question set
        '''
        doc, tag, text = Doc().tagtext()


        # traverse the list of kanji and crete the corresponding kanji practice
        # block
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
