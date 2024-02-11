#!/usr/bin/env python3

import sqlite3
from goodname import GoodName

'''
pick_name.py is an easy tool for picking good name.
Easily modify main function for your use.
You can find result in result.txt.
Progress count can find in search_progress.txt.

Techniques we use are 三才五格 and 81 靈動數字.

We use Moe-dictionary filtering some words we prefer.
This can prevent so many words to pick out.

some useful sample function can refer to:
    find_some_words_with_radical()
    find_some_words_with_attributes()
'''


class DictDb:
    def __init__(self):
        self.conn = sqlite3.connect("dict-revised.sqlite3")

    def query(self, sql, *bind):
        c = self.conn.cursor()
        c.execute(sql, *bind)
        result = c.fetchall()
        c.close()
        return result

    def close(self):
        self.conn.commit()
        self.conn.close()


def find_some_words_with_attributes(attributes=["美玉"]):
    db = DictDb()
    try:
        # search definitions which contain the attributes.
        # It's better to check the words manually via print out.
        condition = 'WHERE ' + \
            ' OR '.join(['definitions.def LIKE ?' for _ in attributes])

        q = f"SELECT entries.title, heteronyms.bopomofo, definitions.def \
              FROM definitions \
              JOIN heteronyms ON definitions.heteronym_id = heteronyms.id \
              JOIN entries ON heteronyms.entry_id = entries.id \
              {condition}"

        res = db.query(q,
                       tuple([f"%{attr}%" for attr in attributes]))

        # filter one word result
        filter_word_list = [
           r[0] for r in res if len(r[0]) == 1
        ]

        # print("title, bopomofo, definitions")
        # for r in res:
        #     print(f"{r[0]}, {r[1]}, {r[2]}")
    finally:
        db.close()

    return filter_word_list


def find_some_words_with_radical():
    db = DictDb()
    try:
        condition = 'WHERE entries.stroke_count > 6 AND ' \
                    'entries.stroke_count < 10 AND ' \
                    '(entries.radical == "心" OR entries.radical == "人")'

        q = f"SELECT entries.title \
              FROM entries \
              {condition}"

        word_list = db.query(q)

        # some special words like {[8e40]} we don't want to consider.
        filter_word_list = [
           w[0] for w in word_list if not w[0].startswith('{')
        ]

        # print(filter_word_list)
    finally:
        db.close()

    return filter_word_list


def main():

    # find words example
    filter_word_list_1 = find_some_words_with_attributes(["美玉"])
    filter_word_list_2 = find_some_words_with_radical()

    # Pick name - main logic for picking name
    name = GoodName()

    filter_word_list = list(filter_word_list_1)
    filter_word_list.extend(filter_word_list_2)

    total_search_count = pow(len(filter_word_list), 2)
    print(f"total need to search:"
          f"{len(filter_word_list)} ^ 2 = {total_search_count}")

    with open("result.txt", "w") as f1:
        with open("search_progress.txt", "w") as f2:
            count = 0
            for w1 in list(filter_word_list):
                for w2 in list(filter_word_list):
                    try:
                        name.set_name("林" + w1 + w2)
                        if name.is_good_name():
                            f1.write(f"{name.get_name()}\n")
                            f1.flush()

                        count += 1
                        if count % (round(total_search_count / 1000)) == 1:
                            f2.write(f"search: {count}\n")
                            f2.flush()
                    except Exception as e:
                        print(f"unknown error: {e}, skip")
                        continue


if __name__ == "__main__":
    main()
