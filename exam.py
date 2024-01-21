class Exam:
    def __init__(self, num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions, pages):
        self.num_pages = num_pages
        self.difficulty = difficulty
        self.prof = prof
        self.pdf_name = pdf_name
        self.duration = duration
        self.date = date
        self.exam_type = exam_type
        self.num_questions = num_questions
        self.pages = pages


class Page:
    def __init__(self, page_num, width, height, questions=None):
        self.page_num = page_num
        self.width = width
        self.height = height
        self.questions = questions


class Question:
    
    def __init__(self, num):
        self.__num = num
