DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS exam;
DROP TABLE IF EXISTS school;
DROP TABLE IF EXISTS school_alternates;
DROP TABLE IF EXISTS page;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE course (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department TEXT(4),
    code TEXT(4),
    name TEXT,
    description TEXT(200),
    school_id TEXT,
    CONSTRAINT Course_School_FK FOREIGN KEY (school_id) REFERENCES School(name) ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE question (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    answer TEXT,
    difficulty FLOAT,
    page_num INTEGER,
    vertices TEXT,
    question_type TEXT,
    num_points INTEGER,
    exam_image BLOB,
    duration FLOAT,
    exam_id INTEGER,
    question TEXT(200),
    CONSTRAINT Exam_FK FOREIGN KEY (exam_id) REFERENCES Exam(exam_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT Page_FK FOREIGN KEY (page_id) REFERENCES Page(page_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE page(
    page_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER,
    page_num INTEGER,
    width FLOAT,
    height FLOAT,
    CONSTRAINT Exam_FK FOREIGN KEY (exam_id) REFERENCES Exam(exam_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE exam(
    exam_id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER,
    school_id TEXT,
    num_pages INTEGER,
    difficulty INTEGER,
    prof TEXT(200),
    pdf_name TEXT,
    duration FLOAT,
    exam_date DATE,
    exam_type TEXT,
    num_questions INTEGER,
    num_points INTEGER,
    pages INTEGER,
    num_points INTEGER,
    CONSTRAINT Course_FK FOREIGN KEY (course_id) REFERENCES Course(course_id) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT School_FK FOREIGN KEY (school_id) REFERENCES School(name) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE school (
    name TEXT PRIMARY KEY,
    city TEXT,
    country TEXT
);

CREATE TABLE school_alternates (
    name TEXT PRIMARY KEY,
    default_name TEXT,
    CONSTRAINT School_FK FOREIGN KEY (default_name) REFERENCES School(name) ON DELETE CASCADE ON UPDATE CASCADE
);


