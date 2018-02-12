#https://pypi.python.org/pypi/liwc
import re
from collections import Counter

def tokenize(text):
    # you may want to use a smarter tokenizer
    for match in re.finditer(r'\w+', text, re.UNICODE):
        yield match.group(0)

import liwc
parse, category_names = liwc.load_token_parser('LIWC2007_English100131.dic')