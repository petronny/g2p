#!/bin/python3
import os
import re
from pypinyin import pinyin, Style
from functools import lru_cache

try:
    from split_pinyin_sp.split_pinyin import split_pinyin
except:
    from .split_pinyin_sp.split_pinyin import split_pinyin

class G2P:

    @lru_cache(maxsize=None)
    def __getitem__(self, key):
        result = [i[0] for i in pinyin(key, style=Style.TONE3)]
        result = [re.sub(r'^([a-z]*$)', '\g<1>5', i) for i in result]
        result = [re.sub(r'^ ', '','%s %s%s' % split_pinyin(i)[:3]).split() for i in result]
        return result

if __name__ == '__main__':
    g2p = G2P()
    print(g2p['我们'])
