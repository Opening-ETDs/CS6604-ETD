import os
from os import listdir
import shutil
from pprint import pprint
docDir = '/Users/bipashabanerjee/Documents/CS/sem3/6604/grobid/dissertation/'
docLabels = [f for f in listdir(docDir) if not f.startswith('.') and not f.startswith('_') and  f.endswith('.xml')]
for id, f1 in enumerate(docLabels):
    current_file = os.path.join(docDir, f1)
    print(current_file)