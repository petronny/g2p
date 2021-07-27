#!/bin/python3
import os
import logging
from optparse import Values
import SequiturTool
from sequitur import Translator
from functools import lru_cache
logger = logging.getLogger()
__dict_path__ = os.path.join(os.path.dirname(__file__), 'cmudict', 'cmudict.dict')
__symbol_path__ = os.path.join(os.path.dirname(__file__), 'cmudict', 'cmudict.symbols')
__model_path__ = os.path.join(os.path.dirname(__file__), 'models', 'order-9')

try:
    from .. en_gb import G2P as G2P_base
except:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from en_gb import G2P as G2P_base

class G2P(G2P_base):

    def __init__(self, dict_path=__dict_path__, model_path=__model_path__, symbol_path=__symbol_path__):
        super().__init__(dict_path, model_path, symbol_path)

if __name__ == '__main__':
    g2p = G2P()
    print(g2p.convert('hello'))
    print(g2p.convert('github'))
