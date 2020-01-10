from hktm.questions.QuestionBase import QuestionBase
from yattag import Doc

class ComboQuestion(QuestionBase):
    """
    This is the class for combination type questions.
    """

    def __init__(self,question_type, question_text):
        super().__init__(question_type, question_text)

    def render(self):
        doc, tag, text = Doc().tagtext()

        with tag('div', ('class','question')):
            #initialize string indexer
            si = 0
            #eat the question string untill we are done
            while self.question_text[si:] != '':

                #if the character at the indexer is the start block character
                if self.question_text[si]=='{':
                    #create the tags
                    with tag('div',('class','kanji_writing')):
                        with tag('div'):
                            doc.stag('img', src='/static/kanji-box.png', height='90px')
                    # now eat the block nom nom nom
                        with tag('div',('class','furigana')):
                                # extract the kanji characters and out put them in the div
                                text(self.question_text[si+1:self.question_text.find('}',si)])

                    si = self.question_text.find('}',si)+1
                else:
                    # other wise its not a kanji block, so output it as standard reading text
                    with tag('div',('class','hiragana')):
                        # check if ther are other kanji blocks in the string
                        if self.question_text.find('{',si) == -1: #no more kanji blocks
                            text(self.question_text[si:])
                            #eat the rest of the string
                            si = len(self.question_text)

                        else: #there are kanji blocks
                            # so output reading text untill we encouter the next kanji block
                            text(self.question_text[si:self.question_text.find('{',si)])
                            # eat the text by moving the indexer over it
                            si=si+1
                            #si = self.question_text.find('[',si)+1

        return doc.getvalue()
