from hktm.lesson_contents.RenderContent_KJTS import RenderContentKJTS
from yattag import Doc

class RenderContentKT36(RenderContentKJTS):
    """
    This is the class for rendering kanji tests.
    """

################################################################　bonus question
    def bonus(self,question,mode):
        '''
        This renders a bonus part of a question

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
        with tag('div',('class','kanji_bonus')):
            with tag('div'):
                # extract the kanji characters and out put them in the div
                text(question[0:question.find(self.te_bonus)])
            # check if the question needs more space for the hiragaana te_writing
            # this is requested by adding 'japanse spaces' to the kanji characeter
            if ('　' in question[0:question.find(self.te_bonus)]):
                rise_next = -60 #if so then tell the main rendere to raise the next hiragana block

        return (doc.getvalue(), rise_next)



#################################################################### constructor
    def __init__(self,question_bundle):
        super().__init__(question_bundle)
        self.close_tokens = '）」｝＞'
        self.tokens = '（「｛＜'
        self.render_mode = {
            'pdf':'90px',
            'preview':'60'
            }




################################################################ render question
    def render_question(self, question, mode):
        '''
        The renders the question token in whatever mode is passed in
        '''
        tokens = {
           '（': self.reading(question[1:], mode),
           '「': self.writing(question[1:], mode),
           '｛': self.combo(question[1:], mode),
           '＜': self.bonus(question[1:], mode)
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
