import sys
from optparse import Values
import SequiturTool
from sequitur import Translator

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
