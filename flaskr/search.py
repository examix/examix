import flaskr.db as db


def parse_search(search_string):
    string_list = search_string.split()
    dept = None
    code = None
    school = None
    schools_in_db = db.get_schools()

    for string in string_list:
        if string[0].isnumeric():
            code = string.upper()
        elif string in schools_in_db:
            school = string.lower()
        else:
            dept = string
    return [dept, code, school]
