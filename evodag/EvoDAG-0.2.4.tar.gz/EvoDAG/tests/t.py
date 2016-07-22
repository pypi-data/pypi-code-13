from test_root import X, cl
import sys
from EvoDAG.command_line import main
import tempfile
import json
import os

fname = tempfile.mktemp()
with open(fname, 'w') as fpt:
    for x, y in zip(X, cl):
        a = {k: v for k, v in enumerate(x)}
        a['klass'] = int(y)
        a['num_terms'] = len(x)
        fpt.write(json.dumps(a) + '\n')
sys.argv = ['EvoDAG', '-m', 'temp.evodag.gz', '--json', '-s2',
            '-e', '10', '-p', '100', fname]  # , '-ooutput.evodag', '-t', fname]
print("Empezando el main")
main()
print("Terminando el main")
os.unlink(fname)
os.unlink('temp.evodag.gz')
print(open('output.evodag').read())
os.unlink('output.evodag')
