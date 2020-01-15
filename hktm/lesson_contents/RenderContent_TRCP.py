from hktm.lesson_contents.RenderContentBase import RenderContentBase
from yattag import Doc

class RenderContentTRCP(RenderContentBase):
    """
    This is the class for rendering kanji tracing sheet
    """


#################################################################### constructor
    def __init__(self,question_bundle):
        super().__init__(question_bundle)
        self.kanjis = question_bundle
        self.render_mode = {
            'pdf':'90px',
            'preview':'60px'
            }


####################################################### render a single question
    def render_question(self, question, mode):
        '''
        The renders the a single question in whatever format its required for
        the worksheet
        '''
        doc, tag, text = Doc().tagtext()
        with tag('div', ('class','trcp_question')):
            with tag('div',('class','trcp_char')):
                text(question)
            with tag('div',('class','trcp_char ghost')):
                text(question)
            for n in range(6):
                with tag('div',('class','trcp_empty')):
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
            for k in self.kanjis:
                renderd_question = self.render_question(k,'preview')
                doc.asis(renderd_question)
        return doc.getvalue()
