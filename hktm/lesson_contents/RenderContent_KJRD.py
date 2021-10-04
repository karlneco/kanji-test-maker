from hktm.lesson_contents.RenderContentBase import RenderContentBase

from yattag import Doc

class RenderContentKJRD(RenderContentBase):
    """
    This is the class for rendering kanji reading practice sheet.
    """

#################################################################### constructor
    def __init__(self,question_bundle):
        super().__init__(question_bundle)
        self.render_mode = {
            'pdf':'90px',
            'preview':'90'
            }

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
        with tag('div',('class','kanji_reading-'+self.render_mode[mode])):
            with tag('div'):
                # extract the kanji characters and out put them in the div
                text(question[0:question.find(self.te_reading)])
            # check if the question needs more space for the hiragaana te_writing
            # this is requested by adding 'japanse spaces' to the kanji characeter
            if ('　' in question[0:question.find(self.te_reading)]):
                rise_next = -40 #if so then tell the main rendere to raise the next hiragana block

            # now eat the block nom nom nom
            with tag('div',('class','kanji_reading_brackets-'+self.render_mode[mode])):
                doc.stag('img', src='/static/top_bracket.png', width="27px")
                with tag('div'):
                    for i in range(len(question[0:question.find(self.te_reading)])):
                        with tag('span',('class','kanji-reading-spacer')):
                            text(' ')
                doc.stag('img', src='/static/btm_bracket.png', width="27px")
        return (doc.getvalue(), rise_next)

####################################################### render a single question
    def render_question(self, question, mode):
        doc, tag, text = Doc().tagtext()
        si = 0
        raise_next = 0
        #render a question in its own div
        with tag('div',('class','kjrd_question')):
            while question[si:] != '':

                #if we are dealing with a token marker, start token processing
                if question[si] in self.ts_reading:
                    renderd_question = self.reading(question[si+1:],'preview')
                    doc.asis(renderd_question[0])
                    raise_next = renderd_question[1]
                    #eat the token untill we find its closure
                    while question[si] not in self.te_reading:
                        si+=1

                    si+=1 # eat the closing marker of this token
                else: #this is just "normal" output

                    # if we got a raise parameter from the render_question call
                    # this is where we'll use it
                    div_style = ''
                    if raise_next != 0:
                            div_style = f'margin-top: {raise_next}px'
                    with tag('div',('class','hiragana-90'), style=div_style):
                        with tag('div',('class','hiragana-content')):
                            with tag('div'):
                                text(' ')
                            with tag('div'):
                                h = ""
                                while (question[si-1:]!='') and (question[si:si+1] not in self.tokens) :
                                    h=h+question[si]
                                    si+=1
                                text(h)
                            with tag('div'):
                                text(' ')
                        with tag('div'):
                            text(' ')
                        text(' ')
        return doc.getvalue()



################################################################ render the page
    def render(self):
        '''
        This renders an in-line preview of a question set
        '''
        doc, tag, text = Doc().tagtext()

        # go through the question in the list and produce the represrentation
        # for each question
        with tag('div',('class','preview')):
            with tag('div',('class','kjrd_layout')):
                with tag('div',('class','col1')):
                    for q in self.question_list[0::2]:
                        renderd_question = self.render_question(q,'preview')
                        doc.asis(renderd_question)
                with tag('div',('class','col2')):
                    for q in self.question_list[1::2]:
                        renderd_question = self.render_question(q,'preview')
                        doc.asis(renderd_question)



        return doc.getvalue()
