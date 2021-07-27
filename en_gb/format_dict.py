#!/bin/python
beep = open('beep-1.0').readlines()
print(len(beep))
beep = [i.replace('\\', '') for i in beep]
beep = [i.replace('~', '') for i in beep]
beep = [i.replace('\r', '') for i in beep]
beep = [i.replace('"', '') for i in beep]
beep = [i.replace('^', '') for i in beep]
beep = [i for i in beep if not i[0] in '#`\'&%"!<-(']
beep = [i for i in beep if not '_' in i]
beep = [i if '\t' in i else i.replace(' ', '\t', 1) for i in beep]
beep = [[j for j in i.split('\t') if j != ''] for i in beep]
assert not False in [len(i) == 2 for i in beep]
beep = [[i[0].lower(), i[1].upper()] for i in beep]
symbols = set()
for line in beep:
    symbols.update(line[1].strip('\r\n').split(' '))
symbols = sorted(list(symbols))
beep = [' '.join(i) for i in beep]
print(len(beep))
print(len(symbols))

open('beep.dict', 'w').writelines(beep)
open('beep.symbols', 'w').write('\n'.join(symbols))
