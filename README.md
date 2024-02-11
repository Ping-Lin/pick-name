# pick-name
Pick a good name!

We use Moe Dictionary for searching some words we want,
and naming techniques are 三才五格 and 81 靈動數字.

## check_name.py example

```
林大明

三才
水木木:吉

五格
[9, 11, 11, 31, 21]
天格(9): 凶「凶惡」利去名空，窮迫慘淡，逆運遭難，短命失怙。
人格(11): 吉「逢春」陰陽新復，萬事順遂，穩健著實，富貴繁衍。
地格(11): 吉「逢春」陰陽新復，萬事順遂，穩健著實，富貴繁衍。
總格(31): 吉「勇志」俱智仁勇，越挫越振，統御力強，名成利就。
外格(21): 吉「明月」獨立權威，首領群倫，富貴榮顯，女性主寡。

is good name: True
```

## pick_name.py example

write some filter function or put the words you want to find good name.

### filter function example

``` python
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
```

- find the stroke count between 7 ~ 9 and radical is "心" or "人"

``` python
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
```

- find the definition of word matching "美玉"

### result.txt
```
林琦珵
林琦球
林琦璦
林琦璨
林琦佩
林琦佪
林琦佬
...
```

## Reference

### Moe Dict
#### data source

- https://github.com/g0v/moedict-data
- source: dict-revised.json (2018/01/03, caac9b5)

#### data process

- https://github.com/g0v/moedict-process
- we use this project to turn json into sqlite3.
- also see: https://github.com/g0v/moedict-webkit/blob/master/README.md?source=post_page-----00c1bd06f09f--------------------------------

### kangxi-strokecount

- https://github.com/breezyreeds/kangxi-strokecount
- 三才五格 need to use kangxi dictionary for stroke count.
