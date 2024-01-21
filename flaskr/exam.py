class Exam:
    def __init__(self, num_pages, difficulty, prof, pdf_name, duration, date, exam_type, num_questions, pages, school,
                 department=None, course_code=None):
        self.num_pages = num_pages
        self.difficulty = difficulty
        self.prof = prof
        self.pdf_name = pdf_name
        self.duration = duration
        self.date = date
        self.exam_type = exam_type
        self.num_questions = num_questions
        self.pages = pages
        self.school = school
        self.department = department 
        self.course_code = course_code
        self.department = department
        self.course_code = course_code


class Page:
    def __init__(self, page_num, width, height, questions=None):
        self.page_num = page_num
        self.width = width
        self.height = height
        self.questions = questions

class Course:
    def __init__(self, department, course_code, course_name, description, school):
        self.department = department
        self.course_code = course_code
        self.course_name = course_name
        self.description = description
        self.school = school

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

