#!/usr/bin/python3
# -*- coding: utf-8 -*-
# https://github.com/rupskygill/ML-mastery/blob/master/deep_learning_with_python_code/28_lstm_larger_gen_text.py

import sqlite3


LIMIT = 200000

def load_comments(limit):
    ret = []
    sql = 'SELECT * FROM Reviews LIMIT %d' % limit if limit > 0 else 'SELECT * FROM Reviews'
    conn = sqlite3.connect('./data/database.sqlite')
    c = conn.cursor()
    for row in c.execute(sql):
        comment = row[-1]
        ret.append(comment)
    return ret

comments = load_comments(LIMIT)
raw_text = '\n'.join(comments).lower()
with open('./data/raw.txt', 'w') as f:
    f.write(raw_text)