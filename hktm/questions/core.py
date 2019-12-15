from hktm.questions.ReadingQuestion import ReadingQuestion
from hktm.questions.WritingQuestion import WritingQuestion
from hktm.questions.ComboQuestion import ComboQuestion
from hktm.models import Question

### the question object factory, returns the appropriate object based on the
#   'type' of question that is passed in
def question_factory(db_question):

    #is there a prettier way to do this .... hmmm
    if db_question.type == 1: base = ReadingQuestion
    elif db_question.type == 2: base = WritingQuestion
    else: base = ComboQuestion

    # instentiate the correct question type
    question_object = base(db_question.grade,db_question.question)

    return question_object
