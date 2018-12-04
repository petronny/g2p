#!/bin/python3
import os
import logging
from optparse import Values
import SequiturTool
from sequitur import Translator
from functools import lru_cache
logger = logging.getLogger()

class G2P(dict):
    def __init__(self, dict_path, model_path):
        self.__dict__ = dict()
        dict_path = os.path.expanduser(dict_path)
        model_path = os.path.expanduser(model_path)
        self.__dict_path__ = dict_path
        self.__model_path__ = model_path

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
            self.__dict__[i[0]] = i[1:]

    def __hash__(self):
        return hash(frozenset([self.__dict_path__, self.__model_path__]))

    @lru_cache(maxsize=None)
    def __getitem__(self, key):
        key = key.lower()
        try:
            return self.__dict__[key]
        except KeyError:
            result = self.__model__(key)
            logger.debug('Converted "%s" to "%s" with g2p model ...' % (key, ' '.join(result)))
            return result

if __name__ == '__main__':
    import sys

    sequitur_options = Values()
    sequitur_options.resume_from_checkpoint = False
    sequitur_options.modelFile = 'order-9'
    sequitur_options.shouldRampUp = False
    sequitur_options.trainSample = False
    sequitur_options.shouldTranspose = False
    sequitur_options.newModelFile = False
    sequitur_options.shouldSelfTest = False
    model = SequiturTool.procureModel(sequitur_options, None)
    if not model:
        print('Can\'t load g2p model.')
        sys.exit(1)
    translator= Translator(model)
    print(translator('hello'))
