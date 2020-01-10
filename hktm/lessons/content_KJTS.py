from yattag import Doc

class ContentKJTS():
    """
    This is the class for rednering kanji tests.
    """

    def reading(self,question):
        doc, tag, text = Doc().tagtext()
        #create the tags
        with tag('div',('class','kanji_reading')):
            with tag('div'):
                # extract the kanji characters and out put them in the div
                text(question[0:question.find(')')])
            # now eat the block nom nom nom
            with tag('div',('class','kanji_reading_brackets')):
                doc.stag('img', src='/static/top_bracket.png', height='20px')
                with tag('div'):
                    text(' ')
                doc.stag('img', src='/static/btm_bracket.png', height='20px')
        return doc.getvalue()

    def writing(self,question):
        doc, tag, text = Doc().tagtext()
        with tag('div',('class','kanji_writing')):
            with tag('div'):
                doc.stag('img', src='/static/kanji-box.png', height='90px')
        # now eat the block nom nom nom
            with tag('div',('class','furigana')):
                    # extract the kanji characters and out put them in the div
                    text(question[0:question.find(']')])
        return doc.getvalue()

    def combo(self,question):
        doc, tag, text = Doc().tagtext()
        return doc.getvalue()



    def __init__(self,question_bundle):
        self.question_list = question_bundle.splitlines()
        self.close_tokens = ')]}'
        self.tokens = '([{'


    def render_question(self,question):
        tokens = {
           '(': self.reading(question[1:]),
           '[': self.writing(question[1:]),
           'Z': self.combo(question[1:])
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
                            doc.asis(self.render_question(question[si:]))

                            #eat the token untill we find its closure
                            while question[si] not in self.close_tokens:
                                si+=1

                            si+=1 # eat the closing marker of this token
                        else: #this is just "normal" output
                            with tag('div',('class','hiragana')):
                                h = ""
                                while (question[si-1:]!='') and (question[si:si+1] not in self.tokens) :
                                    h=h+question[si]
                                    si+=1
                                text(h)
        return doc.getvalue()
