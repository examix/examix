class Exam:
    def __init__(self, num_pages, difficulty, prof, pdf_name, time, date, exam_type, num_questions, pages):
        self.num_pages = num_pages
        self.difficulty = difficulty
        self.prof = prof
        self.pdf_name = pdf_name
        self.time = time
        self.date = date
        self.exam_type = exam_type
        self.num_questions = num_questions
        self.pages = pages


class Page:
    def __init__(self, num, width, height, questions=None):
        self.num = num
        self.width = width
        self.height = height
        self.questions = questions


class Question:
    def __init__(self, question_text, difficulty, page_num, vertices, question_type, num_points, exam_image, duration,
                 answer=None):
        self.question_text = question_text
        self.difficulty = difficulty
        self.page_num = page_num
        self.vertices = vertices
        self.question_type = question_type
        self.num_points = num_points
        self.exam_image = exam_image
        self.duration = duration
        self.answer = answer

