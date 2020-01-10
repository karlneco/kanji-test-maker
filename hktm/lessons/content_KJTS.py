from yattag import Doc

class ContentKJTS():
    """
    This is the class for rednering kanji tests.
    """

    def __init__(self,question_bundle):
        self.question_list = question_bundle.splitlines()

    def render(self):
        pass

    def preview(self):
        doc, tag, text = Doc().tagtext()

        with tag('div',('class','preview')):
            for question in self.question_list:
                si = 0;

                with tag('div',('class','question')):
                    while question[si:] != '':
                        



        return doc.getvalue()
