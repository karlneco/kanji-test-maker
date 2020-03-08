from hktm.lesson_contents.RenderContent_KT36 import RenderContentKT36
from yattag import Doc

class RenderContentK362(RenderContentKT36):
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
