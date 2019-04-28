#!/bin/python3
import os
import re
import thulac
import jieba
from pypinyin import pinyin, Style
from functools import lru_cache
__dict__ = os.path.join(os.path.dirname(__file__), 'dict.txt')

try:
    from split_pinyin import split_pinyin
except:
    from .split_pinyin import split_pinyin

class G2P:
    __leading_spaces_re__ = re.compile(r'^ ')
    __leading_alphabets_re__ = re.compile(r'^([a-z]*$)')

    def __init__(self, user_dict=__dict__):
        self.__thulac__ = thulac.thulac(user_dict)

        for i in [i.strip('\r\n') for i in open(user_dict).readlines()]:
            jieba.add_word(i)

    @staticmethod
    @lru_cache(maxsize=None)
    def __to_phoneme__(i):
        return G2P.__leading_spaces_re__.sub('', '%s %s%s' % i[:3]).split() if type(i) is tuple else i

    @staticmethod
    @lru_cache(maxsize=None)
    def is_pinyin(text):
        if len(text) > 8:
            return False
        for i, j in enumerate(text):
            if i < len(text) - 2 and not j.isalpha():
                return False
            if i == len(text) - 2 and j.isdigit() and (int(j) > 5 or not text[-1] == 'r'):
                return False
            if i == len(text) - 2 and not j.isdigit() and not j.isalpha():
                return False
            if i == len(text) - 1 and j.isdigit() and int(j) > 5:
                return False
            if i == len(text) - 1 and not j.isdigit() and not j.isalpha():
                return False
        return True

    @staticmethod
    def __convert__(key):
            result = [i[0] for i in pinyin(key, style=Style.TONE3)]
            result = [G2P.__leading_alphabets_re__.sub('\g<1>5', i) for i in result]
            result = [split_pinyin(i) if G2P.is_pinyin(i) else i for i in result]
            for i, j in enumerate(result[:-1]):
                if not type(j) is tuple or not type(result[i + 1]) is tuple:
                    continue
                if j[2] == 3 and result[i + 1][2] == 3:
                    result[i] = j[:2] + (2 , ) + j[3:]
                if key[i] == '一' and key[i + 1] != '一' and j[2] == 1 and result[i + 1][2] != 4:
                    result[i] = j[:2] + (4 , ) + j[3:]
                if key[i] == '一' and j[2] == 1 and result[i + 1][2] == 4:
                    result[i] = j[:2] + (2 , ) + j[3:]
            return result

    def convert(self, key, tokenlization=True):
        if tokenlization:
            words = self.__thulac__.cut(key, text=True).split(' ')
            words = [i.split('_')[0] for i in words]
            #words = [i for i in jieba.cut(key)]
            #print(words)
            result = [G2P.__convert__(i) for i in words]
            for i, j in enumerate(result[:-1]):
                if len(j) == 1 and not type(j[0]) is tuple:
                    continue
                if len(result[i + 1]) == 1 and not type(result[i + 1][0]) is tuple:
                    continue
                #if len(j) == 1 and j[0][2] == 3 and len(result[i + 1]) == 1 and result[i + 1][0][2] == 3:
                #    result[i][0] = j[0][:2] + (2 , ) + j[0][3:]
                if words[i] == '不' and j[0][2] == 4 and result[i + 1][0][2] == 4:
                    result[i][0] = j[0][:2] + (2 , ) + j[0][3:]
                if words[i] == '一' and words[i + 1] != '一' and j[0][2] == 1 and result[i + 1][0][2] != 4:
                    result[i][0] = j[0][:2] + (4 , ) + j[0][3:]
                if words[i] == '一' and j[0][2] == 1 and result[i + 1][0][2] == 4:
                    result[i][0] = j[0][:2] + (2 , ) + j[0][3:]
            result = [[G2P.__to_phoneme__(i) for i in j] for j in result]
            #if len(result) == 1:
            #    result = result[0]
        else:
            result = G2P.__convert__(key)
            result = [G2P.__to_phoneme__(i) for i in result]
        return result

if __name__ == '__main__':
    import sys
    g2p = G2P()

    print(g2p.convert('岂有此理'))
    print(g2p.convert('手表厂有五种好产品'))
    print(g2p.convert('请你给我打点洗脸水'))
    print(g2p.convert('好小伙', False))
    print(g2p.convert('并不对应'))
    print(g2p.convert('才不对应'))
    print(g2p.convert('偏不对应'))
    print(g2p.convert('偏不吃菜'))
    print(g2p.convert('一致'))
    print(g2p.convert('不一致'))
    print(g2p.convert('一早一晚'))
    print(g2p.convert('一一对应'))
    print(g2p.convert('一朝'))
    print(g2p.convert('试一试'))
    print(g2p.convert('李二，不叫小明吃饭', True))
    print(g2p.convert('李二不，叫小明吃饭', True))
    print(g2p.convert('统一晚出'))
    print(g2p.convert('一早上'))
