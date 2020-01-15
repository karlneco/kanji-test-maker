from hktm.lesson_contents.RenderContentBase import RenderContentBase
from yattag import Doc

class RenderContentKJWR(RenderContentBase):
    """
    This is the class for rendering writing kanji sheet.
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
        The renders the a single question in whatever format its required for
        the worksheet
        '''
        doc, tag, text = Doc().tagtext()
        question_data = question.split('｜')
        with tag('div', ('class','kjwr_question')):
            with tag('div',('class','kjwr_hiragana')):
                text(question_data[0])
            with tag('div',('class','kjwr_boxes')):
                print(question_data[1])
                for n in range(int(question_data[1])):
                    with tag('div',('class','kjwr_empty')):
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
            for q in self.question_list:
                renderd_question = self.render_question(q,'preview')
                doc.asis(renderd_question)
        return doc.getvalue()
