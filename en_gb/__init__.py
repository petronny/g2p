#!/bin/python3
import os
import logging
from optparse import Values
import SequiturTool
from sequitur import Translator
from functools import lru_cache
logger = logging.getLogger()
__dict_path__ = os.path.join(os.path.dirname(__file__), 'beep.dict')
__symbol_path__ = os.path.join(os.path.dirname(__file__), 'beep.symbols')
__model_path__ = os.path.join(os.path.dirname(__file__), 'models', 'order-9')

class G2P:
    def __init__(self, dict_path=__dict_path__, model_path=__model_path__, symbol_path=__symbol_path__):
        self._dict_ = dict()
        dict_path = os.path.expanduser(dict_path)
        model_path = os.path.expanduser(model_path)
        self.__dict_path__ = dict_path
        self.__model_path__ = model_path
        self.__symbol_path__ = symbol_path

        sequitur_options = Values()
        sequitur_options.resume_from_checkpoint = False
        sequitur_options.modelFile = model_path
        sequitur_options.shouldRampUp = False
        sequitur_options.trainSample = False
        sequitur_options.shouldTranspose = False
        sequitur_options.newModelFile = False
        sequitur_options.shouldSelfTest = False
        self.__model__ = SequiturTool.procureModel(sequitur_options, None)
        if not self.__model__:
            logger.error('Can\'t load g2p model.')
            return None
        self.__model__ = Translator(self.__model__)

        a = open(dict_path).readlines()
        a = [i.strip('\n') for i in a]
        for i in a:
            i = i.split(' ')
            self._dict_[i[0]] = i[1:]

        self.symbols = open(symbol_path).readlines()
        self.symbols = [i.strip('\n') for i in self.symbols]
        self.id2symbol = self.symbols
        self.symbol2id = {}
        for i, symbol in enumerate(self.symbols):
            self.symbol2id[symbol] = i

    def __hash__(self):
        return hash(frozenset([self.__dict_path__, self.__model_path__]))

    @lru_cache(maxsize=None)
    def __convert__(self, key):
        return self.__model__(key)

    def convert(self, key):
        key = key.lower()
        try:
            return self._dict_[key]
        except KeyError:
            result = self.__convert__(key)
            logger.debug('Converted "%s" to "%s" with g2p model ...' % (key, ' '.join(result)))
            return result

if __name__ == '__main__':
    g2p = G2P()
    print(g2p.convert('hello'))
    print(g2p.convert('github'))
