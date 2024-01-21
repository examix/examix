from flaskr.exam import Exam, Page, Question
import flaskr.db as db
import random, itertools

ACCEPTABLE_ERROR = 1.2

def question_score(question) -> float:
    return question.duration * question.difficulty

def calc_exam_difficulty(exam) -> float:
    scores = []

    for page in exam.pages:
        scores += [question_score(question) for question in page.questions]

    return sum(scores) / exam.duration

def calc_time_diff(cur_time, exp_time):
    return abs(cur_time - exp_time) / exp_time

def calc_dieviation(new_items, ext_avg, total_dur, exp_avg):
    new_avg = (sum([item['duration']*item['difficulty'] for item in new_items])+(ext_avg*total_dur)) / (total_dur + sum([item['duration'] for item in new_items])) 

    return abs(new_avg-exp_avg) - abs(ext_avg-exp_avg), new_avg

def remix(exp_time, diff, school="uvic", department="CSC", course_code="110"):
    questions = db.get_questions_db()

    seed_q = questions.pop(random.randint(0, len(questions) - 1))
    time = seed_q['duration']
    time_diff = calc_time_diff(time, exp_time)
    cur_difficulty = seed_q['difficulty']
    results = [seed_q]

    while time_diff > 0.2 and time <= exp_time:
        singles = []
        doubles = []
        for question in questions:
            cur_deiv, new_avg =  calc_dieviation([question], cur_difficulty, time, diff)
            singles.append( ([question], cur_deiv, new_avg) )

        for q_pair in itertools.product(questions, questions):
            cur_deiv, new_avg =  calc_dieviation(q_pair, cur_difficulty, time, diff)
            doubles.append( (q_pair, cur_deiv, new_avg) )

        candidates = sorted(singles + doubles, key=lambda x: x[1])

        if not candidates:
            break

        new_time = time + sum([q[1] for q in candidates[0][0]])
        while candidates and new_time > exp_time*ACCEPTABLE_ERROR:
            candidates.pop(0) 
            new_time = time + sum([q[1] for q in candidates[0][0]] if candidates else [])
        
        if not candidates:
            break
        
        new_qs = candidates.pop(0)
        questions = [question for question in questions if question not in new_qs[0]]
        results.extend(new_qs[0])

        time = new_time
        cur_difficulty =  new_qs[2]
        time_diff = calc_time_diff(time, exp_time)
        
    results_dict = [  { key : result[key] for key in result.keys() } for result in results  ]
    return results_dict, time, cur_difficulty
