import re
import base64
import io
import tempfile
from PIL import Image

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

def get_question_bounds(question_blocks, next_question = None) -> list[tuple[int, int]]:
    blocks_vertices = [get_block_vertices(block) for block in question_blocks]
    top_lefts = [vertices[0] for vertices in blocks_vertices]
    bottom_rights = [vertices[2] for vertices in blocks_vertices]

    top = min([vertex[1] for vertex in top_lefts]) - 10
    left = min([vertex[0] for vertex in top_lefts]) - 10
    bottom = get_block_vertices(next_question[0])[0][1] if next_question else  max([vertex[1] for vertex in bottom_rights]) + 10
    right = max([vertex[0] for vertex in bottom_rights]) + 10

    return [(left, top), (right, top), (right, bottom), (left, bottom)]

def extract_image(page, fname):
    with open(fname, 'wb') as fp:
        fp.write(base64.decodebytes(bytes(page['image']['content'], 'utf-8')))

def extract_question_image(imgfile, bounds, outfile = None):
    #with open(imgfile, 'rb') as fp:
    #    buf_fp = io.BytesIO(fp.read())

    with Image.open(imgfile) as im:
        result = im.crop(box=(bounds[0][0], bounds[0][1], bounds[2][0], bounds[2][1]) )
    
    output = ''
    if outfile:
        with open(outfile, "wb") as out_fp:
            result.save(out_fp)
        with open(outfile, "rb") as fp:
            output = base64.encodebytes(fp.read())
    else:
        with tempfile.TemporaryFile() as outfp:
            result.save(outfp, format='PNG')
            outfp.seek(0, 0)
            output = base64.encodebytes(outfp.read())
    

    #with io.BytesIO() as buf_fp:
    #result.save(buf_fp, format='PNG')
    #output = base64.encodebytes(buf_fp.read())
    #output = buf_fp.read()
    #buf_fp.close()

    return output

    
def write_image(image_base64, fname):
    with open(fname, 'wb') as fp:
        fp.write(base64.decodebytes(image_base64))
        #fp.write(image_base64)
