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
                doc.stag('img', src='/static/top_bracket.png', width="100%")
                with tag('div'):
                    for i in range(len(question[0:question.find(self.te_reading)])):
                        with tag('span',('class','kanji-reading-spacer')):
                            text(' ')
                doc.stag('img', src='/static/btm_bracket.png', width="100%")
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
        with tag('div',('class','kanji_writing-'+self.render_mode[mode])):
            with tag('div',('class','kanji_box')):
                doc.stag('img', src='/static/kanji-box.png', height=self.render_mode[mode]+'px')
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
        token_parts = token.split('｜')
        if '｜' not in token:
            return ('Syntax Error',0)

        with tag('div',('class','combo_question-'+self.render_mode[mode])):
            with tag('div'):
                doc.stag('img', src='/static/top_brace.png', height='20px')
                for c in range(int(token_parts[1])):
                    doc.stag('img', src='/static/empty.png', height=self.render_mode[mode]+'px')
                doc.stag('img', src='/static/btm_brace.png', height='20px')
            # now eat the block nom nom nom
            with tag('div',('class','furigana-combo')):
                # extract the kanji characters and out put them in the div
                # with tag('div',('class','furigana-combo-row')):
                text(token_parts[0])
        return (doc.getvalue(), 0)


########################################################## furigana helping text
    def furigana(self,question,mode):
        '''
        This renders furigana ext to some kanji
        '''
        doc, tag, text = Doc().tagtext()

        # seperate the kanji from the furigana
        token = question[0:question.find(self.te_furi)]
        token_parts = token.split('｜')
        if '｜' not in token:
            return ('Syntax Error',0)

        #create the tags
        with tag('div',('class','kanji-w-furi-'+self.render_mode[mode])):
            #output the kanji
            with tag('div'):
                # extract the kanji characters and out put them in the div
                text(token_parts[0])

            #now the furigana
            with tag('div',('class','kanji-w-furi-furi-'+self.render_mode[mode])):
                with tag('div'):
                    text(token_parts[1])
        return (doc.getvalue(), 0)

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
        self.render_mode = {
            'pdf':'90px',
            'preview':'90'
            }
