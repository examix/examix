import re
import base64

def get_blocks(json, page_num): 
    return sorted(json['pages'][page_num]['blocks'], key=get_block_vert)

def get_text_bounds(block, text_len) -> list[tuple[int, int]]:
    seg_dicts =  block['layout']['textAnchor']['textSegments']
    
    results = []

    for seg in seg_dicts:
        start = int(seg['startIndex']) if 'startIndex' in seg else 0
        end   = int(seg['endIndex']) if 'endIndex' in seg else text_len
        results.append( (start, end) )

    return results

def get_block_text(json, block):
    text = json['text']
    text_len = len(text)

    return ''.join([text[seg_strt:seg_end] for seg_strt, seg_end in get_text_bounds(block, text_len)])
    
def get_block_vertices(block) -> list[tuple[int, int]]:
    return [ (int(vertex['x']), int(vertex['y'])) for vertex in block['layout']['boundingPoly']['vertices'] ]

def get_block_vert(block) -> int:
    # first vertex seems to always be the top-left vertex
    return int(block['layout']['boundingPoly']['vertices'][0]['y'])

def get_question_blocks(json, page_num) -> list[list[dict]]:
    blocks = get_blocks(json, page_num)

    in_question = False
    cur_question = []
    results = []

    for block in blocks:

        text = get_block_text(json, block)

        # question border
        if re.match("\d*\.", text, flags=re.DOTALL):
            if in_question:
                results.append(cur_question)
            #else:
            cur_question = [block]

            #in_question = not in_question
            in_question = True
        elif in_question:
            cur_question.append(block)

    if cur_question: results.append(cur_question)
    return results

def get_question_text(json, question_blocks) -> str:
    return ''.join([get_block_text(json, block) for block in question_blocks])

def get_question_bounds(question_blocks) -> list[tuple[int, int]]:
    blocks_vertices = [get_block_vertices(block) for block in question_blocks]
    top_lefts = [vertices[0] for vertices in blocks_vertices]
    bottom_rights = [vertices[2] for vertices in blocks_vertices]

    top = min([vertex[1] for vertex in top_lefts])
    left = min([vertex[0] for vertex in top_lefts])
    bottom = max([vertex[1] for vertex in bottom_rights])
    right = max([vertex[0] for vertex in bottom_rights])

    return [(left, top), (right, top), (right, bottom), (left, bottom)]

def extract_image(page, fname):
    with open(fname, 'wb') as fp:
        fp.write(base64.decodebytes(bytes(page['image']['content'], 'utf-8')))
