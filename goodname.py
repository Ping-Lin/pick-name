#!/usr/bin/env python3

import csv
from collections import defaultdict


class GoodName:
    # FIXME, consider only 3 words name now
    def __init__(self, name="王大明"):
        self._stroke_word_mapping = defaultdict(list)   # 1: [..., ]
        self._word_stroke_mapping = dict()   # "一": 1
        self._81_fortune_mapping = dict()   # 1: "..."
        self._5_phases_fortune_mapping = dict()   # "金金金": "平"
        self._name_list = list(name)

        self._init_stroke_and_word_mappings()
        self._init_81_fortune_mapping()
        self._init_5_phases_fortune_mapping()

    def __str__(self):
        res = ""
        res += self.get_name()
        res += f"\n\n三才\n{self.get_three_talent()}:" \
               f"{self.get_three_talent_fortune()}"
        res += f"\n\n五格\n{self.get_five_personailty()}\n" \
               f"{self.get_five_personailty_desc()}"
        return res

    def set_name(self, name: str):
        self._name_list = list(name)

    def get_name(self) -> str:
        return ''.join(map(str, self._name_list))

    def _init_stroke_and_word_mappings(self):
        with open("kangxi-strokecount.csv",
                  newline="", encoding="utf-8") as csvfile:
            # skip license statement
            for _ in range(5):
                csvfile.readline()

            # read file
            reader = csv.reader(csvfile)
            for row in reader:
                self._stroke_word_mapping[int(row[3])].extend(row[2].strip())
                self._word_stroke_mapping[row[2].strip()] = int(row[3])

    def _init_81_fortune_mapping(self):
        # 81 靈動數字
        # ref: https://guangyuan.tw/81bihua.php
        with open("81-fortune.csv",
                  newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self._81_fortune_mapping[int(row[0])] = \
                    {"fortune": row[1].strip(), "desc": row[2].strip()}

    def _init_5_phases_fortune_mapping(self):
        # 三才五格配置吉凶論斷
        # ref: https://www.356.com.tw/teaching/?parent_id=1274
        with open("5-phases-fortune.csv",
                  newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self._5_phases_fortune_mapping[''.join(row[0:3])] = \
                        row[3].strip()

    def _god_personality(self) -> int:
        # 天格
        num = 1 + self._word_stroke_mapping[self._name_list[0]]
        return (num - 1) % 81 + 1

    def _man_personality(self) -> int:
        # 人格
        num = self._word_stroke_mapping[self._name_list[0]] + \
               self._word_stroke_mapping[self._name_list[1]]
        return (num - 1) % 81 + 1

    def _ground_personality(self) -> int:
        # 地格
        num = self._word_stroke_mapping[self._name_list[1]] + \
               self._word_stroke_mapping[self._name_list[2]]
        return (num - 1) % 81 + 1

    def _total_personality(self) -> int:
        # 總格
        num = self._god_personality() + \
               self._man_personality() + \
               self._ground_personality()
        return (num - 1) % 81 + 1

    def _out_personality(self) -> int:
        # 外格
        num = self._total_personality() - self._man_personality() + 1
        return (num - 1) % 81 + 1

    def _element_convert(self, num: int) -> str:
        # Metal Wood Water Fire Earth
        while num > 10:
            num = num % 10
        if num == 1 or num == 2:
            return "木"
        elif num == 3 or num == 4:
            return "火"
        elif num == 5 or num == 6:
            return "土"
        elif num == 7 or num == 8:
            return "金"
        elif num == 9 or num == 0:
            return "水"
        else:
            return "ERROR"

    def get_three_talent(self) -> str:
        # 三才
        res = "".join([
            self._element_convert(self._god_personality()),
            self._element_convert(self._man_personality()),
            self._element_convert(self._ground_personality()),
        ])
        return res

    def get_three_talent_fortune(self) -> str:
        return f"{self._5_phases_fortune_mapping[self.get_three_talent()]}"

    def get_81_fortune(self, num: int) -> str:
        return self._81_fortune_mapping[num]["fortune"]

    def get_81_fortune_desc(self, num: int) -> str:
        return self._81_fortune_mapping[num]["desc"]

    def get_five_personailty(self) -> list:
        # 五格
        return [
            self._god_personality(),
            self._man_personality(),
            self._ground_personality(),
            self._total_personality(),
            self._out_personality()
        ]

    def get_five_personailty_desc(self) -> str:
        # 五格
        res = ""
        res += f"天格({self._god_personality()}): " + \
               f"{self.get_81_fortune(self._god_personality())}" + \
               f"{self.get_81_fortune_desc(self._god_personality())}\n"

        res += f"人格({self._man_personality()}): " + \
               f"{self.get_81_fortune(self._man_personality())}" + \
               f"{self.get_81_fortune_desc(self._man_personality())}\n"

        res += f"地格({self._ground_personality()}): " + \
               f"{self.get_81_fortune(self._ground_personality())}" + \
               f"{self.get_81_fortune_desc(self._ground_personality())}\n"

        res += f"總格({self._total_personality()}): " + \
               f"{self.get_81_fortune(self._total_personality())}" + \
               f"{self.get_81_fortune_desc(self._total_personality())}\n"

        res += f"外格({self._out_personality()}): " + \
               f"{self.get_81_fortune(self._out_personality())}" + \
               f"{self.get_81_fortune_desc(self._out_personality())}\n"
        return res

    def get_stroke_words_list(self, num: int) -> list:
        return self._stroke_word_mapping[num]

    def get_word_stroke(self, word: str) -> int:
        return self._word_stroke_mapping[word]

    def get_all_words(self) -> list:
        return list(self._word_stroke_mapping.keys())

    def is_good_name(self) -> bool:
        count = 0

        # Last name may always be calculated to "凶". (Eg. 林)
        # Count "凶" twice for condition of bad name.
        for num in self.get_five_personailty():
            if self.get_81_fortune(num) == "凶":
                count += 1
            if count >= 2:
                return False

        # 平上, 次吉, 吉 are ok!
        if self.get_three_talent_fortune() == "平下" or \
           self.get_three_talent_fortune() == "平":
            return False

        return True
