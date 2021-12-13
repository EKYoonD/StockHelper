import pandas as pd

with open('static/data/except_words.txt', 'r', encoding='utf-8') as f:
    except_words = list(map(lambda line: line.replace('\n', ''), f.readlines()))

print(except_words)